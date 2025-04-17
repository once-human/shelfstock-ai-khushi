import streamlit as st
import time
from utils.data_handler import get_supplier_by_id # Use DB function
from utils.state_management import reset_state 

def render_await_response():
    """Render the await response step - waits for manual user confirmation."""
    st.header("Step 3: Await Supplier Response")
    
    supplier_id = st.session_state.get('selected_supplier_id')
    supplier = get_supplier_by_id(supplier_id)
    
    if not supplier:
        st.error("Supplier details not found. Please restart the process.")
        if st.button("Restart Order"):
            reset_state()
            st.rerun()
        return
    
    # Check if a response has been manually entered
    if st.session_state.get('supplier_response') is None:
        st.info(f"📧 Initial inquiry email sent to {supplier['name']} ({supplier.get('contact_email', 'No email on file')}).")
        st.markdown("**Waiting for supplier response.** Please check your email or other communication channels.")
        st.markdown("Once you receive the response, please update the status below:")
        
        # Add buttons for manual confirmation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Mark Order as ACCEPTED", type="primary"):
                st.session_state['supplier_response'] = 'Accepted'
                st.rerun()
        with col2:
            if st.button("Mark Order as REJECTED"):
                st.session_state['supplier_response'] = 'Rejected'
                st.rerun()
    
    # If response is marked as Accepted
    elif st.session_state['supplier_response'] == 'Accepted':
        st.success(f"✅ Order marked as **Accepted** by {supplier['name']}.")
        if st.button("Next: Assign Worker", type="primary"):
            st.session_state['current_step'] = 4
            st.rerun()
            
    # If response is marked as Rejected
    elif st.session_state['supplier_response'] == 'Rejected':
        st.error(f"❌ Order marked as **Rejected** by {supplier['name']}.")
        st.warning("Cannot proceed with this order.")
        if st.button("Start New Order"):
            reset_state()
            st.rerun() 