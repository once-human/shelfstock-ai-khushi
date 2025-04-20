import streamlit as st
from utils.data_handler import load_suppliers, get_supplier_by_id
from code_library.openai_api_helper import generate_completion

def render_select_supplier():
    """Render the supplier selection step with improved layout and AI recommendations."""
    st.header("Step 1: Select a Supplier")
    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    
    if not product_name: # Need product name for analysis
         st.warning("Product details missing. Please return to Step 0.")
         if st.button("← Back to Product Details"):
              st.session_state['current_step'] = 0
              st.rerun()
         return

    st.write(f"Finding suitable suppliers for **{quantity} x {product_name}**. AI analysis and recommendations are below.")
    st.markdown("--- ")

    suppliers = load_suppliers()
    if not suppliers:
        st.error("Could not load suppliers. Please check data source or configuration.")
        return

    # Initialize state keys for this step
    for key in ['supplier_recommendations', 'current_supplier_insights', 'last_analyzed_supplier_id', 'selected_supplier_id']:
         if key not in st.session_state:
              st.session_state[key] = None

    # --- AI Supplier Analysis (Run once per session for this step) ---
    # We only run this if recommendations haven't been generated yet for this session/step
    if st.session_state.supplier_recommendations is None:
        with st.spinner("🧠 Analyzing supplier suitability..."):
            # Simplified supplier info for prompt clarity
            suppliers_info = "\n".join([
                f"- ID: {s['id']}, Name: {s['name']}, Specialties: {s.get('specialties', 'N/A')}, Rating: {s.get('rating', 'N/A')}, MinQty: {s.get('minimum_order_qty', 'N/A')}"
                for s in suppliers
            ])
            
            prompt = f"""
            Analyze the following suppliers for an order of **{quantity} units of \"{product_name}\"** for a Kirana store:

            {suppliers_info}

            Based *only* on the provided information and the order context, provide:
            1.  **Top 3 Recommended Suppliers:** List their Names and IDs.
            2.  **Brief Reasoning:** For each, explain *why* they fit (e.g., relevant specialty, reasonable min qty).
            3.  **Potential Concerns:** Briefly note any issues (e.g., high min qty, specialty mismatch).

            Format concisely using Markdown. If no supplier seems suitable, state that.
            """
            message_history = [
                {"role": "system", "content": "You are a procurement expert for Indian Kirana stores analyzing suppliers based *only* on provided details and order context. Provide clear, actionable recommendations and concerns."},
                {"role": "user", "content": prompt}
            ]
            try:
                recommendations = generate_completion(message_history)
                st.session_state.supplier_recommendations = recommendations
                st.rerun() # Rerun to display recommendations
            except Exception as e:
                st.session_state.supplier_recommendations = f"*Error analyzing suppliers: {e}*"
                # No rerun on error, just display the error message

    # --- Display AI Recommendations & Supplier Selection ---
    col1, col2 = st.columns([3, 2]) # Adjust ratio: More space for selection/analysis

    with col1:
        st.subheader("🎯 AI Analysis & Recommendations")
        if st.session_state.supplier_recommendations:
            st.markdown(f"<div class='ai-insight-box animate-slideUpFadeIn'>{st.session_state.supplier_recommendations}</div>", unsafe_allow_html=True)
        else:
            # This state should ideally not be reached if spinner ran, but as fallback:
            st.info("AI analysis is processing or encountered an error.")
        
        st.write("") # Spacer
        # The subheader acts as the main label for the radio group
        st.subheader("👥 Select Supplier") 
        
        # Use format_func to show more info in the radio list
        def format_supplier_label(supplier_id):
            s = get_supplier_by_id(supplier_id)
            if not s: return "Unknown Supplier"
            label = f"{s.get('name', 'N/A')}"
            rating = s.get('rating')
            if rating: label += f" ({rating}⭐)"
            specialties = s.get('specialties')
            if specialties: label += f" - Specializes in: {', '.join(specialties)}"
            return label

        # Use label_visibility="collapsed" as the subheader provides context
        selected_supplier_id = st.radio(
            "Select a supplier:", # Internal label, hidden by visibility setting
            options=[s['id'] for s in suppliers],
            format_func=format_supplier_label,
            key="supplier_select_radio",
            label_visibility="collapsed" 
        )
        st.session_state.selected_supplier_id = selected_supplier_id # Update state immediately

    # --- Detailed View & Specific AI Insight --- 
    with col2:
        if st.session_state.selected_supplier_id:
            selected_supplier = get_supplier_by_id(st.session_state.selected_supplier_id)
            if selected_supplier:
                st.subheader(f"🔍 Details for {selected_supplier['name']}")
                
                # Card for details - add animation class to the container
                with st.container():
                    # Add animation class directly to the card div
                    st.markdown("<div class='card animate-slideUpFadeIn'>", unsafe_allow_html=True)
                    st.markdown(f"**Rating:** {selected_supplier.get('rating', 'N/A')} / 5")
                    st.markdown(f"**Specialties:** {', '.join(selected_supplier.get('specialties', ['N/A']))}")
                    st.markdown(f"**Min. Order Qty:** {selected_supplier.get('minimum_order_qty', 'N/A')}")
                    st.markdown(f"**Location:** {selected_supplier.get('location', 'N/A')}")
                    st.markdown(f"**Contact:** {selected_supplier.get('contact_email', 'N/A')}")
                    notes = selected_supplier.get('notes', '')
                    if notes:
                        st.markdown("--- ")
                        st.markdown(f"*Notes: {notes}*", help="Additional notes about this supplier")
                    st.markdown("</div>", unsafe_allow_html=True)

                # --- AI Insight for Selected Supplier (Run when selection changes) ---
                if selected_supplier['id'] != st.session_state.last_analyzed_supplier_id:
                    with st.spinner(f"🤔 Analyzing fit for {selected_supplier['name']}..."):
                        prompt = f"""
                        Analyze the specific fit between supplier **{selected_supplier['name']}** (Specialties: {selected_supplier.get('specialties', 'N/A')}, Min Qty: {selected_supplier.get('minimum_order_qty', 'N/A')}) and the order for **{quantity} units of \"{product_name}\"**.
                        
                        Consider:
                        1.  Specialty Match: How well do they match the product?
                        2.  Quantity Feasibility: Does the order meet their minimum?
                        3.  Pros/Cons: Any key advantages (e.g., location) or risks?
                        4.  Suggested Question: Ask 1 specific question relevant to this order.
                        
                        Keep the response concise, actionable, using Markdown.
                        """
                        message_history = [
                            {"role": "system", "content": "You are a procurement expert providing specific, actionable insights on a chosen supplier's suitability for a specific Kirana store order."},
                            {"role": "user", "content": prompt}
                        ]
                        try:
                            insights = generate_completion(message_history)
                            st.session_state.current_supplier_insights = insights
                            st.session_state.last_analyzed_supplier_id = selected_supplier['id']
                        except Exception as e:
                            st.session_state.current_supplier_insights = f"*Error getting insights: {e}*"
                    st.rerun() # Rerun to display the new insight

                # Display specific insights
                if st.session_state.current_supplier_insights:
                    st.write("") # Spacer
                    st.markdown("**💡 AI Insight on Selection:**")
                    # Add animation class
                    st.markdown(f"<div class='ai-insight-box animate-slideUpFadeIn delay-1'>{st.session_state.current_supplier_insights}</div>", unsafe_allow_html=True)
            else:
                st.error("Selected supplier details could not be loaded.")
        else:
            st.info("Select a supplier from the list on the left to see details and specific AI insights.")

    # --- Navigation Button --- 
    st.markdown("--- ")
    col1, col2 = st.columns([4, 1]) # Align button to the right
    with col2:
        # Disable button if no supplier is effectively selected
        next_disabled = st.session_state.selected_supplier_id is None
        if st.button("Initial Message →", type="primary", use_container_width=True, disabled=next_disabled):
            # Clear next step's state
            st.session_state['initial_message_content'] = None
            st.session_state['initial_message_sent'] = False
            st.session_state['current_step'] = 2
            st.rerun() 