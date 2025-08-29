import fitz

doc = fitz.open("to-be-processed/game-feel.pdf")

# Check pages with images for potential captions
test_pages = [20, 21, 22, 36, 37]  # Pages we know have images

for page_num in test_pages:
    if page_num < doc.page_count:
        page = doc[page_num]
        text = page.get_text()
        
        print(f"\n=== PAGE {page_num + 1} ===")
        
        # Check for images
        images = page.get_images()
        print(f"Images: {len(images)}")
        
        # Show text split by paragraphs
        paragraphs = text.split('\n\n')
        for i, para in enumerate(paragraphs):
            para = para.replace('\n', ' ').strip()
            if len(para) > 10:
                print(f"Para {i}: {para[:100]}...")

doc.close()