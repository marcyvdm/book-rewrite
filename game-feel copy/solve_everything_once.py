import os
import json
import shutil
from collections import defaultdict

def solve_image_mapping_completely():
    """ONE SCRIPT TO SOLVE THE ENTIRE IMAGE MAPPING PROBLEM CORRECTLY"""
    
    # Input directories
    pdf_images_dir = r"C:\Users\Marcy\Documents\Coding\book-rewrite\to-be-processed\game-feel\images_temp"
    backup_json_dir = r"C:\Users\Marcy\Documents\Coding\book-rewrite\to-be-processed copy\game-feel"
    
    # Output directories  
    output_images_dir = r"C:\Users\Marcy\Documents\Coding\book-rewrite\fresh_start\images"
    output_json_dir = r"C:\Users\Marcy\Documents\Coding\book-rewrite\fresh_start"
    
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_json_dir, exist_ok=True)
    
    print("SOLVING IMAGE MAPPING COMPLETELY - ONE SCRIPT TO RULE THEM ALL")
    print("=" * 70)
    
    # STEP 1: ANALYZE ALL EXTRACTED IMAGES
    print("STEP 1: Analyzing extracted images...")
    
    extracted_images = []
    pages_with_images = defaultdict(list)
    
    for filename in os.listdir(pdf_images_dir):
        if filename.startswith('page_'):
            # Parse: page_XXX_img_YY.ext
            parts = filename.split('_')
            pdf_page = int(parts[1])
            img_index = int(parts[3].split('.')[0])
            ext = filename.split('.')[-1]
            
            extracted_images.append((pdf_page, img_index, ext, filename))
            pages_with_images[pdf_page].append((img_index, ext, filename))
    
    # Sort everything properly
    extracted_images.sort()
    for page in pages_with_images:
        pages_with_images[page].sort()
    
    print(f"  Found {len(extracted_images)} extracted images")
    print(f"  Across {len(pages_with_images)} PDF pages")
    
    multi_image_pages = [p for p in pages_with_images if len(pages_with_images[p]) > 1]
    print(f"  Pages with multiple images: {len(multi_image_pages)}")
    
    # STEP 2: CREATE CORRECT IMAGE NAMES
    print("STEP 2: Creating correct image names...")
    
    image_mapping = []  # (old_filename, new_filename, pdf_page, book_page)
    
    for pdf_page in sorted(pages_with_images.keys()):
        images_on_page = pages_with_images[pdf_page]
        book_page = pdf_page + 1  # The +1 offset we determined
        
        if len(images_on_page) == 1:
            # Single image on page
            img_index, ext, old_filename = images_on_page[0]
            new_filename = f"{book_page}.png"
            image_mapping.append((old_filename, new_filename, pdf_page, book_page, None))
        else:
            # Multiple images on page - add suffixes
            suffixes = ['a', 'b', 'c', 'd', 'e']
            for i, (img_index, ext, old_filename) in enumerate(images_on_page):
                suffix = suffixes[i] if i < len(suffixes) else str(i)
                new_filename = f"{book_page}{suffix}.png"
                image_mapping.append((old_filename, new_filename, pdf_page, book_page, suffix))
    
    print(f"  Generated {len(image_mapping)} image name mappings")
    print(f"  Sample mappings:")
    for i in range(min(5, len(image_mapping))):
        old, new, pdf_p, book_p, suffix = image_mapping[i]
        print(f"    {old} -> {new}")
    
    # STEP 3: READ ORIGINAL JSON FILES  
    print("STEP 3: Reading original JSON files...")
    
    original_json_data = {}
    composite_captions = {}  # book_page -> composite_caption
    
    for chapter_file in os.listdir(backup_json_dir):
        if chapter_file.startswith('chapter_') and chapter_file.endswith('.json'):
            try:
                with open(os.path.join(backup_json_dir, chapter_file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                original_json_data[chapter_file] = data
                
                # Find composite captions
                for item in data.get('content', []):
                    if item.get('type') == 'image' and 'caption' in item:
                        src = item['src']
                        caption = item['caption']
                        if '\nFIGURE' in caption:
                            book_page = int(src.replace('.png', ''))
                            composite_captions[book_page] = caption
                            
            except Exception as e:
                print(f"  ERROR reading {chapter_file}: {e}")
    
    print(f"  Read {len(original_json_data)} JSON files")
    print(f"  Found {len(composite_captions)} composite captions")
    
    # STEP 4: DETERMINE SPLIT REQUIREMENTS
    print("STEP 4: Determining which figures need splitting...")
    
    # Create mapping: book_page -> number_of_images
    book_page_counts = defaultdict(int)
    for old_filename, new_filename, pdf_page, book_page, suffix in image_mapping:
        book_page_counts[book_page] += 1
    
    figures_to_split = {bp: count for bp, count in book_page_counts.items() if count > 1}
    print(f"  Figures that need splitting: {len(figures_to_split)}")
    
    # STEP 5: UPDATE JSON FILES
    print("STEP 5: Creating updated JSON files...")
    
    final_json_refs = set()
    
    for chapter_file, data in original_json_data.items():
        new_content = []
        
        for item in data.get('content', []):
            if item.get('type') == 'image' and 'src' in item:
                src = item['src']
                book_page = int(src.replace('.png', ''))
                
                if book_page in figures_to_split:
                    # This figure needs to be split into multiple entries
                    count = figures_to_split[book_page]
                    original_caption = item.get('caption', '')
                    
                    # Split caption if composite
                    if book_page in composite_captions:
                        caption_parts = composite_captions[book_page].split('\nFIGURE')
                    else:
                        caption_parts = [original_caption]
                    
                    # Create entries for each split image
                    suffixes = ['a', 'b', 'c', 'd', 'e']
                    for i in range(count):
                        new_item = item.copy()
                        suffix = suffixes[i] if i < len(suffixes) else str(i)
                        new_item['src'] = f"{book_page}{suffix}.png"
                        
                        # Assign appropriate caption part
                        if i == 0 and len(caption_parts) > 0:
                            new_item['caption'] = caption_parts[0].strip()
                        elif i < len(caption_parts):
                            new_item['caption'] = f"FIGURE{caption_parts[i].strip()}"
                        else:
                            new_item['caption'] = f"[Part {suffix} of Figure {book_page}]"
                        
                        new_content.append(new_item)
                        final_json_refs.add(new_item['src'])
                else:
                    # Single image - keep as is
                    new_content.append(item)
                    final_json_refs.add(item['src'])
            else:
                # Non-image content
                new_content.append(item)
        
        # Save updated JSON file
        data['content'] = new_content
        output_path = os.path.join(output_json_dir, chapter_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  Created {len(final_json_refs)} JSON image references")
    
    # STEP 6: COPY IMAGES WITH CORRECT NAMES
    print("STEP 6: Copying images with correct names...")
    
    final_image_names = set()
    
    for old_filename, new_filename, pdf_page, book_page, suffix in image_mapping:
        old_path = os.path.join(pdf_images_dir, old_filename)
        new_path = os.path.join(output_images_dir, new_filename)
        
        try:
            shutil.copy2(old_path, new_path)
            final_image_names.add(new_filename)
        except Exception as e:
            print(f"  ERROR copying {old_filename}: {e}")
    
    print(f"  Copied {len(final_image_names)} images")
    
    # STEP 7: VERIFY PERFECT MATCH
    print("STEP 7: Final verification...")
    
    matched = len(final_json_refs & final_image_names)
    missing_images = final_json_refs - final_image_names
    extra_images = final_image_names - final_json_refs
    
    print(f"  JSON references: {len(final_json_refs)}")
    print(f"  Image files: {len(final_image_names)}")
    print(f"  Perfect matches: {matched}")
    
    if len(missing_images) > 0:
        print(f"  Missing images: {len(missing_images)}")
        print(f"    {sorted(list(missing_images))[:5]}")
    
    if len(extra_images) > 0:
        print(f"  Extra images: {len(extra_images)}")
        print(f"    {sorted(list(extra_images))[:5]}")
    
    success = (matched == len(final_json_refs) == len(final_image_names))
    
    if success:
        print("  PERFECT 100% MATCH!")
        print("  IMAGE MAPPING PROBLEM COMPLETELY SOLVED!")
    else:
        print("  MISMATCH - NEED TO FIX")
    
    return success, len(final_image_names), len(final_json_refs)

if __name__ == "__main__":
    print("Starting fresh solution...")
    success, images, refs = solve_image_mapping_completely()
    
    if success:
        print(f"\nSUCCESS: {images} images perfectly match {refs} JSON references")
        print("All files are in fresh_start directory")
    else:
        print(f"\nFAILED: {images} images vs {refs} JSON references")