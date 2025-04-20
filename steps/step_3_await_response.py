import streamlit as st
from utils.data_handler import get_supplier_by_id
from utils.state_management import reset_state

def render_await_response():
    """Render the await response step with clearer layout and actions within a card."""
    st.header("Step 3: Await Supplier Response")

    # --- Data Validation ---
    supplier_id = st.session_state.get('selected_supplier_id')
    if not supplier_id:
        st.error("No supplier selected. Please go back to Step 1.")
        if st.button("← Back to Supplier Selection"):
            st.session_state['current_step'] = 1
            st.rerun()
        return
        
    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        st.error(f"Could not find details for supplier ID: {supplier_id}")
        if st.button("← Back to Supplier Selection"):
            st.session_state['current_step'] = 1
            st.rerun()
        return
    
    supplier_name = supplier.get('name', 'the supplier')
    supplier_email = supplier.get('contact_email', 'their contact method')

    # Initialize state if needed
    if 'supplier_response' not in st.session_state:
        st.session_state.supplier_response = None

    response_status = st.session_state.supplier_response

    st.write(f"Waiting for a response from **{supplier_name}** regarding the order inquiry sent.")
    st.markdown("--- ")

    # --- Display based on response status --- 
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        if response_status is None:
            st.subheader("⏳ Waiting for Response")
            st.info(f"An inquiry was simulated as sent to **{supplier_name}** ({supplier_email}).")
            st.write("Please monitor your communication channels (e.g., email) for their reply.")
            st.markdown("**Once you receive the response, please update the status here:**")
            st.write("") # Spacer
            
            # Buttons side-by-side
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mark as ACCEPTED 👍", key="accept_order", use_container_width=True, type="primary"):
                    st.session_state.supplier_response = 'Accepted'
                    st.rerun()
            with col2:
                # Use secondary style for reject
                if st.button("Mark as REJECTED 👎", key="reject_order", use_container_width=True, type="secondary"):
                    st.session_state.supplier_response = 'Rejected'
                    st.rerun()
        
        elif response_status == 'Accepted':
            st.subheader("✅ Order Accepted")
            st.success(f"Status updated: **Accepted** by {supplier_name}.")
            st.write("You can now proceed to assign an internal worker to manage this order.")
            st.write("")
            
            # Align Next button to the right
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("Assign Worker →", type="primary", use_container_width=True):
                    # Clear next step's state
                    st.session_state['worker_recommendations'] = None
                    st.session_state['current_worker_insights'] = None
                    st.session_state['last_analyzed_worker_id'] = None
                    st.session_state['selected_worker_id'] = None
                    
                    st.session_state['current_step'] = 4
                    st.rerun()
                
        elif response_status == 'Rejected':
            st.subheader("❌ Order Rejected")
            st.error(f"Status updated: **Rejected** by {supplier_name}.")
            st.warning("This order cannot proceed. You may need to select a different supplier or product.")
            st.write("")
            
            # Align Restart button to the right
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("Start New Order", key="restart_rejected", use_container_width=True):
                    reset_state() # Reset the entire session state
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True) 