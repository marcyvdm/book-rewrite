import os
import json

def check_extra_images():
    """Check which are the 15 extra images and why they don't have JSON references."""
    
    images_dir = r"C:\Users\Marcy\Documents\Coding\book-rewrite\fresh_start\images"
    json_dir = r"C:\Users\Marcy\Documents\Coding\book-rewrite\fresh_start"
    
    # Get all image files
    all_images = set(os.listdir(images_dir))
    
    # Get all JSON references
    json_refs = set()
    for chapter_file in os.listdir(json_dir):
        if chapter_file.startswith('chapter_') and chapter_file.endswith('.json'):
            try:
                with open(os.path.join(json_dir, chapter_file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for item in data.get('content', []):
                    if item.get('type') == 'image':
                        json_refs.add(item['src'])
            except:
                pass
    
    # Find extra images
    extra_images = all_images - json_refs
    
    print(f"Total images: {len(all_images)}")
    print(f"JSON references: {len(json_refs)}")
    print(f"Extra images (no JSON ref): {len(extra_images)}")
    
    print("\nAll extra images:")
    for img in sorted(extra_images):
        print(f"  {img}")
    
    # Convert to page numbers to understand what they are
    print("\nExtra images by book page number:")
    extra_pages = []
    for img in extra_images:
        page_str = img.replace('.png', '').replace('a', '').replace('b', '').replace('c', '')
        if page_str.isdigit():
            extra_pages.append(int(page_str))
    
    for page in sorted(extra_pages):
        print(f"  Book page {page}")
    
    return len(extra_images)

if __name__ == "__main__":
    check_extra_images()