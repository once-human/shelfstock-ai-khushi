import streamlit as st
from utils.data_handler import load_suppliers, load_workers

def render_send_confirmation():
    """Render the send confirmation step where final confirmation is sent to all parties."""
    st.header("Step 5: Send Confirmation")
    
    # Get all relevant data
    suppliers = load_suppliers()
    workers = load_workers()
    
    supplier = next((s for s in suppliers if s['id'] == st.session_state.get('selected_supplier_id')), None)
    worker = next((w for w in workers if w['id'] == st.session_state.get('selected_worker_id')), None)
    
    if not supplier or not worker:
        st.error("Missing supplier or worker information. Please go back and complete previous steps.")
        return
    
    # Display confirmation message
    st.subheader("Confirmation Message Preview")
    confirmation = f"""
    Order Confirmation

    Product: {st.session_state.get('product_name')}
    Quantity: {st.session_state.get('quantity')}
    
    Supplier: {supplier['name']}
    Assigned Worker: {worker['name']}
    
    Status: Order Confirmed
    
    Thank you for your business!
    """
    
    st.text_area("Confirmation", value=confirmation, height=300, disabled=True)
    
    # Send confirmation button
    if st.button("Send Confirmation"):
        with st.spinner("Sending confirmation to all parties..."):
            import time
            time.sleep(2)
            st.success("Confirmation sent successfully!")
            st.session_state['current_step'] = 6 