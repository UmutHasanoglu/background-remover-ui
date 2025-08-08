import streamlit as st
from rembg import remove
from rembg.bg import new_session
from io import BytesIO
from PIL import Image
import os
import zipfile
import concurrent.futures
from pathlib import Path
from streamlit_image_comparison import image_comparison  # Ensure this is installed


# --- Initialize Session State Variables ---
# Ensure that all necessary session state variables are initialized
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = []
if 'prev_uploaded_files' not in st.session_state:
    st.session_state.prev_uploaded_files = []
if 'prev_selected_model' not in st.session_state:
    st.session_state.prev_selected_model = ''

# --- Model Descriptions ---
# Dictionary mapping model names to their descriptions
model_descriptions = {
    'u2net': 'General-purpose background removal.',
    'u2netp': 'Lightweight version of u2net for faster processing.',
    'u2net_human_seg': 'Optimized for human segmentation.',
    'u2net_cloth_seg': 'Specialized for cloth segmentation.',
    'silueta': 'Advanced silhouette detection.',
    'isnet-general-use': 'General-purpose segmentation by ISNet.',
    'isnet-anime': 'Tailored for anime-style images.',
    'sam': 'Segment Anything Model for versatile segmentation tasks.',
    'birefnet-general': 'BirefNet for general segmentation.',
    'birefnet-general-lite': 'Lightweight BirefNet for faster processing.',
    'birefnet-dis': 'BirefNet optimized for document images.',
    'birefnet-hrsod': 'High-resolution BirefNet for SOD tasks.',
    'birefnet-cod': 'BirefNet for contour detection.',
    'birefnet-massive': 'Massive BirefNet for large-scale segmentation.'
}

# --- App Title and Description ---
st.title('🖼️ Background Remover App')
st.write('Upload one or more images, select a model, and this app will remove the background from each!')

# --- Model Selection Dropdown with Descriptions ---
st.subheader('1. Select a Model')

selected_model = st.selectbox(
    'Choose a background removal model:',
    options=list(model_descriptions.keys()),
    format_func=lambda x: f"{x} - {model_descriptions[x]}",
    key='selected_model'
)

# Display the description of the selected model
st.markdown(f"**Model Description:** {model_descriptions[selected_model]}")

# --- File Uploader ---
st.subheader('2. Upload Images')

uploaded_files = st.file_uploader(
    "Choose images...",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    key='uploaded_files'
)

# --- Reset Processed Images if Inputs Change ---
if (uploaded_files != st.session_state.prev_uploaded_files) or (selected_model != st.session_state.prev_selected_model):
    st.session_state.processed_images = []
    st.session_state.prev_uploaded_files = uploaded_files
    st.session_state.prev_selected_model = selected_model

# --- Clear All Button ---
if st.button('🧹 Clear All'):
    # Reset session state variables to their initial values
    st.session_state.processed_images = []
    st.session_state.prev_uploaded_files = []
    st.session_state.prev_selected_model = ''
    # Note: We do NOT reset 'uploaded_files' as it's tied to the widget key
    st.success('All images and selections have been cleared.')

# --- Function to Process a Single Image ---
def process_image(uploaded_file, model_name):
    try:
        # Ensure the file pointer is at the start in case the file was read before
        uploaded_file.seek(0)

        # Open the uploaded image
        input_image = Image.open(uploaded_file).convert("RGBA")
        
        # Initialize a new session for the selected model
        session = new_session(model_name=model_name)
        
        # Remove the background
        output_image = remove(input_image, session=session)
        
        # Save processed image to BytesIO
        buffered = BytesIO()
        output_image.save(buffered, format="PNG")
        buffered.seek(0)
        base_name = os.path.splitext(uploaded_file.name)[0]
        return {
            'name': f"{base_name}_no_bg.png",
            'original': input_image,
            'processed': Image.open(buffered),
            'data': buffered.getvalue()
        }
    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {e}")
        return None

# --- Progress Bar Initialization ---
progress_bar = None
progress_text = ''

# --- Processing Button ---
if uploaded_files:
    if st.button('🚀 Process Images'):
        # Check if new files or model are selected
        if (uploaded_files != st.session_state.prev_uploaded_files) or (selected_model != st.session_state.prev_selected_model):
            # Reset processed images
            st.session_state.processed_images = []
            st.session_state.prev_uploaded_files = uploaded_files
            st.session_state.prev_selected_model = selected_model
        
        num_files = len(uploaded_files)
        progress_bar = st.progress(0)
        progress_text = st.empty()
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Start processing images concurrently
            future_to_file = {executor.submit(process_image, file, selected_model): file for file in uploaded_files}
            for idx, future in enumerate(concurrent.futures.as_completed(future_to_file)):
                result = future.result()
                if result:
                    st.session_state.processed_images.append(result)
                # Update progress bar
                progress = (idx + 1) / num_files
                progress_bar.progress(progress)
                progress_text.text(f'Processing {idx + 1} of {num_files} images...')
        
        # Finalize progress bar
        progress_bar.empty()
        progress_text.empty()
        
        st.success('All images have been processed!')
    
    # --- Display Processed Images with Image Comparison Slider ---
    if st.session_state.processed_images:
        st.subheader('3. View and Download Results')
        for img_data in st.session_state.processed_images:
            st.markdown(f"### {img_data['name']}")
            
            # Image Comparison Slider using streamlit-image-comparison
            image_comparison(
                img1=img_data['original'],
                img2=img_data['processed'],
                label1="Original",
                label2="Background Removed",
                width=700
                # Removed 'key' parameter
            )
            
            # Provide a download button for the processed image
            st.download_button(
                label="📥 Download Image",
                data=img_data['data'],
                file_name=img_data['name'],
                mime="image/png"
            )
        
        # --- Create ZIP archive for processed images ---
        st.subheader('4. Download All Images as ZIP')
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for img in st.session_state.processed_images:
                zip_file.writestr(img['name'], img['data'])
        zip_buffer.seek(0)
        
        st.download_button(
            label="📥 Download All as ZIP",
            data=zip_buffer.getvalue(),
            file_name="processed_images.zip",
            mime="application/zip"
        )
        
        st.info('Processing complete. You can now clear the page or upload new images.')
