import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import os
import numpy as np
from scipy.signal import find_peaks
import subprocess
import matplotlib.pyplot as plt
from pathlib import Path

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Ensure temp directories exist
Path("temp").mkdir(exist_ok=True)

# App Title
st.set_page_config(page_title="Jump Analysis", layout="wide")
st.title("Jump Analysis with Visual Overlays and Jump Classification")
st.write("Upload a video to see pose keypoints, connections, and jump analysis.")

# Video Upload Section
uploaded_file = st.file_uploader("Upload a Video", type=["mp4", "mov"])

if uploaded_file:
    try:
        # Save uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4", dir="temp") as temp_file:
            temp_file.write(uploaded_file.read())
            video_path = temp_file.name

        st.success("Video uploaded successfully!")

        # Load the video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            st.error("Error opening video file")
            raise ValueError("Could not open video file")

        # Prepare to save frames
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration_minutes = total_frames / (fps * 60)

        # Create temporary directory for frames
        frames_dir = tempfile.mkdtemp(dir="temp")

        # Rest of your existing video processing code remains the same
        # ... [Previous code for processing frames]

        # Cleanup
        try:
            os.remove(video_path)
            for frame_file in os.listdir(frames_dir):
                os.remove(os.path.join(frames_dir, frame_file))
            os.rmdir(frames_dir)
        except Exception as e:
            st.warning(f"Cleanup warning: {str(e)}")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        # Attempt cleanup on error
        if 'video_path' in locals():
            try:
                os.remove(video_path)
            except:
                pass
        if 'frames_dir' in locals():
            try:
                for frame_file in os.listdir(frames_dir):
                    os.remove(os.path.join(frames_dir, frame_file))
                os.rmdir(frames_dir)
            except:
                pass

else:
    st.warning("Please upload a video.")

# Port configuration for Cloud Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    st.server.address = "0.0.0.0"
    st.server.port = port
