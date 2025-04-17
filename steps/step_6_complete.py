import streamlit as st
from utils.data_handler import load_suppliers, load_workers
from utils.state_management import reset_state

def render_complete():
    """Render the complete step showing order summary and completion status."""
    st.header("Step 6: Order Complete")
    
    # Get all relevant data
    suppliers = load_suppliers()
    workers = load_workers()
    
    supplier = next((s for s in suppliers if s['id'] == st.session_state.get('selected_supplier_id')), None)
    worker = next((w for w in workers if w['id'] == st.session_state.get('selected_worker_id')), None)
    
    if not supplier or not worker:
        st.error("Missing order information. Please start a new order.")
        return
    
    # Display success message
    st.success("🎉 Order Successfully Completed!")
    
    # Display order summary in a nice format
    st.subheader("Order Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Product Details**")
        st.write(f"Product Name: {st.session_state.get('product_name')}")
        st.write(f"Quantity: {st.session_state.get('quantity')}")
        
    with col2:
        st.markdown("**Supplier Information**")
        st.write(f"Supplier: {supplier['name']}")
        st.write(f"Rating: {supplier['rating']}/5")
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**Assigned Worker**")
        st.write(f"Name: {worker['name']}")
        st.write(f"Role: {worker['role']}")
        
    with col4:
        st.markdown("**Order Status**")
        st.write("Status: Confirmed")
        st.write("Response: Accepted")
    
    # Add button to start new order
    if st.button("Start New Order", type="primary"):
        reset_state()
        st.rerun() 