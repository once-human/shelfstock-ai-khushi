import streamlit as st
from utils.data_handler import load_suppliers
from code_library.openai_api_helper import generate_completion

def render_select_supplier():
    """Render the supplier selection step with AI-powered recommendations."""
    st.header("Step 1: Select Supplier")
    
    # Get product details from session state
    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    
    # Load all suppliers
    suppliers = load_suppliers()
    
    if not suppliers:
        st.error("No suppliers found in the database.")
        return

    # Initialize AI recommendation state
    if 'supplier_recommendations' not in st.session_state:
        st.session_state['supplier_recommendations'] = None

    # Get AI recommendations for suppliers
    if not st.session_state.get('supplier_recommendations'):
        with st.spinner("Analyzing suppliers..."):
            # Create a detailed prompt for supplier analysis
            suppliers_info = "\n".join([
                f"Supplier {i+1}: {s['name']}\n"
                f"- Specialties: {s.get('specialties', 'N/A')}\n"
                f"- Rating: {s.get('rating', 'N/A')}/5\n"
                f"- Min Order: {s.get('min_order', 'N/A')}\n"
                for i, s in enumerate(suppliers)
            ])
            
            prompt = f"""
            Analyze these suppliers for ordering "{product_name}" (Quantity: {quantity}):

            {suppliers_info}

            Provide:
            1. Top recommended suppliers in order
            2. Reasoning for each recommendation
            3. Any potential concerns or special considerations

            Format as a clear, bulleted list.
            """
            
            message_history = [
                {"role": "system", "content": "You are a procurement expert who analyzes suppliers and provides detailed, actionable recommendations."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                recommendations = generate_completion(message_history)
                st.session_state['supplier_recommendations'] = recommendations
            except Exception as e:
                st.error(f"Could not generate supplier recommendations: {e}")

    # Display AI recommendations
    if st.session_state.get('supplier_recommendations'):
        with st.expander("🎯 AI Supplier Analysis", expanded=True):
            st.markdown(st.session_state['supplier_recommendations'])

    # Display supplier selection with enhanced UI
    st.subheader("Select a Supplier")
    
    # Create radio buttons for supplier selection
    supplier_options = []
    for supplier in suppliers:
        rating_stars = "⭐" * int(supplier.get('rating', 0))
        label = f"{supplier['name']} {rating_stars}\n"
        if supplier.get('specialties'):
            label += f"Specialties: {supplier['specialties']}\n"
        if supplier.get('min_order'):
            label += f"Min Order: {supplier['min_order']}"
        supplier_options.append(label)

    selected_index = st.radio(
        "Available Suppliers",
        range(len(suppliers)),
        format_func=lambda x: supplier_options[x],
        key="supplier_radio"
    )

    selected_supplier = suppliers[selected_index]

    # Display detailed supplier information
    with st.expander("📊 Detailed Supplier Information", expanded=True):
        st.markdown(f"""
        ### {selected_supplier['name']}
        
        **Rating:** {selected_supplier.get('rating', 'N/A')}/5  
        **Specialties:** {selected_supplier.get('specialties', 'N/A')}  
        **Minimum Order:** {selected_supplier.get('min_order', 'N/A')}  
        **Contact:** {selected_supplier.get('contact_email', 'N/A')}
        
        {selected_supplier.get('description', '')}
        """)

    # Get AI insights for the selected supplier
    if selected_supplier['id'] != st.session_state.get('last_analyzed_supplier_id'):
        with st.spinner("Getting AI insights for selected supplier..."):
            prompt = f"""
            Analyze the fit between supplier "{selected_supplier['name']}" and the order:
            - Product: {product_name}
            - Quantity: {quantity}
            
            Consider:
            1. Supplier's specialties and minimum order requirements
            2. Potential advantages and risks
            3. Specific questions to ask or points to clarify
            
            Keep the response concise and actionable.
            """
            
            message_history = [
                {"role": "system", "content": "You are a procurement expert who provides specific insights about supplier-order fit."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                supplier_insights = generate_completion(message_history)
                st.session_state['current_supplier_insights'] = supplier_insights
                st.session_state['last_analyzed_supplier_id'] = selected_supplier['id']
            except Exception as e:
                st.error(f"Could not generate supplier insights: {e}")

    # Display supplier-specific AI insights
    if st.session_state.get('current_supplier_insights'):
        with st.expander("💡 AI Supplier Insights", expanded=True):
            st.markdown(st.session_state['current_supplier_insights'])

    # Next button
    if st.button("Next Step", type="primary"):
        st.session_state['selected_supplier_id'] = selected_supplier['id']
        st.session_state['current_step'] = 2
        st.rerun() 