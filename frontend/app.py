import streamlit as st
import requests
import whisper
import pytesseract as tess
from PIL import Image
tess.pytesseract.tesseract_cmd=r'C:\Users\siva\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
import os
backend_url = "https://3aed-34-16-171-255.ngrok-free.app/predict_sentiment" 
backend_url2="https://3aed-34-16-171-255.ngrok-free.app/recommendations"
# Streamlit app
st.title("Provide Inputs:")

# Sidebar content with increased font size for the header
st.sidebar.markdown("<h2 style='color:blue;'>Enhancement of sales and decision making<br>through the utilization of GEN AI</h2>", unsafe_allow_html=True)

# Select input type
option = st.selectbox('Select your input type:', ["Text", "Audio","Image"])
department_name = st.selectbox("Enter product department:",["Tops","Bottoms","Jackets","Intimate","Dresses"])
class_name = st.selectbox("Enter product class:", ["Knits","Jeans","Skirts","Pants","Blouses","Outwear","Shorts","Swim","Lounge"])

# Function to handle text input
def handle_text_input():
    user_input = st.text_input("Enter your review:", "")
    return user_input

# Function to handle audio input
def handle_audio_input():
    uploaded_audio = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])
    if uploaded_audio is not None:
        st.audio(uploaded_audio, format="audio/*")
        return uploaded_audio

def handle_image_input():
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        return uploaded_image

def calculated_sentiment(payload):
        try:
            response = requests.post(backend_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Sentiment Score: {result['sentiment_score']}, Sentiment Class: {result['sentiment_class']}")
            else:
                st.error(f"Failed to send data. Status code: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Error sending data to the backend: {e}")
        return result['sentiment_class']

def calculated_recommendations(payload):
        custom=f"{department_name},{class_name},{data},{senti_class}."
        payload={'data':custom}
        try:
            response=requests.post(backend_url2,json=payload)
            if response.status_code==200:
                result2=response.json()
                st.info(result2['recommendations'])
            else:
                st.error(f"Failed to send data. Status code: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Error sending data to the backend: {e}")

# Handle input based on the selected option
if option == "Text":
    data= handle_text_input()
elif option == "Image":
    data= handle_image_input()
elif option == "Audio":
    data= handle_audio_input()

# Button to trigger sending data to the backend
if st.button("Send"):
    if option =="Text":
        payload = {'data': data}
        senti_class=calculated_sentiment(payload)
        calculated_recommendations(payload)


    elif option=="Audio":
        def save_uploaded_file(uploaded_file,save_location,save_name):
            file_path=os.path.join(save_location,save_name)
            with open(file_path, 'wb') as file:
                file.write(uploaded_file.read())
            return file_path
        
        save_location="./backend/uploads"
        os.makedirs(save_location,exist_ok=True)
        save_name="saved_audio.mp3"
        uploaded_audio=data
        if uploaded_audio is not None:
            saved_file_path=save_uploaded_file(uploaded_audio,save_location,save_name)
            st.success(f"Audio file save to: {saved_file_path}")
        model=whisper.load_model("base")
        result=model.transcribe('./backend/uploads/saved_audio.mp3')
        data=result['text']

        payload = {'data': data}
        senti_class=calculated_sentiment(payload)
        calculated_recommendations(payload)
        
    elif option=="Image":
        def save_uploaded_file(uploaded_file,save_location,save_name):
            file_path=os.path.join(save_location,save_name)
            with open(file_path, 'wb') as file:
                file.write(uploaded_file.read())
            return file_path
        
        save_location="./backend/uploads2"
        os.makedirs(save_location,exist_ok=True)
        save_name="saved_image.png"
        uploaded_image=data
        if uploaded_image is not None:
            saved_file_path=save_uploaded_file(uploaded_image,save_location,save_name)
            st.success(f"Image file save to: {saved_file_path}")
        img=Image.open('./backend/uploads2/saved_image.png')
        extracted_text=tess.image_to_string(img)
        data=extracted_text
        payload = {'data': data}
        senti_class=calculated_sentiment(payload)
        calculated_recommendations(payload)



