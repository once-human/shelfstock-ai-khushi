import streamlit as st
from utils.data_handler import get_supplier_by_id, get_worker_by_id
from utils.state_management import reset_state

def render_complete():
    """Render the final completion step with a well-formatted summary card."""
    st.header("Step 6: Order Complete")

    # --- Data Retrieval and Validation ---
    supplier_id = st.session_state.get('selected_supplier_id')
    worker_id = st.session_state.get('selected_worker_id')
    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    # Check if essential info exists from previous steps
    if not all([supplier_id, worker_id, product_name, quantity >= 1]):
        st.error("Order information is incomplete or invalid. Cannot display summary.")
        st.warning("Please restart the process to ensure all steps are completed correctly.")
        if st.button("Start New Order"):
            reset_state()
            st.rerun()
        return

    # Fetch details, handle potential None values
    supplier = get_supplier_by_id(supplier_id)
    worker = get_worker_by_id(worker_id)

    if not supplier or not worker:
        st.error("Could not retrieve supplier or worker details for the summary.")
        st.warning("The order might be complete, but the summary cannot be fully displayed. Consider restarting.")
        if st.button("Start New Order"):
            reset_state()
            st.rerun()
        return

    # --- Display Summary Card --- 
    st.success("🎉 Congratulations! The order process is successfully completed.")
    st.write("Below is the final summary of your order:")
    st.write("") # Spacer

    # Use a container and CSS for the card effect and add animation class
    with st.container():
        # Add the class here to apply animation to the card div
        st.markdown("<div class='card final-summary-card'>", unsafe_allow_html=True)
        st.subheader("📜 Final Order Summary")
        
        # Use columns for better organization within the card
        col1, col2 = st.columns(2)
        
        with col1:
            # Using st.markdown allows bolding specific parts
            st.markdown("### Product Details")
            st.markdown(f"- **Product:** `{product_name}`")
            st.markdown(f"- **Quantity:** `{quantity}`")
            st.write("") # Vertical space within column
            
            st.markdown("### Supplier Information")
            st.markdown(f"- **Name:** {supplier.get('name', 'N/A')}")
            st.markdown(f"- **Contact:** {supplier.get('contact_email', 'N/A')}")
            st.markdown(f"- **Location:** {supplier.get('location', 'N/A')}")
        
        with col2:
            st.markdown("### Assigned Internal Contact")
            st.markdown(f"- **Name:** {worker.get('name', 'N/A')}")
            st.markdown(f"- **Role:** {worker.get('role', 'N/A')}")
            # Consider adding worker contact if available in data
            # st.markdown(f"- **Email:** {worker.get('email', 'N/A')}")
            st.write("") # Vertical space within column
            
            st.markdown("### Order Status")
            # These statuses are inferred by reaching this step
            st.markdown("- **Supplier Response:** Accepted") 
            st.markdown("- **Confirmation:** Sent") 
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("") # Spacer after card

    # --- Action Button --- 
    st.markdown("--- ")
    _, btn_col, _ = st.columns([2, 1, 2]) # Centered button
    with btn_col:
        if st.button("✨ Start a New Order", type="primary", use_container_width=True):
            reset_state() # Clear session state for a fresh start
            st.rerun() 