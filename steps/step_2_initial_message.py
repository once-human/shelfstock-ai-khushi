import streamlit as st
from utils.data_handler import load_suppliers

def render_initial_message():
    """Render the initial message step where a message is sent to the supplier."""
    st.header("Step 2: Initial Message")
    
    # Get supplier details
    suppliers = load_suppliers()
    supplier = next((s for s in suppliers if s['id'] == st.session_state.get('selected_supplier_id')), None)
    
    if not supplier:
        st.error("No supplier selected. Please go back and select a supplier.")
        return
        
    # Display message preview
    st.subheader("Message Preview")
    message = f"""
    Dear {supplier['name']},

    We would like to place an order for:
    Product: {st.session_state.get('product_name')}
    Quantity: {st.session_state.get('quantity')}

    Please confirm if you can fulfill this order.

    Best regards,
    Your Company Name
    """
    
    st.text_area("Message", value=message, height=200, disabled=True)
    
    # Simulate sending message
    if st.button("Send Message"):
        with st.spinner("Sending message..."):
            # Simulate API delay
            import time
            time.sleep(2)
            st.success("Message sent successfully!")
            st.session_state['current_step'] = 3 