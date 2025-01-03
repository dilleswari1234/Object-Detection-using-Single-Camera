---

# Object Detection using Single Camera

This project implements object detection using a single camera with pre-trained models. The application is built with Streamlit for easy interaction and OpenCV for image processing.

## Requirements

Make sure you have [Anaconda](https://www.anaconda.com/) or [Python 3.x](https://www.python.org/) installed.

### Install Dependencies

To install the necessary dependencies, use:

```bash
pip install opencv-python-headless streamlit
```

## How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/dilleswari1234/Object-Detection-using-Single-Camera.git
   cd Object-Detection-using-Single-Camera
   ```

2. Run the application using Streamlit:

   ```bash
   streamlit run app.py
   ```

3. The application will launch in your default web browser. You can use images and videos to detect objects by uploading them directly into the application.

## Pre-trained Models

Two pre-trained models are included in this project for object detection. Make sure they are in the correct directory specified in `app.py`.

- **Model 1:** `yolov4-tiny.cfg`
- **Model 2:** `yolov4-tiny.weights`

## Project Structure

```
Object-Detection-using-Single-Camera/
├── app.py               # Main application file to run
├── data/                # Folder for images and videos used for detection
├── README.md            # Project documentation
```

- **`app.py`**: This file contains the main application code and initiates the object detection pipeline.
- **`data/`**: Place any images or videos here for testing purposes.

## Using the Application

- **Image Detection**: Upload an image file, and the model will detect objects within the image.
- **Video Detection**: Upload a video file to detect objects in each frame.

## Troubleshooting

- Ensure `opencv-python-headless` and `streamlit` are installed.
- If models are not loading, check the file paths in `app.py`.

---

After running the code, The Interface would look like this:

![Screenshot 2024-10-29 195410](https://github.com/user-attachments/assets/aac01cdf-b4ba-4486-9ccf-4e533239e7c0)

