import google.generativeai as genai
import streamlit as st
from PIL import Image

genai.configure(api_key=st.secrets['YOUR_API_KEY'])

generation_config = {
  "temperature": 0.5,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 4096,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

st.title('GeoAI 🗺')
st.write('Generate geograpic facts from image and prompt using Gemini AI')

upload = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])

if upload:
    image = Image.open(upload)

    st.image(image, caption='Uploaded Image', use_column_width=True)

    prompt = st.text_input('Enter a prompt', 'Tell me some cool facts about the country where the image is located.')

    sys_prompt = f'You are profficient in geography. You are tasked to do the following: {prompt}. Add some geographic facts about the image above.'

    if st.button('Generate'):
        model = genai.GenerativeModel(model_name='gemini-1.0-pro-vision-latest',
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        response = model.generate_content([sys_prompt, image])

        st.markdown(response.text)
