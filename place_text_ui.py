import streamlit as st
import os
from PIL import Image
import io
from place_text import place_text_on_image, place_text_on_image_object

def main():
    st.title("Text Overlay Positioning Tool")
    st.write("Upload an image and position text overlays interactively")

    # File uploader for image
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        
        # Display image info
        st.write(f"Image dimensions: {image.width} x {image.height}")
        
        # Create a container for texts
        text_entries = []
        
        # Session state to track number of text entries
        if 'num_texts' not in st.session_state:
            st.session_state.num_texts = 1
            
        # Create two columns for layout: preview on left, controls on right
        left_col, right_col = st.columns([3, 2])  # 60% for preview, 40% for controls
        
        # PREVIEW COLUMN (LEFT)
        with left_col:
            # Create a single image display area
            st.subheader("Image Preview")
            image_display = st.empty()
            
            # Show original image initially
            if not st.session_state.get('showing_preview', False):
                image_display.image(image, use_column_width=True)
            
            # Download button placeholder
            download_btn_placeholder = st.empty()
        
        # CONTROLS COLUMN (RIGHT)
        with right_col:
            # Button to add/remove text entries
            st.subheader("Text Controls")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Add Text"):
                    st.session_state.num_texts += 1
                    st.experimental_rerun()
            
            with col2:
                if st.session_state.num_texts > 1 and st.button("Remove Last"):
                    st.session_state.num_texts -= 1
                    st.experimental_rerun()
                    
            with col3:
                # Toggle to show original image
                if st.session_state.get('showing_preview', False):
                    if st.button("Show Original"):
                        st.session_state.showing_preview = False
                        st.experimental_rerun()
            
            # Auto-preview option
            auto_preview = st.checkbox("Auto-preview", value=True)
            
            # Create text configuration UI
            for i in range(st.session_state.num_texts):
                with st.expander(f"Text {i+1}", expanded=(i==0)):
                    text = st.text_input("Text", value=f"Sample Text {i+1}", key=f"text_{i}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        x_pos = st.slider("X Position", 0, image.width, image.width // 2, key=f"x_{i}")
                    with col2:
                        y_pos = st.slider("Y Position", 0, image.height, image.height // 2, key=f"y_{i}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # Find available fonts in the fonts directory
                        default_fonts = ["Mali-Bold.ttf", "Arial.ttf", "Times.ttf"]
                        font_dir = "fonts"
                        available_fonts = default_fonts
                        
                        if os.path.exists(font_dir) and os.path.isdir(font_dir):
                            try:
                                # List font files from the fonts directory
                                font_files = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
                                if font_files:
                                    available_fonts = font_files
                            except Exception:
                                pass
                        
                        font_name = st.selectbox("Font", available_fonts, key=f"font_{i}")
                    
                    with col2:
                        font_size = st.slider("Font Size", 10, 500, 50, key=f"size_{i}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        alignment = st.selectbox("Alignment", ["left", "center", "right"], index=1, key=f"align_{i}")
                    
                    with col2:
                        font_color = st.color_picker("Color", "#3C4658", key=f"color_{i}")
                    
                    # Add this text configuration to our list
                    text_entries.append((text, (x_pos, y_pos), font_name, font_size, font_color, alignment))
            
            # Add a button to copy position data as code
            if st.button("Copy as Code"):
                code_snippet = "[\n"
                for entry in text_entries:
                    code_snippet += f"    {str(entry)},\n"
                code_snippet += "]"
                st.code(code_snippet, language="python")
                st.success("Copy the code above to use in your script")
            
            # Manual preview button (in case auto-preview is off)
            if not auto_preview and st.button("Preview Text Placement"):
                st.session_state.trigger_preview = True
        
        # Logic for preview (outside of columns to avoid redraw issues)
        trigger_preview = auto_preview or st.session_state.get('trigger_preview', False)
        
        if trigger_preview and text_entries:
            # Apply text overlay directly with the in-memory function
            try:
                # Use the in-memory version for faster previews
                result_image = place_text_on_image_object(image, text_entries)
                
                # Display the result in the placeholder
                with left_col:
                    image_display.image(result_image, use_column_width=True)
                    
                    # Create a download button for the result
                    buf = io.BytesIO()
                    result_image.save(buf, format='PNG')
                    download_btn_placeholder.download_button(
                        label="Download Result",
                        data=buf.getvalue(),
                        file_name="text_overlay_result.png",
                        mime="image/png"
                    )
                
                # Mark that we're showing the preview
                st.session_state.showing_preview = True
                
                # Reset trigger if it was manual
                if not auto_preview:
                    st.session_state.trigger_preview = False
                    
            except Exception as e:
                with left_col:
                    st.error(f"Error generating preview: {str(e)}")

if __name__ == "__main__":
    main()