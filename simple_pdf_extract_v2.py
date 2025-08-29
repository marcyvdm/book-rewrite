#!/usr/bin/env python3
"""
Simple PDF extractor - AI-agent friendly version
Creates separate files instead of bloated JSON
"""

import json
import re
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])
    import fitz


class AIFriendlyPDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.doc = fitz.open(str(self.pdf_path))
        
    def clean_page_text(self, text: str, page_num: int) -> str:
        """Remove headers/footers from page text"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip obvious headers/footers
            if self.is_header_footer_line(line, page_num):
                continue
                
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def is_header_footer_line(self, line: str, page_num: int) -> bool:
        """Check if a single line is header/footer"""
        line = line.strip()
        
        if not line:
            return True
            
        # Common patterns
        patterns = [
            r'^CHAPTER\s+[A-Z]+\s*•',  # CHAPTER ONE • 
            r'^THE\s+[A-Z\s]+OF\s+GAME\s+FEEL$',  # THE THREE BUILDING BLOCKS OF GAME FEEL
            r'^[A-Z\s]{20,}$',  # Long all-caps lines (likely headers)
            r'^\d+\s*$',  # Just page numbers
            r'^Page\s+\d+',  # Page X
            r'^Copyright\s+',  # Copyright
            r'^©\s+\d{4}',  # Copyright symbol
        ]
        
        for pattern in patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True
        
        # Check if line starts with page number followed by short text
        if re.match(r'^\d+\s+[A-Z\s]+•', line):
            return True
            
        return False
    
    def extract_images_to_files(self, page_num: int, output_dir: Path, chapter_id: str) -> List[Dict]:
        """Extract images from a page and save as separate files"""
        images = []
        page = self.doc[page_num]
        
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                
                # Get image position
                try:
                    img_rect = page.get_image_bbox(img)
                    position = {
                        "x": round(img_rect.x0, 2),
                        "y": round(img_rect.y0, 2),
                        "width": round(img_rect.width, 2),
                        "height": round(img_rect.height, 2)
                    }
                except:
                    position = {
                        "x": 0,
                        "y": img_index * 100,
                        "width": 100,
                        "height": 100
                    }
                
                # Extract actual image data
                image_filename = None
                image_format = "unknown"
                actual_size = {"width": 0, "height": 0}
                
                try:
                    # Get the image object from PDF
                    pix = fitz.Pixmap(self.doc, xref)
                    
                    # Get actual image dimensions
                    actual_size = {
                        "width": pix.width,
                        "height": pix.height
                    }
                    
                    # Create filename
                    image_id = f"img_{chapter_id}_p{page_num + 1:03d}_{img_index + 1:02d}"
                    
                    # Convert to appropriate format and save
                    if pix.n - pix.alpha < 4:  # Can convert to PNG
                        img_bytes = pix.tobytes("png")
                        image_filename = f"{image_id}.png"
                        image_format = "png"
                    else:
                        img_bytes = pix.tobytes("jpeg")
                        image_filename = f"{image_id}.jpg"
                        image_format = "jpeg"
                    
                    # Save image file
                    image_path = output_dir / image_filename
                    with open(image_path, 'wb') as f:
                        f.write(img_bytes)
                    
                    pix = None  # Clean up
                    
                except Exception as e:
                    print(f"Could not extract image data for page {page_num + 1}, image {img_index + 1}: {e}")
                
                # Create image metadata (no base64 data!)
                images.append({
                    "type": "image",
                    "id": image_id,
                    "filename": image_filename,
                    "page": page_num + 1,
                    "index": img_index,
                    "position": position,
                    "actual_size": actual_size,
                    "format": image_format,
                    "description": f"Image {img_index + 1} on page {page_num + 1}"
                })
                
            except Exception as e:
                print(f"Failed to process image on page {page_num + 1}: {e}")
        
        return images
    
    def find_captions_near_images(self, page_text: str, images: List[Dict]) -> Dict[str, str]:
        """Find captions and map them to image IDs"""
        if not images:
            return {}
        
        lines = page_text.split('\n')
        image_captions = {}
        
        # Look for caption patterns in the text
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check for explicit caption markers
            caption_patterns = [
                r'^Figure\s+\d+[\.:]\s*(.+)',  # Figure 1: Description
                r'^Fig\.\s+\d+[\.:]\s*(.+)',   # Fig. 1: Description
                r'^Image\s+\d+[\.:]\s*(.+)',   # Image 1: Description
                r'^Table\s+\d+[\.:]\s*(.+)',   # Table 1: Description
                r'^Illustration\s+\d+[\.:]\s*(.+)',    # Illustration 1: Description
                r'^Screenshot[\.:]\s*(.+)',         # Screenshot: Description
                r'^Source:\s*(.+)',            # Source: citation
                r'^Diagram\s+\d+[\.:]\s*(.+)', # Diagram 1: Description
            ]
            
            for pattern in caption_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    caption_text = match.group(1).strip() if match.lastindex else line
                    # Assign to the first available image (simple heuristic)
                    for img in images:
                        if img["id"] not in image_captions:
                            image_captions[img["id"]] = caption_text
                            break
                    break
        
        return image_captions
    
    def extract_chapter_content(self, start_page: int, end_page: int, chapter_id: str, output_dir: Path) -> Dict:
        """Extract full content of a chapter"""
        chapter_content = []
        chapter_images = []
        all_paragraphs = []
        
        # Process each page individually (original working approach)
        for page_num in range(start_page - 1, min(end_page, self.doc.page_count)):
            page = self.doc[page_num]
            
            # Get text and clean headers/footers
            text = page.get_text()
            text = self.clean_page_text(text, page_num)
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r' {2,}', ' ', text)
            
            # Extract images to files
            page_images = self.extract_images_to_files(page_num, output_dir, chapter_id)
            chapter_images.extend(page_images)
            
            # Find captions for images on this page
            image_captions = self.find_captions_near_images(text, page_images)
            
            # Assign captions to images
            for img in page_images:
                if img["id"] in image_captions:
                    img["caption"] = image_captions[img["id"]]
            
            # Split into paragraphs for this page
            page_paragraphs = []
            caption_texts = set(image_captions.values())
            
            # Detect paragraphs by looking for capitalized lines that start with spaces
            lines = text.split('\n')
            current_paragraph = []
            
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # If line starts with space AND is capitalized, it's a new paragraph
                if line.startswith(' ') and current_paragraph:
                    first_word = line.strip().split()[0] if line.strip().split() else ""
                    is_capitalized = first_word and first_word[0].isupper()
                    
                    if is_capitalized:
                        # Save previous paragraph
                        para_text = ' '.join(current_paragraph).strip()
                        if len(para_text) > 30 and para_text not in caption_texts:
                            page_paragraphs.append(para_text)
                        current_paragraph = [line.strip()]
                    else:
                        # This is a continuation, add to current paragraph
                        current_paragraph.append(line.strip())
                else:
                    # Continue current paragraph
                    current_paragraph.append(line.strip())
            
            # Don't forget the last paragraph on this page
            if current_paragraph:
                para_text = ' '.join(current_paragraph).strip()
                if len(para_text) > 30 and para_text not in caption_texts:
                    page_paragraphs.append(para_text)
            
            # Add paragraphs to overall collection
            all_paragraphs.extend(page_paragraphs)
            
            # Store page content temporarily
            for para_text in page_paragraphs:
                chapter_content.append({
                    "type": "paragraph",
                    "content": para_text,
                    "page": page_num + 1
                })
            
            # Add images for this page
            chapter_content.extend(page_images)
        
        # Post-processing: Fix cross-page continuations
        # Look for paragraphs that start with lowercase (likely continuations)
        fixed_content = []
        i = 0
        
        while i < len(chapter_content):
            item = chapter_content[i]
            
            if item["type"] == "paragraph":
                content = item["content"]
                
                # If paragraph starts with lowercase, it might be a continuation
                if content and content[0].islower():
                    # Find the previous paragraph to merge with
                    prev_para_idx = -1
                    for j in range(len(fixed_content) - 1, -1, -1):
                        if fixed_content[j]["type"] == "paragraph":
                            prev_para_idx = j
                            break
                    
                    if prev_para_idx >= 0:
                        # Merge with previous paragraph
                        fixed_content[prev_para_idx]["content"] += " " + content
                        i += 1
                        continue
                
                # Not a continuation, add as is
                fixed_content.append(item)
            else:
                # Not a paragraph (image), add as is
                fixed_content.append(item)
            
            i += 1
        
        return {
            "content": fixed_content,
            "images": chapter_images
        }
    
    def find_real_chapters(self) -> List[Dict]:
        """Find actual chapter starts by looking for CHAPTER headings"""
        chapter_starts = []
        
        for page_num in range(self.doc.page_count):
            page = self.doc[page_num]
            text = page.get_text()
            lines = text.split('\n')
            
            if lines:
                first_line = lines[0].strip()
                
                # Look for "CHAPTER [WORD] • [TITLE]" pattern
                if re.match(r'CHAPTER\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|ELEVEN|TWELVE)\s*•', first_line, re.IGNORECASE):
                    # Extract chapter title
                    title_match = re.match(r'CHAPTER\s+\w+\s*•\s*(.+)', first_line, re.IGNORECASE)
                    title = title_match.group(1).strip() if title_match else "Unknown"
                    
                    chapter_starts.append({
                        'pdf_page': page_num + 1,
                        'title': title,
                        'full_heading': first_line
                    })
        
        # Remove duplicates (keep first occurrence of each chapter)
        unique_chapters = []
        seen_titles = set()
        
        for ch in chapter_starts:
            if ch['title'] not in seen_titles:
                unique_chapters.append(ch)
                seen_titles.add(ch['title'])
        
        return unique_chapters
    
    def extract_to_files(self, output_dir: str = None) -> Dict:
        """Extract PDF to AI-friendly file structure"""
        if output_dir is None:
            output_dir = self.pdf_path.stem + "_extracted"
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        images_dir = output_path / "images"
        chapters_dir = output_path / "chapters"
        images_dir.mkdir(exist_ok=True)
        chapters_dir.mkdir(exist_ok=True)
        
        print(f"Extracting: {self.pdf_path}")
        
        # Get metadata
        metadata = {
            "title": self.doc.metadata.get("title", self.pdf_path.stem),
            "author": self.doc.metadata.get("author", "Unknown"),
            "subject": self.doc.metadata.get("subject", ""),
            "pages": self.doc.page_count,
            "extracted_date": datetime.now().isoformat(),
            "source_file": str(self.pdf_path)
        }
        
        print(f"  Title: {metadata['title']}")
        print(f"  Author: {metadata['author']}")
        print(f"  Pages: {metadata['pages']}")
        
        # Find real chapters
        chapters = self.find_real_chapters()
        print(f"  Found {len(chapters)} real chapters")
        
        # Extract chapters
        chapters_info = []
        total_images = 0
        
        if chapters:
            for i, chapter in enumerate(chapters):
                chapter_id = f"ch{i+1:02d}"
                start_page = chapter["pdf_page"]
                end_page = chapters[i + 1]["pdf_page"] if i + 1 < len(chapters) else self.doc.page_count
                
                print(f"  Extracting Chapter {i+1}: {chapter['title']}")
                
                # Extract chapter content
                chapter_data = self.extract_chapter_content(
                    start_page, end_page, chapter_id, images_dir
                )
                
                # Count content types
                paragraphs = [item for item in chapter_data["content"] if item["type"] == "paragraph"]
                images = [item for item in chapter_data["content"] if item["type"] == "image"]
                
                chapter_info = {
                    "id": chapter_id,
                    "number": i + 1,
                    "title": chapter["title"],
                    "page_start": start_page,
                    "page_end": end_page - 1,
                    "paragraph_count": len(paragraphs),
                    "image_count": len(images),
                    "word_count": sum(len(p["content"].split()) for p in paragraphs)
                }
                
                chapters_info.append(chapter_info)
                total_images += len(images)
                
                # Save individual chapter file
                chapter_file = chapters_dir / f"{chapter_id}.json"
                chapter_output = {
                    "metadata": chapter_info,
                    "content": chapter_data["content"]
                }
                
                with open(chapter_file, 'w', encoding='utf-8') as f:
                    json.dump(chapter_output, f, indent=2, ensure_ascii=False)
                
                print(f"    -> {len(paragraphs)} paragraphs, {len(images)} images")
        
        # Create main metadata file
        main_metadata = {
            "book": metadata,
            "extraction_summary": {
                "total_chapters": len(chapters_info),
                "total_images": total_images,
                "total_words": sum(ch["word_count"] for ch in chapters_info),
                "extraction_date": datetime.now().isoformat()
            },
            "chapters_detected": [{"title": ch["title"], "page": ch["pdf_page"]} for ch in chapters],
            "chapters": chapters_info,
            "file_structure": {
                "metadata_file": "metadata.json",
                "chapters_directory": "chapters/",
                "images_directory": "images/",
                "chapter_files": [f"{ch['id']}.json" for ch in chapters_info]
            }
        }
        
        metadata_file = output_path / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(main_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\nExtraction complete!")
        print(f"Output directory: {output_path.absolute()}")
        print(f"Structure:")
        print(f"  metadata.json - Main book metadata and index")
        print(f"  chapters/ - Individual chapter JSON files")
        print(f"  images/ - All extracted images as PNG/JPEG files")
        print(f"\nFor AI agents:")
        print(f"  1. Read metadata.json first")
        print(f"  2. Process individual chapter files from chapters/")
        print(f"  3. Reference images by filename from content")
        
        return main_metadata
    
    def close(self):
        """Clean up"""
        self.doc.close()


def main():
    """Test the AI-friendly extractor"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_pdf_extract_v2.py <pdf_file> [output_dir]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(pdf_path).exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    
    # Extract
    extractor = AIFriendlyPDFExtractor(pdf_path)
    try:
        result = extractor.extract_to_files(output_dir)
    finally:
        extractor.close()


if __name__ == "__main__":
    main()