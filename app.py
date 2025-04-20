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
from utils.db_init import init_database # Import DB initializer
from pathlib import Path
import configs # Import configs

# Initialize Database (Run once if DB doesn't exist)
# Wrap in try-except to prevent app crash if DB is locked or permissions issue
try:
    db_path = Path("data/app_data.db")
    if not db_path.exists():
        print("Database file not found, initializing...")
        init_database()
        print("Database initialization complete.")
except Exception as e:
    st.error(f"Database check/initialization failed: {e}")
    st.warning("Please ensure the data directory exists and has write permissions.")
    # Optionally st.stop() if DB is critical

# --- Page Config and Styling --- 
# Needs to be the first Streamlit command
st.set_page_config(
    page_title="Banthia's Quick Store",
    page_icon="🛒", # Changed icon
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load CSS
def load_css(file_name):
    css_path = Path("assets") / file_name
    if css_path.is_file():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {css_path}")

# Load custom CSS
load_css("style.css")

# Initialize session state (after page config)
init_session_state()

# --- Sidebar Rendering --- 
# Define step names and icons 
# Try loading from configs.py, fallback to default
DEFAULT_STEPS_CONFIG = {
    0: {"name": "Product Details", "icon": "📦"},
    1: {"name": "Select Supplier", "icon": "👥"},
    2: {"name": "Send Initial Message", "icon": "📝"},
    3: {"name": "Await Response", "icon": "🕒"},
    4: {"name": "Assign Worker", "icon": "🧑‍🔧"},
    5: {"name": "Send Confirmation", "icon": "📨"},
    6: {"name": "Order Complete", "icon": "✔️"}
}
STEPS_CONFIG = getattr(configs, 'STEPS_CONFIG', DEFAULT_STEPS_CONFIG)

with st.sidebar:
    # Sidebar Header (Logo Placeholder + Title)
    st.markdown("""
        <div class='sidebar-header'>
            <div>
                <div class='sidebar-title'>Banthia's Quick Store</div>
                <div class='sidebar-subtitle'>Supplier Order Management</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Add some space
    st.subheader("Order Progress")
    
    current_step = st.session_state.get('current_step', 0)
    
    # Render Step Navigation
    for step_num, config in STEPS_CONFIG.items():
        step_name = config["name"]
        icon = config["icon"]
        step_class = "sidebar-step-inactive"
        if step_num == current_step:
            step_class = "sidebar-step-active"
        elif step_num < current_step:
            step_class = "sidebar-step-completed"
            icon = "✅" # Use checkmark for completed steps

        st.markdown(f"""
            <div class='sidebar-step {step_class}'>
                <span class='sidebar-step-icon'>{icon}</span> 
                <span>{step_name}</span>
            </div>
        """, unsafe_allow_html=True)

# --- Main Content Area --- 

# Render main content area based on current step
main_content_area = st.container()
with main_content_area:
    current_step = st.session_state.get('current_step', 0)
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
    else:
        st.error("Invalid step number.")
        st.button("Restart Process", on_click=lambda: st.session_state.clear() or st.rerun())

# --- Footer --- 

st.markdown("--- ") # Visual separator
st.markdown("""
    <div class='footer'>
        © 2024 Banthia's Quick Store. All rights reserved. | Built with Streamlit by Khushi
    </div>
""", unsafe_allow_html=True) 