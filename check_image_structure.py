import json
import pprint

# Load the extracted data
with open('to-be-processed/game-feel.simple.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ch = data['chapters'][0]
images = [item for item in ch['content'] if item['type'] == 'image']

print('Enhanced image structure:')
if images:
    # Show structure without the full base64 data
    img = {k: v for k, v in images[0].items() if k != 'data'}
    if images[0]['data']:
        img['data_preview'] = images[0]['data'][:50] + '...(base64 continues)'
        img['has_actual_data'] = True
    else:
        img['data_preview'] = None
        img['has_actual_data'] = False
    
    pprint.pprint(img)
    
    print(f"\nImages with actual data: {sum(1 for img in images if img['data'])}")
    print(f"Images with captions: {sum(1 for img in images if img.get('caption'))}")
    
    # Show any captions found
    for i, img in enumerate(images[:5]):
        if img.get('caption'):
            print(f"Image {i+1} caption: {img['caption']}")
else:
    print("No images found")