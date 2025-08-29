#!/usr/bin/env python3
"""
Extract images from the JSON to separate files for AI analysis
"""

import json
import base64
from pathlib import Path

def extract_images_to_files(json_path: str, output_dir: str = "extracted_images"):
    """Extract images from JSON to separate PNG files"""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    extracted_count = 0
    total_size = 0
    
    # Process each chapter
    for ch_idx, chapter in enumerate(data['chapters']):
        chapter_dir = output_path / f"chapter_{ch_idx + 1:02d}"
        chapter_dir.mkdir(exist_ok=True)
        
        # Find images in chapter content
        for item in chapter['content']:
            if item['type'] == 'image' and item.get('data'):
                try:
                    # Decode base64 image data
                    image_data = base64.b64decode(item['data'])
                    
                    # Create filename
                    image_filename = f"{item['id']}.png"
                    image_path = chapter_dir / image_filename
                    
                    # Save image
                    with open(image_path, 'wb') as img_file:
                        img_file.write(image_data)
                    
                    # Create metadata file
                    metadata = {
                        "id": item['id'],
                        "page": item['page'],
                        "description": item['description'],
                        "caption": item.get('caption'),
                        "position": item['position'],
                        "actual_size": item['actual_size'],
                        "format": item['format'],
                        "size_bytes": len(image_data),
                        "chapter": chapter['title'],
                        "chapter_page_range": f"{chapter['page_start']}-{chapter['page_end']}"
                    }
                    
                    metadata_path = chapter_dir / f"{item['id']}_metadata.json"
                    with open(metadata_path, 'w', encoding='utf-8') as meta_file:
                        json.dump(metadata, meta_file, indent=2, ensure_ascii=False)
                    
                    extracted_count += 1
                    total_size += len(image_data)
                    
                    print(f"Extracted: {image_filename} ({len(image_data):,} bytes)")
                    
                except Exception as e:
                    print(f"Failed to extract {item.get('id', 'unknown')}: {e}")
    
    print(f"\nExtraction complete!")
    print(f"Images extracted: {extracted_count}")
    print(f"Total size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
    print(f"Output directory: {output_path.absolute()}")
    
    return extracted_count

if __name__ == "__main__":
    import sys
    
    json_file = "to-be-processed/game-feel.simple.json"
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    
    if not Path(json_file).exists():
        print(f"File not found: {json_file}")
        sys.exit(1)
    
    extract_images_to_files(json_file)