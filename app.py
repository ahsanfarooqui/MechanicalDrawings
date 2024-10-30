import base64
import json
import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to encode the image
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# Function to create the request and parse the response
def extract_drawing_information(image_bytes):
    # Encode the image to base64
    base64_image = encode_image(image_bytes)
    
    # Construct the chat message
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please analyze the attached mechanical engineering drawing and extract key information in a table format (Markdown) and as JSON."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ],
            }
        ],
    )
    
    # Extract and return the result
    return response.choices[0]

# Streamlit interface
st.title("Mechanical Drawing Analyzer")

# Upload image file
uploaded_file = st.file_uploader("Upload an image of the mechanical drawing", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded file to bytes
    image_bytes = uploaded_file.read()
    
    # Display the uploaded image
    st.image(image_bytes, caption="Uploaded Image", use_column_width=True)
    
    # Extract information from the image
    with st.spinner("Extracting information..."):
        extracted_info = extract_drawing_information(image_bytes)
    
    # Display the extracted Markdown table and JSON
    st.markdown("### Extracted Information (Markdown Table)")
    st.markdown(extracted_info)
    
    # Attempt to display JSON data separately if available
    try:
        json_start = extracted_info.index('{')
        json_end = extracted_info.rindex('}') + 1
        json_data = json.loads(extracted_info[json_start:json_end])
        st.json(json_data)
    except (ValueError, json.JSONDecodeError):
        st.write("JSON data could not be extracted from the response.")
