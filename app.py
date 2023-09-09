import os
from PIL import Image
import streamlit as st
from streamlit import components
from ocr import OCRProcessor
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Setting up OpenAI API Key
os.environ["OPENAI_API_KEY"] = "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"

# Constants
IMAGE_SAMPLE = "img.jpg"
CUSTOM_PROMPT_TEMPLATE = """
You have received a layout sketch for a modern, sans-serif website. The layout sketch includes text and coordinates for the outer vertices of various elements. Your task is to create an HTML representation of this layout. Please adhere to the following guidelines:

1. Reflect the elements from the layout sketch in your design.
2. Utilize CSS to align the elements based on their relative positions in the sketch.
3. Use appropriate HTML tags to represent elements, keeping in mind their font sizes and relative placements.
4. If elements appear to be part of a menu list, use <ul> and <li> tags to represent them.
5. Use functional tags like <button> and <input> where the elements' names suggest such functionality.
6. Prioritize the coordinates when designing, but also employ creativity to enhance the layout based on common web design principles.
7. Avoid using absolute coordinates in your HTML source code.

Note: Your submission should be a source code file only, without any descriptions.

Layout Details: {layout}
"""

def ocr_func(img_path):
    """Function to extract layout information from an image using OCR."""
    ocr_processor = OCRProcessor()
    layout = ocr_processor.extract_layout(img_path)
    return layout

def html_generation(layout):
    """Function to generate HTML code based on the extracted layout information."""
    prompt = PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE, input_variables=["layout"])
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.1, max_tokens=2096)
    chain = LLMChain(prompt=prompt, llm=llm)
    output = chain.run(layout=layout)
    return output

def image_run():
    """Function to run the OCR and HTML generation process with the uploaded image."""
    layout = ocr_func(st.session_state.image)
    if layout:
        st.session_state.html = html_generation(layout)
        st.session_state.image = st.session_state.image

# Streamlit app configuration
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: Blue;'>GenAI WebDesign by Rakib.ai.ds</h1>", unsafe_allow_html=True)

# Initializing session state variables
st.session_state.setdefault("html", "")
st.session_state.setdefault("image", "")

col1, col2 = st.columns([0.5, 0.5], gap='medium')

# Column 1: File uploader and 'Run' button
with col1:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image_filename = uploaded_file.name
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        image = Image.open(uploaded_file)
        image.save(image_filename)
        st.session_state.image = image_filename
        st.button("Run", on_click=image_run)

# Column 2: Display HTML code and preview
with col2:
    if st.session_state.html:
        with st.expander("See source code"):
            st.code(st.session_state.html)
        with st.container():
            components.v1.html(st.session_state.html, height=600, scrolling=True)
