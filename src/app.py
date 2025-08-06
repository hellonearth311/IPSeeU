import streamlit as st
from scan import hack_function

# custom css
st.markdown(
    """
    <style>
    body {
        background-color: #0f111a;
        color: #39ff14;
    }
    .stApp {
        background-color: #0f111a;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #39ff14;
        font-family: 'Fira Mono', monospace;
    }
    .stButton>button {
        background-color: #222;
        color: #39ff14;
        border: 1px solid #39ff14;
        font-family: 'Fira Mono', monospace;
    }
    .stButton>button:hover {
        background-color: #39ff14;
        color: #222;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("IPSeeU")
st.write("Welcome to IPSeeU. Click the button below to scan your network for all the devices")

if st.button("Initiate Hack"):
    hack_function()