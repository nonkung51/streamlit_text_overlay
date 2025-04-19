# Text Overlay Positioning Tool

A Streamlit app that helps you position text overlays on images with real-time previews.

## Features

- Upload any image (JPG, JPEG, PNG)
- Add multiple text overlays
- Configure text properties:
  - Text content
  - Position (X, Y coordinates)
  - Font selection
  - Font size
  - Text color
  - Alignment (left, center, right)
- Preview text placement on the image
- Download the final image with text overlays

## Installation

1. Make sure you have Python installed (3.6 or higher)
2. Install the required packages:

```bash
pip install streamlit pillow
```

3. Make sure you have fonts available in a `fonts` directory or use system fonts

## Usage

1. Run the Streamlit app:

```bash
cd text_overlay
streamlit run streamlit_app.py
```

2. Open your browser to the URL shown in the terminal (typically http://localhost:8501)
3. Use the app:
   - Upload an image
   - Add and configure text overlays
   - Preview the result
   - Download the final image

## Tips for Finding Good Text Positions

- Use the X and Y position sliders to move text precisely
- Use the preview button to see how the text looks on the image
- Adjust font size and color for better readability
- Try different alignments (left, center, right) based on text position

## Examples

- Add a title at the top center of the image
- Add captions at specific locations
- Create watermarks or copyright notices
- Add multiple related text elements at different positions 