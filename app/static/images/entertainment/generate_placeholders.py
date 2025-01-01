from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(size, text, filename, bg_color=(30, 30, 30), text_color=(255, 255, 255)):
    # Create image with background
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except:
        font = ImageFont.load_default()
    
    # Center text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_position = ((size[0] - text_bbox[2]) / 2, (size[1] - text_bbox[3]) / 2)
    
    # Draw text
    draw.text(text_position, text, font=font, fill=text_color)
    
    # Save image
    image.save(filename)

# Create placeholder images
placeholders = {
    'streams/live-event.jpg': ((800, 450), 'Live Event'),
    'streams/stream1.jpg': ((640, 360), 'Gaming Stream'),
    'avatars/avatar1.jpg': ((100, 100), 'Streamer'),
    'games/game1.jpg': ((300, 400), 'Game Cover'),
    'sports/team1.png': ((64, 64), 'Team 1'),
    'sports/team2.png': ((64, 64), 'Team 2'),
    'services/netflix.png': ((200, 100), 'Streaming'),
    'promos/promo1.jpg': ((600, 300), 'Promotion')
}

base_path = os.path.dirname(os.path.abspath(__file__))

for path, (size, text) in placeholders.items():
    full_path = os.path.join(base_path, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    create_placeholder(size, text, full_path) 