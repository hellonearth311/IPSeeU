import streamlit as st
from scan import scan

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
st.write("Welcome to IPSeeU. Click the button below to scan your network for all the devices on it.")

if 'scan_results' not in st.session_state:
    st.session_state['scan_results'] = None
if 'scan_count' not in st.session_state:
    st.session_state['scan_count'] = 0

if st.button("Scan"):
    st.session_state['scan_results'] = None  # Clear previous results
    st.session_state['scan_count'] += 1  # Increment to create unique component key
    result = scan(st.session_state['scan_count'])  # Pass the count for unique key
    st.session_state['scan_results'] = result

if st.session_state['scan_results'] is not None:
    st.write(st.session_state['scan_results'])