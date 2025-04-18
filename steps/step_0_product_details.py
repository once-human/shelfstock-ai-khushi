import streamlit as st

def render_product_details():
    """
    Render the product details step where users input product name and quantity.
    """
    st.header("Step 0: Product Details")
    
    # Initialize session state if needed
    if 'product_name' not in st.session_state:
        st.session_state['product_name'] = ''
    if 'quantity' not in st.session_state:
        st.session_state['quantity'] = 1
    
    # Product Name Input - using on_change callback
    product_name = st.text_input(
        "Product Name",
        value=st.session_state.product_name,
        key='product_name_input'  # Changed key to avoid conflict
    )
    
    # Quantity Input
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=st.session_state.quantity,
        key='quantity_input'  # Changed key to avoid conflict
    )
    
    # Next button
    if st.button("Next Step", type="primary"):
        if product_name.strip():  # Basic validation
            # Update session state
            st.session_state.product_name = product_name
            st.session_state.quantity = quantity
            st.session_state.current_step = 1
            st.rerun()
        else:
            st.error("Please enter a product name before proceeding.") 