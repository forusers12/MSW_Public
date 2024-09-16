import os
from PIL import Image, ImageEnhance
import numpy as np

# Folder where the images are stored
image_folder = "loader path"
output_folder = "output path"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)


# Function to apply a more subtle color tint by blending with the original
def blend_tint_image(img, color, intensity=0.3):
    img_array = np.array(img)
    r, g, b, a = img_array.T  # Separate color and alpha channels

    # Blend the new color with the original color, moderated by 'intensity'
    non_transparent = a > 0
    img_array[..., 0][non_transparent.T] = (1 - intensity) * img_array[..., 0][non_transparent.T] + intensity * color[0]
    img_array[..., 1][non_transparent.T] = (1 - intensity) * img_array[..., 1][non_transparent.T] + intensity * color[1]
    img_array[..., 2][non_transparent.T] = (1 - intensity) * img_array[..., 2][non_transparent.T] + intensity * color[2]

    return Image.fromarray(img_array)


# Function to adjust brightness or contrast with smaller changes
def moderate_brightness_contrast(img, factor, mode='brightness'):
    enhancer = ImageEnhance.Brightness(img) if mode == 'brightness' else ImageEnhance.Contrast(img)
    moderate_factor = 1 + (factor - 1) * 0.5  # Scaling down the intensity
    return enhancer.enhance(moderate_factor)


# Colors for subtle tinting (blended)
colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 0, 0),  # Maroon
    (0, 128, 0),  # Dark Green
    (0, 0, 128),  # Navy
    (128, 128, 0),  # Olive
    (128, 0, 128),  # Purple
    (0, 128, 128),  # Teal
    (192, 192, 192),  # Silver
    (128, 128, 128),  # Gray
    (255, 165, 0),  # Orange
    (75, 0, 130),  # Indigo
    (199, 21, 133),  # Medium Violet Red
    (0, 100, 0),  # Dark Green
    (210, 105, 30),  # Chocolate
    (0, 191, 255),  # Deep Sky Blue
    (123, 104, 238),  # Medium Slate Blue
    (255, 20, 147),  # Deep Pink
    (173, 216, 230),  # Light Blue
    (72, 61, 139),  # Dark Slate Blue
    (240, 128, 128),  # Light Coral
    (220, 20, 60),  # Crimson
    (0, 206, 209),  # Dark Turquoise
    (255, 105, 180),  # Hot Pink
    (255, 218, 185),  # Peach Puff
    (0, 139, 139),  # Dark Cyan
    (64, 224, 208),  # Turquoise
    (50, 205, 50),  # Lime Green
    (144, 238, 144),  # Light Green
    (218, 112, 214),  # Orchid
    (139, 69, 19),  # Saddle Brown
    (255, 192, 203),  # Pink
    (245, 245, 220),  # Beige
    (0, 250, 154),  # Medium Spring Green
    (186, 85, 211),  # Medium Orchid
    (255, 228, 181),  # Moccasin
]

# Moderated brightness/contrast factors
# factors = [0.9, 1.1, 1.2, 0.95, 1.05]
factors = [0.95, 1.05, 1.1, 0.98, 1.02]  # Closer to 1 for more subtle changes

# Loop through all PNG files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        img_path = os.path.join(image_folder, filename)
        img = Image.open(img_path).convert("RGBA")
        base_filename = os.path.splitext(filename)[0]  # Get the filename without extension

        # Apply 40 different color tints with moderation
        for i, color in enumerate(colors):
            tinted_img = blend_tint_image(img, color, intensity=0.5)  # Set intensity to blend colors subtly
            tinted_img.save(os.path.join(output_folder, f"{base_filename}_tint_{i + 1}.png"), "PNG")

        # Apply 5 different brightness/contrast adjustments, with moderation
        for i, factor in enumerate(factors):
            mode = 'brightness' if i % 2 == 0 else 'contrast'
            adjusted_img = moderate_brightness_contrast(img, factor, mode)
            adjusted_img.save(os.path.join(output_folder, f"{base_filename}_adjusted_{i + 1}.png"), "PNG")

print("All images have been moderately processed and saved.")