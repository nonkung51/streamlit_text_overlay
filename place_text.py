from PIL import Image, ImageDraw, ImageFont
import os


def place_text_on_image(
    image_path,
    output_path,
    text,
    position=None,
    font_name=None,
    font_size=None,
    font_color=None,
    align="left",
):
    """
    Place text on an image using Pillow.

    Args:
        image_path (str): Path to the input image
        output_path (str): Path to save the output image
        text (str or list): Text to place on the image or a list of tuples in format
                           [(text, position, font_name, font_size, font_color, align), ...] 
                           where each element is optional except text
        position (tuple, optional): (x, y) coordinates for text placement. Defaults to (1397, -1180).
        font_name (str, optional): Font name to use. Defaults to "Mali-Bold.ttf".
        font_size (int, optional): Font size. Defaults to 12.
        font_color (str, optional): Font color in hex. Defaults to "#3C4658".
        align (str, optional): Text alignment. Options: "left", "center", "right". Defaults to "left".
    """
    # Open the image
    img = Image.open(image_path)
    
    # Process the image with in-memory function
    result_img = place_text_on_image_object(
        img, text, position, font_name, font_size, font_color, align
    )
    
    # Save the modified image
    result_img.save(output_path)
    
    return output_path


def place_text_on_image_object(
    img,
    text,
    position=None,
    font_name=None,
    font_size=None,
    font_color=None,
    align="left",
):
    """
    Place text on a PIL Image object without file I/O operations.
    Works directly with image objects in memory for better performance.

    Args:
        img (PIL.Image.Image): PIL Image object
        text (str or list): Text to place on the image or a list of tuples
        position, font_name, font_size, font_color, align: Same as place_text_on_image
        
    Returns:
        PIL.Image.Image: Modified image with text overlays
    """
    # Create a copy of the image to avoid modifying the original
    img = img.copy()
    
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    
    # Default values
    default_position = (1397, -1180)
    default_font_name = "Mali-Bold.ttf"
    default_font_size = 12
    default_font_color = "#3C4658"
    default_align = "left"
    
    # Check if text is a list of tuples (new format)
    if isinstance(text, list) and text and isinstance(text[0], (tuple, list)):
        # Process each text entry from the array of tuples
        for entry in text:
            # Unpack the tuple with defaults for missing values
            current_text = entry[0]  # Text is required
            current_position = entry[1] if len(entry) > 1 and entry[1] is not None else default_position
            current_font_name = entry[2] if len(entry) > 2 and entry[2] is not None else default_font_name
            current_font_size = entry[3] if len(entry) > 3 and entry[3] is not None else default_font_size
            current_font_color = entry[4] if len(entry) > 4 and entry[4] is not None else default_font_color
            current_align = entry[5] if len(entry) > 5 and entry[5] is not None else default_align
            
            # Process and draw this text
            _draw_text(draw, current_text, current_position, current_font_name, 
                      current_font_size, current_font_color, current_align)
    else:
        # Original behavior for single text
        _draw_text(draw, text, 
                  position if position is not None else default_position,
                  font_name if font_name is not None else default_font_name,
                  font_size if font_size is not None else default_font_size,
                  font_color if font_color is not None else default_font_color,
                  align)
    
    return img


def _draw_text(draw, text, position, font_name, font_size, font_color, align):
    """Helper function to draw a single text on the image"""
    # Load the font
    font_path = (
        os.path.join("fonts", font_name)
        if os.path.exists(os.path.join("fonts", font_name))
        else font_name
    )
    font = ImageFont.truetype(font_path, font_size, layout_engine=0)
    
    # Convert hex color to RGB tuple
    if font_color.startswith("#"):
        font_color = font_color.lstrip("#")
        font_color_rgb = tuple(int(font_color[i : i + 2], 16) for i in (0, 2, 4))
    else:
        font_color_rgb = font_color
    
    # Get text size for alignment
    if hasattr(draw, 'textsize'):
        text_width, text_height = draw.textsize(text, font=font)
    else:
        # In newer Pillow versions, use font.getbbox or getlength
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    
    # Adjust position based on alignment
    x, y = position
    if align == "center":
        x -= text_width // 2
    elif align == "right":
        x -= text_width
    
    # Draw the text on the image
    draw.text((x, y), text, font=font, fill=font_color_rgb)
