import streamlit as st
from utils.data_handler import get_available_workers, get_supplier_by_id
from code_library.openai_api_helper import generate_completion

def render_assign_worker():
    """Render the worker assignment step with AI-powered matching."""
    st.header("Step 4: Assign Worker")
    
    # Get order details from session state
    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    supplier_id = st.session_state.get('selected_supplier_id')
    supplier = get_supplier_by_id(supplier_id)
    
    if not supplier:
        st.error("Supplier information not found. Please go back and select a supplier.")
        return
    
    # Get available workers
    workers = get_available_workers()
    
    if not workers:
        st.error("No available workers found.")
        return

    # Initialize AI recommendation state
    if 'worker_recommendations' not in st.session_state:
        st.session_state['worker_recommendations'] = None

    # Get AI recommendations for worker assignment
    if not st.session_state.get('worker_recommendations'):
        with st.spinner("Analyzing best worker matches..."):
            # Create detailed worker information for analysis
            workers_info = "\n".join([
                f"Worker {i+1}: {w['name']}\n"
                f"- Role: {w.get('role', 'N/A')}\n"
                f"- Experience: {w.get('experience', 'N/A')} years\n"
                f"- Specialties: {w.get('specialties', 'N/A')}\n"
                for i, w in enumerate(workers)
            ])
            
            prompt = f"""
            Analyze the best worker matches for this order:
            
            Order Details:
            - Product: {product_name}
            - Quantity: {quantity}
            - Supplier: {supplier['name']}
            
            Available Workers:
            {workers_info}
            
            Provide:
            1. Ranked list of recommended workers
            2. Reasoning for each recommendation
            3. Specific strengths for handling this order
            
            Format as a clear, bulleted list.
            """
            
            message_history = [
                {"role": "system", "content": "You are an HR expert who matches workers to orders based on their expertise and the order requirements."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                recommendations = generate_completion(message_history)
                st.session_state['worker_recommendations'] = recommendations
            except Exception as e:
                st.error(f"Could not generate worker recommendations: {e}")

    # Display AI recommendations
    if st.session_state.get('worker_recommendations'):
        with st.expander("🎯 AI Worker Recommendations", expanded=True):
            st.markdown(st.session_state['worker_recommendations'])

    # Display worker selection with enhanced UI
    st.subheader("Select a Worker")
    
    # Create selectbox for worker selection with formatted options
    worker_options = []
    for worker in workers:
        experience = worker.get('experience', 'N/A')
        specialties = worker.get('specialties', 'N/A')
        label = f"{worker['name']} ({worker.get('role', 'Staff')})"
        if experience != 'N/A':
            label += f" - {experience} years exp."
        worker_options.append(label)

    selected_index = st.selectbox(
        "Available Workers",
        range(len(workers)),
        format_func=lambda x: worker_options[x],
        key="worker_selectbox"
    )

    selected_worker = workers[selected_index]

    # Display detailed worker information
    with st.expander("👤 Detailed Worker Information", expanded=True):
        st.markdown(f"""
        ### {selected_worker['name']}
        
        **Role:** {selected_worker.get('role', 'N/A')}  
        **Experience:** {selected_worker.get('experience', 'N/A')} years  
        **Specialties:** {selected_worker.get('specialties', 'N/A')}  
        **Status:** {'🟢 Available' if selected_worker.get('available', True) else '🔴 Unavailable'}
        
        {selected_worker.get('bio', '')}
        """)

    # Get AI insights for the selected worker
    if selected_worker['id'] != st.session_state.get('last_analyzed_worker_id'):
        with st.spinner("Getting AI insights for selected worker..."):
            prompt = f"""
            Analyze the fit between worker "{selected_worker['name']}" and this order:
            - Product: {product_name}
            - Quantity: {quantity}
            - Supplier: {supplier['name']}
            
            Consider:
            1. Worker's expertise and experience
            2. Potential strengths and challenges
            3. Specific recommendations for handling this order
            
            Keep the response concise and actionable.
            """
            
            message_history = [
                {"role": "system", "content": "You are an HR expert who provides specific insights about worker-order fit."},
                {"role": "user", "content": prompt}
            ]
            
            try:
                worker_insights = generate_completion(message_history)
                st.session_state['current_worker_insights'] = worker_insights
                st.session_state['last_analyzed_worker_id'] = selected_worker['id']
            except Exception as e:
                st.error(f"Could not generate worker insights: {e}")

    # Display worker-specific AI insights
    if st.session_state.get('current_worker_insights'):
        with st.expander("💡 AI Worker Insights", expanded=True):
            st.markdown(st.session_state['current_worker_insights'])

    # Next button
    if st.button("Next Step", type="primary"):
        st.session_state['selected_worker_id'] = selected_worker['id']
        st.session_state['current_step'] = 5
        st.rerun() 