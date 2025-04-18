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
            
        st.markdown("Please choose a supplier from the list below.")

        # Using st.radio - CSS will style the individual radio labels
        selected_supplier_display = st.radio(
            "Available Suppliers", # Label for the radio group
            options=[(s['id'], f"{s['name']} (Rating: {s.get('rating', 'N/A')}/5)") for s in suppliers],
            format_func=lambda x: x[1], # Show only the formatted name/rating
            key="selected_supplier_radio",
            label_visibility="collapsed" # Hide the main radio group label, use markdown above instead
        )

        if selected_supplier_display:
            selected_supplier_id = selected_supplier_display[0]
            # Optional: Display details of the selected one if needed
            # supplier_details = next((s for s in suppliers if s['id'] == selected_supplier_id), None)
            # if supplier_details:
            #    with st.expander("Selected Supplier Details"):
            #        st.write(supplier_details)

            if st.button("Next Step", type="primary"):
                st.session_state['selected_supplier_id'] = selected_supplier_id
                st.session_state['current_step'] = 2
                st.rerun()
        else:
            st.info("Please select a supplier to continue.")
            
    except Exception as e:
        st.error(f"Error loading suppliers: {str(e)}") 