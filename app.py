import streamlit as st
from ultralytics import YOLO
import os
from PIL import Image
import numpy as np
import random
import base64

st.set_page_config(page_title="Tiny Spy AI", layout="centered")


# Set Goku background
def set_goku_background():
    img_path = "assets/Goku_anime_profile.webp"
    if os.path.exists(img_path):
        try:
            with open(img_path, "rb") as f:
                encoded_img = f.read()
            b64 = base64.b64encode(encoded_img).decode()
            st.markdown(f"""
                <style>
                    .stApp {{
                        background-color: #ADD8E6;
                        background-image: url("data:image/webp;base64,{b64}");
                        background-size: 15% auto;
                        background-repeat: no-repeat;
                        background-position: left bottom;
                    }}
                </style>
            """, unsafe_allow_html=True)
        except:
            st.markdown("""
                <style>
                    .stApp {
                        background-color: #ADD8E6;
                    }
                </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                .stApp {
                    background-color: #ADD8E6;
                }
            </style>
        """, unsafe_allow_html=True)


# Set background
set_goku_background()


@st.cache_resource
def load_model():
    model_path = os.path.join("model", "yolov8finetuned.pt")
    if os.path.exists(model_path):
        return YOLO(model_path)
    else:
        return YOLO("yolov8n.pt")


# Simple list of common objects
ITEMS = ['phone', 'laptop', 'cup', 'book', 'mouse', 'keyboard', 'bottle', 'apple', 'chair', 'pen']

# Load model
model = load_model()

# Initialize game state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target' not in st.session_state:
    st.session_state.target = random.choice(ITEMS)

# Title
st.title("🕵️ Tiny Spy AI")

# Score
st.markdown(f"### Score: {st.session_state.score}")

# Target
st.markdown(f"### 🎯 Find: **{st.session_state.target.upper()}**")

# Camera
photo = st.camera_input("📸 Take a photo!")

if photo:
    # Process image
    image = Image.open(photo)
    img_array = np.array(image)

    # Run detection
    results = model(img_array, conf=0.5)

    # Show image with detections
    annotated_img = results[0].plot()
    st.image(annotated_img)

    # Check if target found
    found = False
    detected = []

    if results[0].boxes is not None:
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            if hasattr(model, 'names'):
                class_name = model.names[class_id]
            else:
                class_name = f"object_{class_id}"

            detected.append(class_name)

            if st.session_state.target.lower() in class_name.lower():
                found = True

    # Show what was detected
    if detected:
        st.info(f"Found: {', '.join(detected)}")

    # Score and next target
    if found:
        st.success(f"✅ Great! You found the {st.session_state.target}!")
        st.session_state.score += 1
        st.session_state.target = random.choice(ITEMS)
        st.balloons()
        st.rerun()
    else:
        st.warning(f"❌ Keep looking for: {st.session_state.target}")

# Reset button
if st.button("🔄 Reset Game"):
    st.session_state.score = 0
    st.session_state.target = random.choice(ITEMS)
    st.rerun()
