import streamlit as st
from utils.data_handler import load_suppliers

def render_select_supplier():
    """
    Render the supplier selection step where users choose a supplier from a list.
    """
    st.header("Step 1: Select Supplier")
    
    try:
        suppliers = load_suppliers()
        
        if not suppliers:
            st.error("No suppliers available. Please add suppliers to the system.")
            return
            
        # Display suppliers with their ratings
        selected_supplier = st.radio(
            "Select a Supplier",
            options=[(s['id'], f"{s['name']} (Rating: {s['rating']}/5)") for s in suppliers],
            format_func=lambda x: x[1]
        )
        
        if st.button("Next Step"):
            st.session_state['selected_supplier_id'] = selected_supplier[0]
            st.session_state['current_step'] = 2
            
    except Exception as e:
        st.error(f"Error loading suppliers: {str(e)}") 