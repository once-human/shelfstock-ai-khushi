# Utility functions for managing Streamlit session state
import streamlit as st

def init_session_state():
    """Initialize the session state with default values if they don't exist."""
    defaults = {
        'current_step': 0,
        'product_name': '',
        'quantity': 1,
        'selected_supplier_id': None,
        'supplier_response': None,
        'selected_worker_id': None,
        'order_complete': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def initialize_state():
    """Initializes the session state variables if they don't exist."""
    if 'current_step' not in st.session_state:
        st.session_state['current_step'] = 0
    if 'product_name' not in st.session_state:
        st.session_state['product_name'] = ""
    if 'quantity' not in st.session_state:
        st.session_state['quantity'] = 1
    if 'selected_supplier_id' not in st.session_state:
        st.session_state['selected_supplier_id'] = None
    if 'supplier_response' not in st.session_state:
        st.session_state['supplier_response'] = None # e.g., 'Accepted', 'Rejected'
    if 'assigned_worker_id' not in st.session_state:
        st.session_state['assigned_worker_id'] = None
    # Add any other state variables needed

def next_step():
    """Increments the current step."""
    # Add validation if needed before incrementing
    st.session_state['current_step'] += 1

def reset_state():
    """Resets the session state for a new order."""
    st.session_state['current_step'] = 0
    st.session_state['product_name'] = ""
    st.session_state['quantity'] = 1
    st.session_state['selected_supplier_id'] = None
    st.session_state['supplier_response'] = None
    st.session_state['assigned_worker_id'] = None
    # Reset any other state variables 