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

if 'scanning' not in st.session_state:
    st.session_state['scanning'] = False
if 'scan_results' not in st.session_state:
    st.session_state['scan_results'] = None

scan_button_placeholder = st.empty()
results_placeholder = st.empty()

if not st.session_state['scanning']:
    if scan_button_placeholder.button("Scan", key="scan_button"):
        st.session_state['scanning'] = True
        scan_button_placeholder.markdown("**Scanning...**")
        result = scan()
        st.session_state['scan_results'] = result
        st.session_state['scanning'] = False
        st.rerun()
    elif st.session_state['scan_results'] is not None:
        results_placeholder.write(st.session_state['scan_results'])
else:
    scan_button_placeholder.markdown("**Scanning...**")