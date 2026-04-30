import streamlit as st
from PIL import Image
import numpy as np
import io
import tempfile

from api import convert_to_sketch
from utils import opencv_sketch

st.set_page_config(page_title="UrPic Art", layout="wide")

st.title("✏️ UrPic Art")
st.caption("Turn your photos into pencil sketches")

# SIDEBAR
api_key = st.sidebar.text_input("API Key", type="password")
mode = st.sidebar.radio("Mode", ["AI Sketch", "Fast Sketch"])
uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

# SESSION
if "original" not in st.session_state:
    st.session_state.original = None
if "sketch" not in st.session_state:
    st.session_state.sketch = None

# LOAD IMAGE
if uploaded_file:
    st.session_state.original = Image.open(uploaded_file).convert("RGB")

# GENERATE
if st.sidebar.button("Generate"):
    if st.session_state.original is None:
        st.warning("Upload image first")
    else:
        with st.spinner("Processing..."):

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                st.session_state.original.save(tmp.name)
                path = tmp.name

            if mode == "AI Sketch":
                if not api_key:
                    st.error("API key required")
                else:
                    st.session_state.sketch = convert_to_sketch(api_key, path)
            else:
                sketch = opencv_sketch(path)
                st.session_state.sketch = Image.fromarray(sketch)

# DISPLAY
col1, col2 = st.columns(2)

if st.session_state.original:
    col1.image(st.session_state.original, caption="Original")

if st.session_state.sketch:
    col2.image(st.session_state.sketch, caption="Sketch")

# COMPARE
if st.session_state.original and st.session_state.sketch:
    st.subheader("Compare")

    slider = st.slider("Slide", 0.0, 1.0, 0.5)

    orig = st.session_state.original.resize((800, 500))
    sketch = st.session_state.sketch.resize((800, 500))

    orig_np = np.array(orig)
    sketch_np = np.array(sketch)

    split = int(800 * slider)

    combined = orig_np.copy()
    combined[:, split:] = sketch_np[:, split:]

    st.image(combined)

# DOWNLOAD
if st.session_state.sketch:
    buf = io.BytesIO()
    st.session_state.sketch.save(buf, format="PNG")

    st.download_button("Download", buf.getvalue(), "sketch.png")