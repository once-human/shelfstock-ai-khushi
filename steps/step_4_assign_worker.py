import streamlit as st
from utils.data_handler import get_available_workers

def render_assign_worker():
    """Render the assign worker step where a worker is assigned to handle the order."""
    st.header("Step 4: Assign Worker")
    
    # Get available workers
    available_workers = get_available_workers()
    
    if not available_workers:
        st.error("No workers are currently available. Please try again later.")
        return
    
    # Create selection options
    worker_options = {
        f"{w['name']} (Tasks: {w['current_tasks']})": w['id'] 
        for w in available_workers
    }
    
    # Worker selection
    selected_worker_name = st.selectbox(
        "Select Available Worker",
        options=list(worker_options.keys()),
        index=None,
        placeholder="Choose a worker..."
    )
    
    if selected_worker_name:
        selected_worker_id = worker_options[selected_worker_name]
        worker = next((w for w in available_workers if w['id'] == selected_worker_id), None)
        
        # Show worker details
        st.info(f"Selected: {worker['name']}")
        st.write(f"Current tasks: {worker['current_tasks']}")
        st.write(f"Role: {worker['role']}")
        
        # Assign worker button
        if st.button("Assign Worker"):
            st.session_state['selected_worker_id'] = selected_worker_id
            st.success(f"Successfully assigned {worker['name']} to this order!")
            st.session_state['current_step'] = 5 