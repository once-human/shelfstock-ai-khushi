# Main Streamlit application file
import streamlit as st
from steps.step_0_product_details import render_product_details
from steps.step_1_select_supplier import render_select_supplier
from steps.step_2_initial_message import render_initial_message
from steps.step_3_await_response import render_await_response
from steps.step_4_assign_worker import render_assign_worker
from steps.step_5_send_confirmation import render_send_confirmation
from steps.step_6_complete import render_complete
from utils.state_management import init_session_state
from pathlib import Path

# Function to load CSS
def load_css(file_name):
    css_path = Path("assets") / file_name
    if css_path.is_file():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Supplier Order Management",
    page_icon="🏭",
    layout="wide"
)

# Initialize session state
init_session_state()

# Load custom CSS
load_css("style.css")

# Define step names (TODO: Move to configs.py)
STEPS = {
    0: "Product Details",
    1: "Select Supplier",
    2: "Initial Message",
    3: "Await Response",
    4: "Assign Worker",
    5: "Send Confirmation",
    6: "Complete"
}

# Render sidebar step tracker
with st.sidebar:
    st.title("Progress")
    current_step = st.session_state.get('current_step', 0)
    
    for step_num, step_name in STEPS.items():
        if step_num == current_step:
            st.markdown(f"**➡️ {step_name}**")
        elif step_num < current_step:
            st.markdown(f"✅ {step_name}")
        else:
            st.markdown(f"⭕ {step_name}")

# Render main content area based on current step
if current_step == 0:
    render_product_details()
elif current_step == 1:
    render_select_supplier()
elif current_step == 2:
    render_initial_message()
elif current_step == 3:
    render_await_response()
elif current_step == 4:
    render_assign_worker()
elif current_step == 5:
    render_send_confirmation()
elif current_step == 6:
    render_complete()
# TODO: Add other steps as they are implemented 