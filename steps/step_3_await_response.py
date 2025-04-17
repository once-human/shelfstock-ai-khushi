import streamlit as st
import time
from utils.data_handler import load_suppliers
from utils.state_management import reset_state

def render_await_response():
    """Render the await response step where we wait for supplier's response."""
    st.header("Step 3: Await Response")
    
    # Get supplier details
    suppliers = load_suppliers()
    supplier = next((s for s in suppliers if s['id'] == st.session_state.get('selected_supplier_id')), None)
    
    if not supplier:
        st.error("No supplier selected. Please go back and select a supplier.")
        return
    
    # If we don't have a response yet, show waiting state
    if 'supplier_response' not in st.session_state or st.session_state['supplier_response'] is None:
        st.info(f"Waiting for response from {supplier['name']}...")
        
        # Add a simulate response button (in real app, this would be handled by backend)
        if st.button("Simulate Response"):
            with st.spinner("Getting response..."):
                time.sleep(2)
                # For demo, we'll always accept. In real app, this could be random or based on actual response
                st.session_state['supplier_response'] = 'Accepted'
                st.rerun()
    
    # If we have a response, show it
    else:
        response = st.session_state['supplier_response']
        if response == 'Accepted':
            st.success(f"{supplier['name']} has accepted your order!")
            if st.button("Proceed to Worker Assignment", type="primary"):
                st.session_state['current_step'] = 4
                st.rerun()
        else:
            st.error(f"{supplier['name']} has declined your order.")
            if st.button("Start Over"):
                # Reset relevant state
                reset_state()
                st.rerun() 