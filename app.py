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
# In a real deployment, this might be handled differently (e.g., separate script)
if not Path("data/app_data.db").exists():
    try:
        init_database()
    except Exception as e:
        st.error(f"Database initialization failed: {e}")
        st.stop() # Stop the app if DB can't be initialized

# Function to load CSS
def load_css(file_name):
    css_path = Path("assets") / file_name
    if css_path.is_file():
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set page config with custom theme
st.set_page_config(
    page_title="VIA Rides - Supplier Order Management",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Load custom CSS
load_css("style.css")

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

# Render sidebar step tracker with enhanced styling
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: var(--text-primary); font-size: 1.5rem; margin-bottom: 0.5rem;'>VIA Rides</h1>
            <p style='color: var(--text-secondary); font-size: 0.875rem;'>Supplier Order Management</p>
        </div>
    """, unsafe_allow_html=True)
    
    current_step = st.session_state.get('current_step', 0)
    
    for step_num, config in STEPS_CONFIG.items():
        step_name = config["name"]
        icon = config["icon"]
        
        if step_num == current_step:
            st.markdown(f"""
                <div class='step-active'>
                    <strong>{icon} {step_name}</strong>
                </div>
            """, unsafe_allow_html=True)
        elif step_num < current_step:
            st.markdown(f"""
                <div class='step-completed'>
                    <span>✅ {step_name}</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='step-inactive'>
                    {icon} {step_name}
                </div>
            """, unsafe_allow_html=True)

# Main content area with card container
st.markdown("""
    <div class='card-container'>
""", unsafe_allow_html=True)

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

st.markdown("""
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 2rem; padding: 1rem; color: var(--text-tertiary); font-size: 0.875rem;'>
        © 2025 VIA Rides. All rights reserved.
    </div>
""", unsafe_allow_html=True) 