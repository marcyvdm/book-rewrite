import fitz

doc = fitz.open("to-be-processed/game-feel.pdf")

total_images = 0
pages_with_images = []

for page_num in range(min(50, doc.page_count)):  # Check first 50 pages
    page = doc[page_num]
    images = page.get_images()
    if images:
        total_images += len(images)
        pages_with_images.append(page_num + 1)
        print(f"Page {page_num + 1}: {len(images)} images")

print(f"\nTotal images in first 50 pages: {total_images}")
print(f"Pages with images: {pages_with_images[:10]}")

# Also check for drawings/vectors
page = doc[20]  # Check page 21
drawings = page.get_drawings()
if drawings:
    print(f"\nPage 21 has {len(drawings)} vector drawings")

doc.close()