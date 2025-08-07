import streamlit as st
from scan import scan

# custom css and favicon injection
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
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    /* Hide Deploy button with multiple methods */
    button[title="Deploy"] {display: none !important;}
    button[data-testid="stDeployButton"] {display: none !important;}
    .stApp > header {display: none !important;}
    header[data-testid="stHeader"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    /* Custom navigation buttons styling */
    .nav-button {
        margin-right: 10px;
    }

    div[data-testid="column"] .stButton > button {
        width: 100% !important;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# config page
st.set_page_config(
    page_title="IPSeeU",
    page_icon="https://www.python.org/static/favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

col1, col2, col3 = st.columns([2, 2, 6])

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Scanning"

with col1:
    if st.button("🔍 Scanning", key="scan_btn", use_container_width=True):
        st.session_state.current_page = "Scanning"

with col2:
    if st.button("ℹ️ About", key="about_btn", use_container_width=True):
        st.session_state.current_page = "About"

page = st.session_state.current_page

st.title("IPSeeU")

if page == "Scanning":
    st.write("Welcome to IPSeeU. Click the button below to scan your network for all the devices on it.")

    if 'scan_results' not in st.session_state:
        st.session_state['scan_results'] = None
    if 'scan_count' not in st.session_state:
        st.session_state['scan_count'] = 0

    if st.button("Scan"):
        st.session_state['scan_results'] = None
        st.session_state['scan_count'] += 1
        result = scan(st.session_state['scan_count'])
        st.session_state['scan_results'] = result

    if st.session_state['scan_results'] is not None:
        if isinstance(st.session_state['scan_results'], list) and len(st.session_state['scan_results']) > 0:
            st.table(st.session_state['scan_results'])
        elif isinstance(st.session_state['scan_results'], list):
            st.info("No devices found on the network.")
        else:
            st.write(st.session_state['scan_results'])

elif page == "About":
    st.title("About")
    st.markdown("""
    ## IPSeeU
    Created by Swarit Narang!
                
    Special thanks to:  
    - [Streamlit](https://streamlit.io) for making the web framework this app is based on.
    - [macvendors.co](https://macvendors.co) for identifying the vendors from mac address.
    - [The PSF](https://www.python.org/psf-landing/) for making the language that this is written in.
    
    ## Important Stuff
    - Source Code: https://github.com/hellonearth311/IPSeeU
    - Report a Bug: https://github.com/hellonearth311/IPSeeU/issues
    
    ## Socials
                
    - [GitHub](https://github.com/hellonearth311)
    > I write dumb code here :D
                
    - [YouTube](https://www.youtube.com/@hellonearth311)
    > I play Geometry Dash here 🥀
    """)