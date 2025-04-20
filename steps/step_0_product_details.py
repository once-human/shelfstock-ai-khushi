import streamlit as st
from code_library.openai_api_helper import generate_completion

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
    
    # Initialize session state for AI suggestions
    if 'product_suggestions' not in st.session_state:
        st.session_state['product_suggestions'] = None
    if 'product_validation' not in st.session_state:
        st.session_state['product_validation'] = None

    # Product Name Input with AI suggestions
    product_name = st.text_input(
        "Product Name",
        value=st.session_state.get('product_name', ''),
        placeholder="Enter the product name",
        help="Enter the product name and get AI suggestions"
    )

    # Get AI suggestions when product name changes
    if product_name and product_name != st.session_state.get('last_product_name', ''):
        with st.spinner("Getting AI suggestions..."):
            prompt = f"""
            Based on the product name "{product_name}", suggest:
            1. Common specifications buyers should consider
            2. Typical quantity ranges for bulk orders
            3. Any quality standards or certifications to look for
            
            Format the response in clear bullet points.
            """
            message_history = [
                {"role": "system", "content": "You are a helpful product sourcing assistant that provides concise, relevant suggestions for product specifications and ordering details."},
                {"role": "user", "content": prompt}
            ]
            try:
                suggestions = generate_completion(message_history)
                st.session_state['product_suggestions'] = suggestions
                st.session_state['last_product_name'] = product_name
            except Exception as e:
                st.error(f"Could not get AI suggestions: {e}")

    # Display AI suggestions if available
    if st.session_state.get('product_suggestions'):
        with st.expander("📋 AI Product Insights", expanded=True):
            st.markdown(st.session_state['product_suggestions'])

    # Quantity input with AI validation
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=st.session_state.get('quantity', 1),
        help="Enter the quantity needed"
    )

    # Validate quantity with AI when it changes
    if quantity and quantity != st.session_state.get('last_quantity', 0):
        with st.spinner("Validating quantity..."):
            prompt = f"""
            For product "{product_name}" with quantity {quantity}, analyze:
            1. If this is a reasonable order quantity
            2. Any potential concerns or recommendations
            3. Suggested minimum/maximum quantities if applicable
            
            Keep the response brief and actionable.
            """
            message_history = [
                {"role": "system", "content": "You are a helpful sourcing assistant that validates order quantities and provides brief, actionable feedback."},
                {"role": "user", "content": prompt}
            ]
            try:
                validation = generate_completion(message_history)
                st.session_state['product_validation'] = validation
                st.session_state['last_quantity'] = quantity
            except Exception as e:
                st.error(f"Could not validate quantity: {e}")

    # Display AI validation if available
    if st.session_state.get('product_validation'):
        with st.expander("🔍 AI Quantity Analysis", expanded=True):
            st.markdown(st.session_state['product_validation'])

    # Next button
    if st.button("Next Step", type="primary"):
        if not product_name:
            st.error("Please enter a product name.")
            return
        
        # Save to session state
        st.session_state['product_name'] = product_name
        st.session_state['quantity'] = quantity
        st.session_state['current_step'] = 1
        st.rerun() 