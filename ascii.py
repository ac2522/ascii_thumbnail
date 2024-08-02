import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import colorsys
import cv2
import math

ascii_render_str = ["@", "#", "N", "$", "2", "1", "?", "!", "a", ".", " "]
ascii_render_str.reverse()
edge_chars = {0: "|", 45: "/", 90: "_", 135: "\\"}

def sobel_edge_detection(image):
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    direction = np.arctan2(sobely, sobelx) * (180 / np.pi) % 180
    return magnitude, direction

def get_dominant_direction(directions):
    counts = {0: 0, 45: 0, 90: 0, 135: 0}
    for angle in directions.flatten():
        closest_key = min(counts.keys(), key=lambda k: abs(k - angle))
        counts[closest_key] += 1
    return max(counts, key=counts.get)

def generate_ascii_art(ascii_render_str, image_path, pixel_size=8, sigma1=0.5, sigma2=1.0, 
                       edge_detection=False, edge_threshold=5200, font_type="Courier_New.ttf", 
                       character_fill=None, background_color=(3, 46, 58, 255)):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        original_width, original_height = img.size
        new_width = original_width // pixel_size
        new_height = original_height // pixel_size
        img_small = img.resize((new_width, new_height), Image.LANCZOS)
        
        magnitude = direction = None
        if edge_detection:
            cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            blur1 = cv2.GaussianBlur(gray_image, (0, 0), sigmaX=sigma1)
            blur2 = cv2.GaussianBlur(gray_image, (0, 0), sigmaX=sigma2)
            dog = blur1 - blur2
            binary_dog = np.where(dog > 200, 255, 0).astype(np.uint8)
            magnitude, direction = sobel_edge_detection(binary_dog)
        
        ascii_img = Image.new('RGBA', (original_width, original_height), color=background_color)
        draw = ImageDraw.Draw(ascii_img)
        
        try:
            font = ImageFont.truetype(font_type, pixel_size)
        except IOError:
            font = ImageFont.load_default()
        
        for y in range(new_height):
            for x in range(new_width):
                r, g, b = img_small.getpixel((x, y))
                
                if edge_detection:
                    block_magnitude = magnitude[y*pixel_size:(y+1)*pixel_size, x*pixel_size:(x+1)*pixel_size]
                    block_direction = direction[y*pixel_size:(y+1)*pixel_size, x*pixel_size:(x+1)*pixel_size]
                    dominant_direction = get_dominant_direction(block_direction)
                    direction_mask = np.abs(block_direction - dominant_direction) < 22.5
                    mean_magnitude = np.mean(block_magnitude[direction_mask]) if np.any(direction_mask) else 0
                    
                    if mean_magnitude > edge_threshold:
                        char = edge_chars[dominant_direction]
                    else:
                        _, l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
                        char_index = int(l ** 0.6 * (len(ascii_render_str) - 1))
                        char = ascii_render_str[char_index]
                else:
                    _, l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
                    char_index = int(l ** 0.6 * (len(ascii_render_str) - 1))
                    char = ascii_render_str[char_index]
                
                if int(r+g+b) != 0:
                    fill = character_fill if character_fill else (int(r), int(g), int(b))
                    draw.text((x*pixel_size, y*pixel_size), char, font=font, fill=fill)
        
        return ascii_img

def main():
    parser = argparse.ArgumentParser(description="Generate ASCII art from an image.")
    parser.add_argument("file_path", help="Path to the input image file")
    parser.add_argument("--pixel_size", type=int, default=8, help="Size of each ASCII character")
    parser.add_argument("--save_location_path", default="ascii_art_output.png", help="Path to save the output image")
    parser.add_argument("--sigma1", type=float, default=0.5, help="Sigma value for first Gaussian blur")
    parser.add_argument("--sigma2", type=float, default=1.0, help="Sigma value for second Gaussian blur")
    parser.add_argument("--edge_detection", action="store_true", help="Enable edge detection")
    parser.add_argument("--edge_threshold", type=float, default=5200, help="Threshold for edge detection")
    parser.add_argument("--font_type", default="Courier_New.ttf", help="Font type for ASCII characters")
    parser.add_argument("--character_fill", help="Color to fill characters (R,G,B)")
    parser.add_argument("--background_color", default="3,46,58,255", help="Background color (R,G,B,A)")

    args = parser.parse_args()

    character_fill = None
    if args.character_fill:
        character_fill = tuple(map(int, args.character_fill.split(',')))

    background_color = tuple(map(int, args.background_color.split(',')))

    ascii_image = generate_ascii_art(
        ascii_render_str,
        args.file_path,
        pixel_size=args.pixel_size,
        sigma1=args.sigma1,
        sigma2=args.sigma2,
        edge_detection=args.edge_detection,
        edge_threshold=args.edge_threshold,
        font_type=args.font_type,
        character_fill=character_fill,
        background_color=background_color
    )
    
    ascii_image.save(args.save_location_path)
    print(f"ASCII art saved to {args.save_location_path}")

if __name__ == "__main__":
    main()
