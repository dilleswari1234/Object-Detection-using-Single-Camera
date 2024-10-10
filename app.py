import cv2 as cv
import streamlit as st
import os
from tempfile import NamedTemporaryFile

# Constants
Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Load class names
class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

# Load the YOLOv4-tiny model
net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

# Set the preferred backend and target
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

# Create a DetectionModel
model = cv.dnn_DetectionModel(net)

# Set input parameters
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

def detect_and_draw(model, image, class_name, Conf_threshold=0.4, NMS_threshold=0.4):
    classes, scores, boxes = model.detect(image, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        classid = int(classid)
        color = COLORS[classid % len(COLORS)]
        label = f'{class_name[classid]} : {score: .2f}' 
        cv.rectangle(image, box, color, 2)
        cv.putText(image, label, (box[0], box[1] - 10), cv.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
    return image

def process_image(image_path):
    image = cv.imread(image_path)
    if image is None:
        st.error("Could not read the image")
        return
    
    result_image = detect_and_draw(model, image, class_name)
    st.image(result_image, channels="BGR")

def process_video(video_path):
    cap = cv.VideoCapture(video_path)
    stframe = st.empty()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        result_frame = detect_and_draw(model, frame, class_name)
        stframe.image(result_frame, channels="BGR")
        
    cap.release()

def live_camera():
    cap = cv.VideoCapture(0)  # Change the index if you have multiple cameras
    stframe = st.empty()
    stop_button = st.button("Stop Live Camera", key="stop_live")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame")
            break
        
        result_frame = detect_and_draw(model, frame, class_name)
        stframe.image(result_frame, channels="BGR")
        
        if stop_button:
            break
    
    cap.release()

def record_live_video(save_directory, frame_width, frame_height, fps=10):
    cap = cv.VideoCapture(0)  # Use the live camera
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    output_path = os.path.join(save_directory, 'recorded_live_video.avi')
    out = cv.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    stframe = st.empty()
    stop_button = st.button("Stop Recording", key="stop_record")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to grab frame")
            break
        
        result_frame = detect_and_draw(model, frame, class_name)
        out.write(result_frame)
        stframe.image(result_frame, channels="BGR")
        
        if stop_button:
            break
    
    cap.release()
    out.release()
    return output_path

st.title("Object Detection using Single Camera")

option = st.sidebar.selectbox("Select mode", ["Image", "Video", "Live", "Record Live"])

if option == "Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        tfile = NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        process_image(tfile.name)
elif option == "Video":
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi", "mkv"])
    if uploaded_file is not None:
        tfile = NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        process_video(tfile.name)
elif option == "Live":
    if st.button("Start Live Camera", key="start_live"):
        live_camera()
elif option == "Record Live":
    save_directory = st.text_input("Enter directory to save the video:", value=os.getcwd())
    frame_width = 640 #st.number_input("Enter frame width:", min_value=1, value=640)
    frame_height = 480 #st.number_input("Enter frame height:", min_value=1, value=480)
    if st.button("Start Recording Live Camera", key="start_record_live"):
        recorded_file_path = record_live_video(save_directory, frame_width, frame_height)
        st.success(f"Recording saved to {recorded_file_path}")
        st.video(recorded_file_path)
