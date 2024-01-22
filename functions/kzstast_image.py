import requests
from PIL import Image, ImageDraw, ImageFont


def get_player_stats(steam_id):
    # Replace with the actual URL you need to query
    url = f"https://kzgo.eu/players/{steam_id}?kzt"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()  # Or the appropriate parsing method for the site's response
        return data
    else:
        # Handle errors or non-200 responses here
        return None


def create_stats_image(stats_data):
    # Load a base image template or create a new one with PIL
    base_image = Image.new('RGBA', (768, 912), 'black')
    draw = ImageDraw.Draw(base_image)

    # Define fonts, colors, and positions for your stats
    font = ImageFont.truetype('arial.ttf', 24)  # You'll need an actual font file path

    # Draw the stats onto the base image
    # Example: draw.text((x, y), stats_data['username'], fill='white', font=font)

    # Save or return the generated image
    image_path = '/path/to/output/stats_image.png'
    base_image.save(image_path)
    return image_path


# Example usage
steam_id = 'STEAM_1:0:182656610'
player_stats = get_player_stats(steam_id)
if player_stats:
    image_path = create_stats_image(player_stats)
    # Now you can send this image via your Discord bot or save it etc.
