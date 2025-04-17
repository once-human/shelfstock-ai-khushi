import streamlit as st

def render_product_details():
    """
    Render the product details step where users input product name and quantity.
    """
    st.header("Step 0: Product Details")
    
    # Product Name Input
    product_name = st.text_input(
        "Product Name",
        value=st.session_state.get('product_name', ''),
        key='product_name'
    )
    
    # Quantity Input
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=st.session_state.get('quantity', 1),
        key='quantity'
    )
    
    # Next button
    if st.button("Next Step", type="primary"):
        if product_name.strip():  # Basic validation
            st.session_state['current_step'] = 1
        else:
            st.error("Please enter a product name before proceeding.") 