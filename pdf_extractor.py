#!/usr/bin/env python3
"""
PDF Extraction Script for AI Book Processing
Extracts text, structure, and images from PDF files for book rewriting pipeline.
"""

import json
import uuid
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import argparse

try:
    import fitz  # PyMuPDF
    from PIL import Image
    import io
except ImportError as e:
    print(f"Error: Required libraries not installed. Run: pip install pymupdf pillow")
    print(f"Missing: {e}")
    exit(1)


class PDFExtractor:
    def __init__(self, pdf_path: str, output_dir: str = "extracted-content"):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.doc = fitz.open(str(self.pdf_path))
        
        # Create subdirectories
        (self.output_dir / "images").mkdir(exist_ok=True)
        (self.output_dir / "text").mkdir(exist_ok=True)
        
        print(f"Initialized PDF extractor for: {self.pdf_path.name}")
        print(f"Pages: {len(self.doc)}")

    def extract_metadata(self) -> Dict:
        """Extract PDF metadata and infer book information."""
        metadata = self.doc.metadata
        
        # Try to parse filename for book info
        filename = self.pdf_path.stem
        parts = filename.split(" -- ")
        
        extracted_metadata = {
            "filename": self.pdf_path.name,
            "total_pages": len(self.doc),
            "extraction_date": datetime.now().isoformat(),
            "pdf_metadata": metadata,
        }
        
        # Parse filename format: Title -- Author -- Publisher, Year -- etc.
        if len(parts) >= 2:
            extracted_metadata["title"] = parts[0].strip()
            extracted_metadata["author"] = parts[1].strip()
            if len(parts) >= 3:
                pub_info = parts[2].strip()
                # Try to extract year
                year_match = re.search(r'\b(19|20)\d{2}\b', pub_info)
                if year_match:
                    extracted_metadata["publication_year"] = int(year_match.group())
                extracted_metadata["publisher_info"] = pub_info
        
        return extracted_metadata

    def detect_chapter_structure(self, text_blocks: List[Dict]) -> List[Dict]:
        """Detect chapters, sections, and headings based on text formatting."""
        chapters = []
        current_chapter = None
        current_section = None
        
        # Common chapter patterns
        chapter_patterns = [
            r'^Chapter\s+\d+',
            r'^\d+\.\s+[A-Z][^.]*$',
            r'^[A-Z][A-Z\s]{10,}$',  # ALL CAPS headings
        ]
        
        section_patterns = [
            r'^\d+\.\d+\s+',
            r'^[A-Z][a-z]+\s+[A-Z][a-z]+',  # Title Case headings
        ]
        
        for block in text_blocks:
            text = block['text'].strip()
            if not text:
                continue
                
            # Check for chapter headings
            is_chapter = any(re.match(pattern, text, re.IGNORECASE) for pattern in chapter_patterns)
            if is_chapter or (block['font_size'] > 16 and len(text) < 100):
                if current_chapter:
                    chapters.append(current_chapter)
                
                current_chapter = {
                    "id": f"ch-{len(chapters) + 1}",
                    "title": text,
                    "page_start": block['page'],
                    "sections": [],
                    "font_size": block['font_size'],
                }
                current_section = None
                continue
            
            # Check for section headings
            is_section = any(re.match(pattern, text) for pattern in section_patterns)
            if is_section or (block['font_size'] > 12 and len(text) < 150 and current_chapter):
                if current_section:
                    current_chapter['sections'].append(current_section)
                
                current_section = {
                    "id": f"sec-{len(current_chapter['sections']) + 1}",
                    "title": text,
                    "page": block['page'],
                    "paragraphs": [],
                    "font_size": block['font_size'],
                }
                continue
            
            # Regular paragraph text
            if current_chapter:
                if not current_section:
                    # Create default section for ungrouped content
                    current_section = {
                        "id": f"sec-{len(current_chapter['sections']) + 1}",
                        "title": "Introduction",
                        "page": block['page'],
                        "paragraphs": [],
                        "font_size": 12,
                    }
                
                current_section['paragraphs'].append({
                    "id": str(uuid.uuid4()),
                    "text": text,
                    "page": block['page'],
                    "font_size": block['font_size'],
                    "bbox": block['bbox'],
                })
        
        # Add final chapter and section
        if current_section and current_chapter:
            current_chapter['sections'].append(current_section)
        if current_chapter:
            chapters.append(current_chapter)
            
        return chapters

    def extract_text_with_structure(self, max_pages: Optional[int] = None) -> Tuple[List[Dict], List[Dict]]:
        """Extract text with formatting information to detect structure."""
        text_blocks = []
        images = []
        
        pages_to_process = min(len(self.doc), max_pages) if max_pages else len(self.doc)
        
        for page_num in range(pages_to_process):
            page = self.doc.load_page(page_num)
            
            # Extract text with formatting
            blocks = page.get_text("dict")
            
            for block in blocks["blocks"]:
                if "lines" in block:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                text_blocks.append({
                                    "text": text,
                                    "page": page_num + 1,
                                    "font_size": span["size"],
                                    "font_name": span["font"],
                                    "bbox": span["bbox"],
                                    "flags": span["flags"],  # Bold, italic, etc.
                                })
                
                elif "image" in block:  # Image block
                    images.append({
                        "page": page_num + 1,
                        "bbox": block["bbox"],
                        "block_type": "image"
                    })
            
            print(f"Processed page {page_num + 1}/{pages_to_process}")
        
        return text_blocks, images

    def extract_images(self, max_pages: Optional[int] = None) -> List[Dict]:
        """Extract all images from the PDF with metadata."""
        extracted_images = []
        
        pages_to_process = min(len(self.doc), max_pages) if max_pages else len(self.doc)
        
        for page_num in range(pages_to_process):
            page = self.doc.load_page(page_num)
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(self.doc, xref)
                    
                    if pix.n - pix.alpha < 4:  # GRAY or RGB
                        img_filename = f"page_{page_num + 1}_img_{img_index + 1}.png"
                        img_path = self.output_dir / "images" / img_filename
                        
                        pix.save(str(img_path))
                        
                        # Get image dimensions and other metadata
                        img_info = {
                            "id": f"img-{page_num}-{img_index}",
                            "filename": img_filename,
                            "page": page_num + 1,
                            "width": pix.width,
                            "height": pix.height,
                            "colorspace": pix.colorspace.name if pix.colorspace else "Unknown",
                            "bbox": img[1:5],  # Bounding box coordinates
                            "file_size": img_path.stat().st_size,
                        }
                        
                        extracted_images.append(img_info)
                        print(f"Extracted image: {img_filename}")
                    
                    pix = None  # Free memory
                    
                except Exception as e:
                    print(f"Error extracting image on page {page_num + 1}: {e}")
                    continue
        
        return extracted_images

    def create_paragraphs_from_text(self, text_blocks: List[Dict]) -> List[Dict]:
        """Group text blocks into logical paragraphs."""
        paragraphs = []
        current_paragraph = []
        current_page = 1
        
        for block in text_blocks:
            text = block['text'].strip()
            
            # Skip very short text (likely artifacts)
            if len(text) < 3:
                continue
            
            # Check if this starts a new paragraph
            starts_new_paragraph = (
                len(current_paragraph) == 0 or
                block['page'] != current_page or
                text[0].isupper() and text.endswith('.') and len(text) > 50 or
                text.startswith(('Chapter', 'Section', '1.', '2.', '3.', '4.', '5.'))
            )
            
            if starts_new_paragraph and current_paragraph:
                # Finalize current paragraph
                paragraph_text = ' '.join([p['text'] for p in current_paragraph])
                if len(paragraph_text.strip()) > 20:  # Only include substantial paragraphs
                    paragraphs.append({
                        "id": str(uuid.uuid4()),
                        "content": paragraph_text.strip(),
                        "page_start": current_paragraph[0]['page'],
                        "page_end": current_paragraph[-1]['page'],
                        "word_count": len(paragraph_text.split()),
                        "font_size": current_paragraph[0]['font_size'],
                        "bbox": current_paragraph[0]['bbox'],
                    })
                current_paragraph = []
            
            current_paragraph.append(block)
            current_page = block['page']
        
        # Add final paragraph
        if current_paragraph:
            paragraph_text = ' '.join([p['text'] for p in current_paragraph])
            if len(paragraph_text.strip()) > 20:
                paragraphs.append({
                    "id": str(uuid.uuid4()),
                    "content": paragraph_text.strip(),
                    "page_start": current_paragraph[0]['page'],
                    "page_end": current_paragraph[-1]['page'],
                    "word_count": len(paragraph_text.split()),
                    "font_size": current_paragraph[0]['font_size'],
                    "bbox": current_paragraph[0]['bbox'],
                })
        
        return paragraphs

    def process_pdf(self, max_pages: Optional[int] = None, extract_images: bool = True) -> Dict:
        """Main processing function that extracts everything."""
        print(f"\n{'='*60}")
        print(f"PROCESSING PDF: {self.pdf_path.name}")
        print(f"{'='*60}")
        
        # Extract metadata
        print("📋 Extracting metadata...")
        metadata = self.extract_metadata()
        
        # Extract text with structure
        print("📖 Extracting text content...")
        text_blocks, image_blocks = self.extract_text_with_structure(max_pages)
        
        # Detect structure
        print("🏗️  Detecting document structure...")
        chapters = self.detect_chapter_structure(text_blocks)
        
        # Create paragraphs
        print("📝 Creating paragraph structure...")
        paragraphs = self.create_paragraphs_from_text(text_blocks)
        
        # Extract images
        extracted_images = []
        if extract_images:
            print("🖼️  Extracting images...")
            extracted_images = self.extract_images(max_pages)
        
        # Calculate statistics
        total_words = sum(p['word_count'] for p in paragraphs)
        reading_time = max(1, total_words // 250)  # Assume 250 WPM
        
        result = {
            "extraction_metadata": metadata,
            "book_metadata": {
                "id": str(uuid.uuid4()),
                "title": metadata.get("title", "Unknown Title"),
                "author": metadata.get("author", "Unknown Author"),
                "publication_year": metadata.get("publication_year"),
                "source_format": "pdf",
                "total_pages": metadata["total_pages"],
                "pages_processed": max_pages if max_pages else metadata["total_pages"],
                "extraction_date": metadata["extraction_date"],
                "word_count": total_words,
                "estimated_reading_time_minutes": reading_time,
                "category": "technical",  # Default, can be refined
            },
            "chapters": chapters,
            "paragraphs": paragraphs,
            "images": extracted_images,
            "statistics": {
                "total_paragraphs": len(paragraphs),
                "total_chapters": len(chapters),
                "total_images": len(extracted_images),
                "average_words_per_paragraph": total_words / len(paragraphs) if paragraphs else 0,
                "pages_with_images": len(set(img['page'] for img in extracted_images)),
            }
        }
        
        return result

    def save_extraction(self, data: Dict, output_filename: Optional[str] = None) -> Path:
        """Save extraction results to JSON file."""
        if not output_filename:
            safe_title = re.sub(r'[^\w\s-]', '', data['book_metadata']['title'])
            safe_title = re.sub(r'[-\s]+', '-', safe_title).strip('-').lower()
            output_filename = f"{safe_title}-extracted.json"
        
        output_path = self.output_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Extraction complete!")
        print(f"📄 Saved to: {output_path}")
        print(f"📊 Statistics:")
        stats = data['statistics']
        print(f"   • {stats['total_chapters']} chapters")
        print(f"   • {stats['total_paragraphs']} paragraphs")
        print(f"   • {stats['total_images']} images")
        print(f"   • {data['book_metadata']['word_count']} words")
        print(f"   • ~{data['book_metadata']['estimated_reading_time_minutes']} min read")
        
        return output_path

    def close(self):
        """Clean up resources."""
        if hasattr(self, 'doc'):
            self.doc.close()


def main():
    parser = argparse.ArgumentParser(description='Extract content from PDF for AI book processing')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--max-pages', type=int, help='Maximum pages to process (for testing)')
    parser.add_argument('--no-images', action='store_true', help='Skip image extraction')
    parser.add_argument('--output-dir', default='extracted-content', help='Output directory')
    parser.add_argument('--output-file', help='Output filename (optional)')
    
    args = parser.parse_args()
    
    if not Path(args.pdf_path).exists():
        print(f"Error: PDF file not found: {args.pdf_path}")
        return 1
    
    try:
        extractor = PDFExtractor(args.pdf_path, args.output_dir)
        
        # Process the PDF
        data = extractor.process_pdf(
            max_pages=args.max_pages,
            extract_images=not args.no_images
        )
        
        # Save results
        extractor.save_extraction(data, args.output_file)
        
        extractor.close()
        return 0
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())