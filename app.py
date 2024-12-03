import os
import streamlit as st
import requests 


# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'

# Define the url to be used by requests.get to get a prediction (adapt if needed)
upload_url = BASE_URI + 'upload-audio'
predict_url = BASE_URI + 'predict-deepfake'

# --- Page Config ---
st.set_page_config(
    page_title="Fake No More - Voice Analysis",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- App Header ---
st.markdown(
    """
    <style>
    /* Set background color for the entire app */
    body {
        background-color: #07182A; /* Light blue background */
    }
    .title {
        font-size: 58px;
        font-weight: bold;
        text-align: center;
        color: #408BDE;
        margin-bottom: 20px;
        animation: fade-in 2s;
    }
    .subtitle {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #AAD7FA;

    }
    .next-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #408BDE;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
    }
    
    </style>
    <div class="title">🎙️ Fake No More 🎙️</div>
    <div class="subtitle">Drawing the line between real and artificial voices</div>
    """,
    unsafe_allow_html=True,
)

#st.write("### Upload Your Audio File"; margin-bottom: 20px)
st.markdown("---")

st.markdown(
    """
     <style>
    .subtitle2 {
        text-align: left;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px
        color: #00aaff;
    }
    
    </style>
    <div class="subtitle2">Step 1 - Upload a file: </div>
    """,
    unsafe_allow_html=True,
)

# --- File Upload ---
uploaded_file = st.file_uploader(' ', type=["wav"])

if uploaded_file:
    st.success(f"File {uploaded_file.name} uploaded successfully.")
    st.markdown("---")
    st.markdown(
        """
        </style>
        <div class="subtitle2">Step 2 - Play and analyze the audio</div>
        """,
        unsafe_allow_html=True,
)
    st.write("\n\n\n")
    # --- Audio Playback ---
    st.audio(uploaded_file, format="audio/wav")
    
    # Send the file to the FastAPI endpoint for upload
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "audio/wav")}

    # --- Placeholder Prediction ---
    st.markdown("---")
    st.markdown(
    """
    </style>
    <div class="subtitle2">Step 3 - Predict the results</div>
    """,
    unsafe_allow_html=True,
    )
    st.write("\n\n\n")
    if st.button("Analyze Voice"):
        with st.spinner("Analyzing..."):
            # Now send the file to the /predict-deepfake/ endpoint to get the prediction
            predict_response = requests.post(predict_url, files=files)
            if predict_response.status_code == 200:
                prediction = predict_response.json().get("prediction")
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 20px; font-size: 20px; 
                                font-weight: bold; color: {"#2ecc71" if prediction == "REAL" else "#e74c3c"}; 
                                border: 2px solid {"#2ecc71" if prediction == "REAL" else "#e74c3c"}; 
                                border-radius: 10px; margin-top: 20px;'>
                        {prediction}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.error(f"Error in prediction: {predict_response.json().get('error', 'Unknown error')}")



