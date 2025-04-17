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

# Define step names and icons (TODO: Move to configs.py)
STEPS_CONFIG = {
    0: {"name": "Product Details", "icon": "📦"},
    1: {"name": "Select Supplier", "icon": "👥"},
    2: {"name": "Initial Message", "icon": "📝"},
    3: {"name": "Await Response", "icon": "🕒"},
    4: {"name": "Assign Worker", "icon": "🧑\u200d🔧"}, # Using unicode for person mechanic
    5: {"name": "Send Confirmation", "icon": "📨"},
    6: {"name": "Complete", "icon": "✔️"}
}

# Render sidebar step tracker
with st.sidebar:
    st.title("Order Steps") # Changed title slightly
    current_step = st.session_state.get('current_step', 0)
    
    for step_num, config in STEPS_CONFIG.items():
        step_name = config["name"]
        icon = config["icon"]
        if step_num == current_step:
            # Use Markdown bold for active step, CSS targets this
            st.markdown(f"**{icon} {step_name}**", unsafe_allow_html=True)
        elif step_num < current_step:
            # Completed step - you could use a different icon or style if desired
            st.markdown(f"✅ {step_name}", unsafe_allow_html=True) # Using checkmark for completed
        else:
            # Inactive step
            st.markdown(f"{icon} {step_name}", unsafe_allow_html=True)

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