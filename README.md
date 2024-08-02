# ASCII Art Generator

This Python script converts images into ASCII art, with optional edge detection. It allows for customization of various parameters such as pixel size, edge detection settings, and character colors.

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.

2. Clone this repository or download the `ascii_art_generator.py` file.

3. Install the required dependencies using pip:

```
pip install numpy Pillow opencv-python
```

## Usage

Run the script from the command line with the following syntax:

```
python ascii_art_generator.py <input_image_path> [options]
```

### Required Arguments:

- `<input_image_path>`: Path to the input image file

### Optional Arguments:

- `--pixel_size`: Size of each ASCII character (default: 8)
- `--save_location_path`: Path to save the output image (default: "ascii_art_output.png")
- `--sigma1`: Sigma value for first Gaussian blur (default: 0.5)
- `--sigma2`: Sigma value for second Gaussian blur (default: 1.0)
- `--edge_detection`: Enable edge detection (flag, no value required)
- `--edge_threshold`: Threshold for edge detection (default: 5200)
- `--font_type`: Font type for ASCII characters (default: "Courier_New.ttf")
- `--character_fill`: Color to fill characters (format: R,G,B)
- `--background_color`: Background color (format: R,G,B,A, default: 3,46,58,255)

## Examples

1. Basic usage with default settings:
   ```
   python ascii_art_generator.py input.jpg
   ```

2. Custom pixel size and output location:
   ```
   python ascii_art_generator.py input.jpg --pixel_size 10 --save_location_path output.png
   ```

3. Enable edge detection with custom threshold:
   ```
   python ascii_art_generator.py input.jpg --edge_detection --edge_threshold 5000
   ```

4. Custom character fill color (white) and background color (black):
   ```
   python ascii_art_generator.py input.jpg --character_fill 255,255,255 --background_color 0,0,0,255
   ```

5. Combining multiple options:
   ```
   python ascii_art_generator.py input.jpg --pixel_size 12 --edge_detection --sigma1 1.0 --sigma2 2.0 --character_fill 0,255,0 --save_location_path green_edges.png
   ```

## Notes

- The script requires the Pillow, NumPy, and OpenCV libraries. Make sure they are installed using the pip command provided in the installation section.
- If the specified font is not found, the script will fall back to the default system font.
- Edge detection is computationally intensive and may increase processing time, especially for larger images.
- Experiment with different parameters to achieve the desired ASCII art effect.

## Troubleshooting

- If you encounter a "module not found" error, ensure you've installed all required dependencies using pip.
- For issues with font rendering, try specifying a different font using the `--font_type` argument or ensure the default font path is correct for your system.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or bug fixes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
