# Background Remover App

A Streamlit-based application for background removal from images. The app allows you to upload multiple images, choose a background removal model, and process the images in parallel. It also provides an interactive image comparison slider and options to download individual images or all processed images as a ZIP file.

## Features

- **Multiple Model Support**: Choose from a variety of background removal models tailored for different use cases:
  - General-purpose models (`u2net`, `isnet-general-use`)
  - Human segmentation (`u2net_human_seg`)
  - Cloth segmentation (`u2net_cloth_seg`)
  - Anime-style images (`isnet-anime`)
  - Advanced segmentation (`sam`, `birefnet-general`, etc.)
- **Batch Processing**: Upload multiple images and process them concurrently for efficiency.
- **Interactive Image Comparison**: Compare original and processed images side-by-side with a slider.
- **Download Options**: Download individual images or all processed images as a ZIP file.
- **Easy Reset**: Clear all selections and uploads with a single button.

## Requirements

- Python 3.8 or higher
- Dependencies:
  - `streamlit`
  - `rembg`
  - `Pillow`
  - `streamlit-image-comparison`
  - `concurrent.futures`

Install the dependencies with:
```bash
pip install streamlit rembg Pillow streamlit-image-comparison
```

## Usage

1. Clone the Repository:

```bash
git clone https://github.com/your-username/background-remover-app.git
cd background-remover-app
```

2. Create a virtual environment and activate it

3. Install dependencies

## Run the Application: 

Start the app with Streamlit:

```bash
streamlit run app.py
```

## Using the App:

Select a background removal model from the dropdown.
Upload one or more images (.jpg, .jpeg, .png).
Click "Process Images" to remove the background.
View and compare the results with an interactive slider.
Download individual processed images or a ZIP file of all results.
Screenshots
Main Interface

Image Comparison

Download Options

## Models
Here are the supported models and their use cases:

| Model Name              | Description                                   |
|-------------------------|-----------------------------------------------|
| `u2net`                 | General-purpose background removal.          |
| `u2netp`                | Lightweight and faster version of `u2net`.   |
| `u2net_human_seg`       | Optimized for human segmentation.            |
| `u2net_cloth_seg`       | Specialized for cloth segmentation.          |
| `silueta`               | Advanced silhouette detection.               |
| `isnet-general-use`     | General-purpose segmentation by ISNet.       |
| `isnet-anime`           | Tailored for anime-style images.             |
| `sam`                   | Segment Anything Model for versatile tasks.  |
| `birefnet-general`      | BirefNet for general segmentation.           |
| `birefnet-general-lite` | Lightweight version for faster processing.   |
| `birefnet-dis`          | Optimized for document images.               |
| `birefnet-hrsod`        | High-resolution BirefNet for SOD tasks.      |
| `birefnet-cod`          | BirefNet for contour detection.              |
| `birefnet-massive`      | Large-scale segmentation tasks.              |

## Contributing
Contributions are welcome! Feel free to fork the repository, make improvements, and submit a pull request.

## License
This project is licensed under the Apache License.

## Happy Background Removing!
