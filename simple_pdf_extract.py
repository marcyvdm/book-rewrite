#!/usr/bin/env python3
"""
Simple, reliable PDF text extraction
No over-engineering, just what works
"""

import json
import re
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


class SimplePDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.doc = fitz.open(str(self.pdf_path))
        
    def extract_metadata(self) -> Dict:
        """Extract actual PDF metadata"""
        metadata = self.doc.metadata
        return {
            "title": metadata.get("title", self.pdf_path.stem),
            "author": metadata.get("author", "Unknown"),
            "subject": metadata.get("subject", ""),
            "keywords": metadata.get("keywords", ""),
            "pages": self.doc.page_count,
            "creation_date": metadata.get("creationDate", ""),
            "modification_date": metadata.get("modDate", ""),
            "extracted_date": datetime.now().isoformat()
        }
    
    def extract_text_by_page(self) -> List[Dict]:
        """Extract text from each page, preserving layout"""
        pages = []
        for page_num, page in enumerate(self.doc):
            # Get text with layout preservation
            text = page.get_text()
            
            # Clean up excessive whitespace but preserve paragraph breaks
            text = re.sub(r'\n{3,}', '\n\n', text)  # Limit to double newlines
            text = re.sub(r' {2,}', ' ', text)  # Remove excessive spaces
            
            pages.append({
                "page_number": page_num + 1,
                "text": text.strip()
            })
        return pages
    
    def extract_full_text(self) -> str:
        """Extract all text as one continuous string with proper paragraph breaks"""
        full_text = []
        for page in self.doc:
            text = page.get_text()
            # Clean up but preserve structure
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r' {2,}', ' ', text)
            full_text.append(text.strip())
        
        # Join pages with clear page breaks
        return "\n\n---PAGE BREAK---\n\n".join(full_text)
    
    def extract_images(self, page_num: int) -> List[Dict]:
        """Extract images from a page with their data and positions"""
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
                image_data = None
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
                    
                    # Convert to PNG and encode as base64
                    if pix.n - pix.alpha < 4:  # Can convert to PNG
                        import base64
                        img_bytes = pix.tobytes("png")
                        image_data = base64.b64encode(img_bytes).decode('utf-8')
                        image_format = "png"
                    
                    pix = None  # Clean up
                    
                except Exception as e:
                    # If we can't extract the image data, still record the image exists
                    print(f"Could not extract image data for page {page_num + 1}, image {img_index + 1}: {e}")
                
                images.append({
                    "type": "image",
                    "page": page_num + 1,
                    "index": img_index,
                    "position": position,
                    "actual_size": actual_size,
                    "format": image_format,
                    "data": image_data,  # base64 encoded image
                    "data_size_bytes": len(image_data) if image_data else 0,
                    "description": f"Image {img_index + 1} on page {page_num + 1}",
                    "id": f"img_p{page_num + 1:03d}_{img_index + 1:02d}"
                })
                
            except Exception as e:
                # Still record that an image exists, even if we can't process it
                images.append({
                    "type": "image",
                    "page": page_num + 1,
                    "index": img_index,
                    "position": {"x": 0, "y": 0, "width": 0, "height": 0},
                    "actual_size": {"width": 0, "height": 0},
                    "format": "unknown",
                    "data": None,
                    "data_size_bytes": 0,
                    "description": f"Image {img_index + 1} on page {page_num + 1} (extraction failed)",
                    "id": f"img_p{page_num + 1:03d}_{img_index + 1:02d}"
                })
        
        return images
    
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
        
        # Skip empty lines
        if not line:
            return True
            
        # Common patterns
        patterns = [
            r'^CHAPTER\s+[A-Z]+\s*•',  # CHAPTER ONE • 
            r'^\d+\s*$',  # Just page numbers
            r'^Page\s+\d+',  # Page X
            r'^Copyright\s+',  # Copyright
            r'^©\s+\d{4}',  # Copyright symbol
        ]
        
        for pattern in patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True
        
        # Check if line starts with page number followed by short text
        # This catches cases like "14 CHAPTER ONE • DEFINING GAME FEEL"
        if re.match(r'^\d+\s+[A-Z\s]+•', line):
            return True
            
        return False
    
    def find_captions_near_images(self, page_text: str, images: List[Dict]) -> Dict[int, str]:
        """Find captions that are likely associated with images on the page"""
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
                    for img_idx, img in enumerate(images):
                        if img_idx not in image_captions:
                            image_captions[img_idx] = caption_text
                            break
                    break
            
            # Also look for short lines that might be captions (conservative)
            # These are often centered or isolated lines near images
            if (len(line) > 10 and len(line) < 100 and 
                not line.endswith('.') and 
                not re.match(r'^\d+', line) and  # Not starting with page numbers
                not line.isupper()):  # Not all caps (likely headers)
                
                # Check if this line is surrounded by empty lines or short lines
                # This suggests it might be a standalone caption
                prev_line = lines[i-1].strip() if i > 0 else ""
                next_line = lines[i+1].strip() if i < len(lines)-1 else ""
                
                if (len(prev_line) < 10 and len(next_line) < 10 and 
                    len([img for img in images if img not in image_captions.values()]) > 0):
                    # Assign to next available image
                    for img_idx, img in enumerate(images):
                        if img_idx not in image_captions:
                            image_captions[img_idx] = line
                            break
        
        return image_captions
    
    def extract_chapter_content(self, start_page: int, end_page: Optional[int] = None) -> Dict:
        """Extract full content of a chapter including text and images"""
        if end_page is None:
            end_page = self.doc.page_count
        
        chapter_content = []
        
        for page_num in range(start_page - 1, min(end_page, self.doc.page_count)):
            page = self.doc[page_num]
            
            # Get text and clean headers/footers
            text = page.get_text()
            text = self.clean_page_text(text, page_num)
            text = re.sub(r'\n{3,}', '\n\n', text)
            text = re.sub(r' {2,}', ' ', text)
            
            # Get images for this page first
            images = self.extract_images(page_num)
            
            # Find captions for images on this page
            image_captions = self.find_captions_near_images(text, images)
            
            # Assign captions to images
            for img_idx, caption in image_captions.items():
                if img_idx < len(images):
                    images[img_idx]["caption"] = caption
            
            # Split into paragraphs for this page
            page_paragraphs = []
            caption_texts = set(image_captions.values())  # Don't include these as paragraphs
            
            for para in text.split('\n\n'):
                para = para.replace('\n', ' ').strip()
                
                # Skip if it's too short
                if len(para) <= 20:
                    continue
                
                # Skip if this text is already used as a caption
                if para in caption_texts:
                    continue
                
                page_paragraphs.append({
                    "type": "paragraph",
                    "content": para,
                    "page": page_num + 1
                })
            
            # Interleave images with paragraphs based on position
            # Simple approach: add images after every few paragraphs
            if images and page_paragraphs:
                # Insert images throughout the paragraphs
                items_per_image = max(1, len(page_paragraphs) // (len(images) + 1))
                combined = []
                img_index = 0
                
                for i, para in enumerate(page_paragraphs):
                    combined.append(para)
                    if img_index < len(images) and (i + 1) % items_per_image == 0:
                        combined.append(images[img_index])
                        img_index += 1
                
                # Add any remaining images at the end
                while img_index < len(images):
                    combined.append(images[img_index])
                    img_index += 1
                    
                chapter_content.extend(combined)
            else:
                # No images or no paragraphs, just add what we have
                chapter_content.extend(page_paragraphs)
                chapter_content.extend(images)
        
        return chapter_content
    
    def detect_chapters(self, pages: List[Dict], toc: Optional[List[Dict]] = None) -> List[Dict]:
        """Use TOC if available, otherwise detect chapters from text"""
        chapters = []
        
        # If we have a TOC, use it as the primary source
        if toc:
            for i, entry in enumerate(toc):
                # Determine end page (start of next chapter or end of document)
                end_page = toc[i + 1]["page"] if i + 1 < len(toc) else self.doc.page_count
                
                # Extract full chapter content
                chapter_content = self.extract_chapter_content(entry["page"], end_page)
                
                chapters.append({
                    "title": entry["title"],
                    "page_start": entry["page"],
                    "page_end": end_page - 1,
                    "content": chapter_content,
                    "source": "toc"
                })
            return chapters
        
        # Otherwise, look for chapter headings (but be more conservative)
        # Only look for explicit CHAPTER markers
        chapter_patterns = [
            r'^CHAPTER\s+([A-Z]+|\d+)',    # CHAPTER ONE, CHAPTER 1
            r'^Chapter\s+(\d+)',            # Chapter 1
        ]
        
        combined_pattern = '|'.join(f'({p})' for p in chapter_patterns)
        
        for page_data in pages:
            page_num = page_data["page_number"]
            text = page_data["text"]
            
            # Check first few lines of each page for chapter headings
            lines = text.split('\n')[:10]  # Check first 10 lines
            
            for i, line in enumerate(lines):
                line = line.strip()
                if re.match(combined_pattern, line, re.IGNORECASE):
                    # Found a chapter heading
                    title = line
                    
                    # Try to get the actual chapter title from the next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.isdigit() and len(next_line) > 3:
                            title = f"{line}: {next_line}"
                    
                    # Find the end page (next chapter or end of doc)
                    end_page = self.doc.page_count
                    for future_page in pages[pages.index(page_data) + 1:]:
                        future_text = future_page["text"]
                        future_lines = future_text.split('\n')[:10]
                        for future_line in future_lines:
                            if re.match(combined_pattern, future_line.strip(), re.IGNORECASE):
                                end_page = future_page["page_number"]
                                break
                        if end_page != self.doc.page_count:
                            break
                    
                    # Extract full chapter content
                    chapter_content = self.extract_chapter_content(page_num, end_page)
                    
                    chapters.append({
                        "title": title,
                        "page_start": page_num,
                        "page_end": end_page - 1,
                        "content": chapter_content,
                        "source": "detected"
                    })
                    break
        
        return chapters
    
    def extract_toc(self) -> Optional[List[Dict]]:
        """Try to extract table of contents if it exists"""
        toc_entries = []
        
        # Look for TOC in first 20 pages
        for page_num in range(min(20, self.doc.page_count)):
            page = self.doc[page_num]
            text = page.get_text()
            
            # Check if this page contains TOC
            if 'table of contents' in text.lower() or 'contents' in text.lower()[:100]:
                # Extract lines that look like TOC entries (text followed by page numbers)
                lines = text.split('\n')
                
                for line in lines:
                    # Match patterns like "1. Introduction.....23" or "Chapter 1: Title     15"
                    toc_match = re.match(r'^(.+?)[\.\s]{2,}(\d+)\s*$', line.strip())
                    if toc_match:
                        toc_entries.append({
                            "title": toc_match.group(1).strip(),
                            "page": int(toc_match.group(2))
                        })
                
                if toc_entries:
                    break
        
        return toc_entries if toc_entries else None
    
    def extract_paragraphs(self, text: str) -> List[str]:
        """Split text into proper paragraphs, not individual lines"""
        # Split on double newlines (actual paragraph breaks)
        paragraphs = text.split('\n\n')
        
        # Clean up each paragraph
        cleaned_paragraphs = []
        for para in paragraphs:
            # Join lines within a paragraph (remove single newlines)
            para = para.replace('\n', ' ')
            # Clean up whitespace
            para = re.sub(r'\s+', ' ', para).strip()
            
            # Only keep paragraphs with actual content (more than 20 chars)
            if len(para) > 20:
                cleaned_paragraphs.append(para)
        
        return cleaned_paragraphs
    
    def extract(self) -> Dict:
        """Main extraction method - returns everything in a simple structure"""
        print(f"Extracting: {self.pdf_path}")
        
        # Get metadata
        metadata = self.extract_metadata()
        print(f"  Title: {metadata['title']}")
        print(f"  Author: {metadata['author']}")
        print(f"  Pages: {metadata['pages']}")
        
        # Extract text by pages
        print("  Extracting text...")
        pages = self.extract_text_by_page()
        
        # Get full text
        full_text = self.extract_full_text()
        
        # Extract paragraphs from full text
        print("  Detecting paragraphs...")
        paragraphs = self.extract_paragraphs(full_text)
        print(f"  Found {len(paragraphs)} paragraphs")
        
        # Try to extract TOC first
        print("  Looking for table of contents...")
        toc = self.extract_toc()
        if toc:
            print(f"  Found {len(toc)} TOC entries")
        
        # Detect chapters (using TOC if available)
        print("  Detecting chapters...")
        chapters = self.detect_chapters(pages, toc)
        print(f"  Found {len(chapters)} chapters")
        
        # Calculate stats
        word_count = len(full_text.split())
        avg_words_per_page = word_count // metadata['pages'] if metadata['pages'] > 0 else 0
        
        # Count total images
        total_images = sum(
            len([item for item in ch.get("content", []) if item.get("type") == "image"])
            for ch in chapters
        )
        
        return {
            "metadata": metadata,
            "statistics": {
                "total_words": word_count,
                "total_paragraphs": len(paragraphs),
                "total_chapters": len(chapters),
                "total_images": total_images,
                "avg_words_per_page": avg_words_per_page
            },
            "table_of_contents": toc,
            "chapters": chapters  # Full chapter content with paragraphs and images
        }
    
    def close(self):
        """Clean up"""
        self.doc.close()


def main():
    """Test the extractor"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python simple_pdf_extract.py <pdf_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"File not found: {pdf_path}")
        sys.exit(1)
    
    # Extract
    extractor = SimplePDFExtractor(pdf_path)
    try:
        result = extractor.extract()
        
        # Save to JSON
        output_path = Path(pdf_path).with_suffix('.simple.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\nExtraction complete!")
        print(f"Results saved to: {output_path}")
        
        # Show summary
        print("\n=== Summary ===")
        print(f"Title: {result['metadata']['title']}")
        print(f"Author: {result['metadata']['author']}")
        print(f"Pages: {result['metadata']['pages']}")
        print(f"Words: {result['statistics']['total_words']:,}")
        print(f"Paragraphs: {result['statistics']['total_paragraphs']:,}")
        print(f"Chapters: {result['statistics']['total_chapters']}")
        print(f"Images: {result['statistics'].get('total_images', 0)}")
        
        if result['chapters']:
            print("\n=== Chapters Found ===")
            for ch in result['chapters'][:10]:  # Show first 10
                content = ch.get('content', [])
                para_count = len([c for c in content if c.get('type') == 'paragraph'])
                img_count = len([c for c in content if c.get('type') == 'image'])
                print(f"  Page {ch['page_start']}-{ch.get('page_end', '?')}: {ch['title']}")
                print(f"    -> {para_count} paragraphs, {img_count} images")
        
    finally:
        extractor.close()


if __name__ == "__main__":
    main()