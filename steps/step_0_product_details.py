import streamlit as st
from code_library.openai_api_helper import generate_completion

def render_product_details():
    """
    Render the product details step with improved layout and styling.
    Inputs are grouped, and AI insights appear below.
    """
    st.header("Step 0: Enter Product Details")
    st.write("Specify the product and quantity. AI insights will appear below based on your input.")
    st.markdown("--- ")

    # Initialize session state if needed
    # (Ensure keys used for AI results are also initialized)
    for key in ['product_name', 'quantity', 'product_suggestions', 'product_validation', 'last_product_name', 'last_quantity']:
        if key not in st.session_state:
            st.session_state[key] = '' if key == 'product_name' else (1 if key == 'quantity' else None)
            if key == 'last_quantity': st.session_state[key] = 0 # Initialize last_quantity specifically

    # --- Input Section --- 
    with st.container():
        st.subheader("📦 Product Information")
        col1, col2 = st.columns(2) # Use columns for inputs for better alignment
        with col1:
            product_name = st.text_input(
                "Product Name",
                value=st.session_state.product_name,
                placeholder="e.g., Organic Basmati Rice",
                key="product_name_input",
                help="Enter the product you want to order."
            )
        with col2:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=st.session_state.quantity,
                key="quantity_input",
                help="Enter the desired order quantity."
            )

        # Update session state immediately on input change
        st.session_state.product_name = product_name
        st.session_state.quantity = quantity

    # --- AI Insights Section --- 
    st.write("") # Add some spacing
    with st.container():
        st.subheader("🤖 AI Insights")

        # --- Trigger AI Calls --- 
        # Trigger suggestions only when product name *changes* and is not empty
        if product_name and product_name != st.session_state.last_product_name:
            with st.spinner("🧠 Getting AI product suggestions..."):
                prompt = f"""
                Based on the product name \"{product_name}\", briefly suggest for a Kirana store owner:
                1. **Common Specifications:** (e.g., grade, origin, common packaging sizes)
                2. **Typical Order Quantities:** (e.g., initial bulk range)
                3. **Key Certifications/Standards:** (e.g., FSSAI, Organic, Agmark)
                Format as concise Markdown bullet points.
                """
                message_history = [
                    {"role": "system", "content": "You are a helpful sourcing assistant for Indian Kirana stores. Provide concise, actionable suggestions for product specifications and ordering details."},
                    {"role": "user", "content": prompt}
                ]
                try:
                    suggestions = generate_completion(message_history)
                    st.session_state.product_suggestions = suggestions
                    st.session_state.last_product_name = product_name # Update last processed name
                    st.session_state.product_validation = None # Clear validation if product changes
                    st.session_state.last_quantity = 0
                except Exception as e:
                    st.session_state.product_suggestions = f"*Error getting suggestions: {e}*"
            st.rerun() # Rerun to display new suggestions/clear old validation
        
        # Trigger validation only when quantity *changes* and product name is present
        if product_name and quantity != st.session_state.last_quantity:
            with st.spinner("🤔 Analyzing quantity..."):
                prompt = f"""
                For product \"{product_name}\" with quantity {quantity} for a Kirana store order, analyze:
                1. **Reasonableness:** Is this quantity typical for a Kirana store? (Consider shelf life, storage)
                2. **Potential Concerns:** (e.g., too high for initial stock, too low for wholesale discount?)
                3. **Recommendations:** (e.g., suggest typical range if unusual).
                Keep the response brief, actionable, using Markdown.
                """
                message_history = [
                    {"role": "system", "content": "You are a helpful Kirana store sourcing assistant. Validate order quantities briefly, considering typical store needs and providing actionable feedback."},
                    {"role": "user", "content": prompt}
                ]
                try:
                    validation = generate_completion(message_history)
                    st.session_state.product_validation = validation
                    st.session_state.last_quantity = quantity # Update last processed quantity
                except Exception as e:
                    st.session_state.product_validation = f"*Error validating quantity: {e}*"
            st.rerun() # Rerun to display new validation

        # --- Display AI Results --- 
        ai_results_exist = st.session_state.product_suggestions or st.session_state.product_validation

        if not ai_results_exist and product_name:
            st.info("AI is analyzing... Refresh if needed or adjust product/quantity.")
        elif not ai_results_exist:
             st.info("Enter product name and quantity above to get AI insights.")

        if st.session_state.product_suggestions:
            st.markdown("**Product Insights:**")
            st.markdown(f"<div class='ai-insight-box animate-slideUpFadeIn'>{st.session_state.product_suggestions}</div>", unsafe_allow_html=True)
        
        if st.session_state.product_validation:
            st.markdown("**Quantity Analysis:**")
            st.markdown(f"<div class='ai-insight-box animate-slideUpFadeIn delay-1'>{st.session_state.product_validation}</div>", unsafe_allow_html=True)
        

    # --- Navigation --- 
    st.markdown("--- ") 
    # Use columns to align button to the right
    col1, col2 = st.columns([4, 1]) # Give more space to col1, button in col2
    with col2:
        # Disable button if product name is missing
        next_disabled = not bool(st.session_state.product_name)
        if st.button("Select Supplier →", type="primary", use_container_width=True, disabled=next_disabled, help="Proceed to supplier selection"):
            # Clear next step's state before moving
            st.session_state['supplier_recommendations'] = None
            st.session_state['current_supplier_insights'] = None
            st.session_state['last_analyzed_supplier_id'] = None
            st.session_state['current_step'] = 1
            st.rerun() 