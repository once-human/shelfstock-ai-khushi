import streamlit as st
from utils.data_handler import get_available_workers, get_supplier_by_id, get_worker_by_id
from code_library.openai_api_helper import generate_completion

def render_assign_worker():
    """Render the worker assignment step with improved layout and AI matching."""
    st.header("Step 4: Assign Internal Worker")

    # --- Data Validation & Context ---
    if st.session_state.get('supplier_response') != 'Accepted':
        st.warning("Cannot assign worker: Supplier has not accepted the order yet (Step 3).")
        if st.button("← Back to Await Response"):
            st.session_state['current_step'] = 3
            st.rerun()
        return

    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    supplier_id = st.session_state.get('selected_supplier_id')
    supplier = get_supplier_by_id(supplier_id)
    supplier_name = supplier.get('name', 'the supplier') if supplier else 'Unknown Supplier'

    if not product_name or not supplier: # Basic check
        st.error("Missing order context (Product/Supplier). Please restart.")
        if st.button("Restart Order"):
            from utils.state_management import reset_state
            reset_state()
            st.rerun()
        return

    st.write(f"Assign an internal team member to manage the accepted order for **{quantity} x {product_name}** from **{supplier_name}**.")
    st.markdown("--- ")

    # --- Load Workers --- 
    workers = get_available_workers()
    if not workers:
        st.error("No available workers found in the system. Cannot proceed.")
        # Consider adding a way to manually enter worker info or skip?
        return

    # --- Initialize State for this Step --- 
    for key in ['worker_recommendations', 'current_worker_insights', 'last_analyzed_worker_id', 'selected_worker_id']:
        if key not in st.session_state:
             st.session_state[key] = None

    # --- AI Worker Matching (Run once) ---
    if st.session_state.worker_recommendations is None:
        with st.spinner("🧠 Analyzing worker suitability for this order..."):
            workers_info = "\n".join([
                f"- ID: {w['id']}, Name: {w['name']}, Role: {w.get('role', 'N/A')}, Expertise: {w.get('expertise', 'N/A')}, Tasks: {w.get('current_tasks', 'N/A')}"
                for w in workers
            ])
            
            prompt = f"""
            Analyze the best worker matches for managing this Kirana store order:
            
            **Order Context:**
            - Product: {product_name}
            - Quantity: {quantity}
            - Supplier: {supplier_name}
            
            **Available Workers (ID, Name, Role, Expertise, Current Tasks):**
            {workers_info}
            
            Based *only* on the provided info, provide:
            1.  **Top 2-3 Recommended Workers:** List Names & IDs.
            2.  **Reasoning:** Briefly explain why each is a good fit (expertise match, workload).
            3.  **Concerns:** Note potential issues (workload, expertise gap).
            
            Format concisely using Markdown. If none seem suitable, state that.
            """
            message_history = [
                {"role": "system", "content": "You are an operations manager for a Kirana store. Match workers to orders based *only* on provided details (role, expertise, tasks) and order context. Provide clear recommendations/concerns."},
                {"role": "user", "content": prompt}
            ]
            try:
                recommendations = generate_completion(message_history)
                st.session_state.worker_recommendations = recommendations
                st.rerun() # Rerun to show results
            except Exception as e:
                st.session_state.worker_recommendations = f"*Error analyzing workers: {e}*"

    # --- Display Recommendations & Selection --- 
    col1, col2 = st.columns([3, 2]) # Adjust ratio

    with col1:
        st.subheader("🎯 AI Matching Analysis")
        if st.session_state.worker_recommendations:
            st.markdown(f"<div class='ai-insight-box animate-slideUpFadeIn'>{st.session_state.worker_recommendations}</div>", unsafe_allow_html=True)
        else:
            st.info("AI analysis failed or is processing.")
        
        st.write("")
        st.subheader("🧑‍🔧 Select Worker to Assign")
        
        def format_worker_label(worker_id):
            w = get_worker_by_id(worker_id)
            if not w: return "Unknown Worker"
            label = f"{w.get('name', 'N/A')}"
            role = w.get('role')
            tasks = w.get('current_tasks', -1)
            if role: label += f" ({role})"
            if tasks >= 0: label += f" - {tasks} tasks"
            return label

        selected_worker_id = st.radio(
            "Assign this order to:",
            options=[w['id'] for w in workers],
            format_func=format_worker_label,
            key="worker_select_radio",
            # label_visibility="collapsed"
        )
        st.session_state.selected_worker_id = selected_worker_id # Update state

    # --- Details & Specific AI Insight --- 
    with col2:
        if st.session_state.selected_worker_id:
            selected_worker = get_worker_by_id(st.session_state.selected_worker_id)
            if selected_worker:
                st.subheader(f"👤 Details for {selected_worker.get('name', 'Worker')}")
                with st.container():
                    st.markdown("<div class='card animate-slideUpFadeIn'>", unsafe_allow_html=True)
                    st.markdown(f"**Role:** {selected_worker.get('role', 'N/A')}")
                    st.markdown(f"**Expertise:** {', '.join(selected_worker.get('expertise', ['N/A']))}")
                    st.markdown(f"**Current Tasks:** {selected_worker.get('current_tasks', 'N/A')}")
                    availability = selected_worker.get('availability')
                    status_text = '<span style="color: var(--success-green);">Available</span>' if availability else '<span style="color: var(--danger-red);">Busy</span>'
                    st.markdown(f"**Status:** {status_text}", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # --- AI Insight for Selected Worker --- 
                if selected_worker['id'] != st.session_state.last_analyzed_worker_id:
                    with st.spinner(f"🤔 Analyzing {selected_worker.get('name', 'worker')}'s fit..."):
                        prompt = f"""
                        Analyze specific fit: **{selected_worker.get('name', 'Worker')}** (Role: {selected_worker.get('role', 'N/A')}, Expertise: {selected_worker.get('expertise', 'N/A')}, Tasks: {selected_worker.get('current_tasks', 'N/A')}) managing order for **{quantity} x \"{product_name}\"** from **{supplier_name}**.
                        
                        Consider:
                        1.  Expertise Match: How relevant is their expertise?
                        2.  Workload: Is {selected_worker.get('current_tasks', 'N/A')} tasks manageable?
                        3.  Pros/Cons: Specific strengths or challenges for *this* order.
                        4.  Key Action: Suggest 1 specific action for them.
                        
                        Keep response concise, actionable, use Markdown.
                        """
                        message_history = [
                            {"role": "system", "content": "You are an operations manager providing specific, actionable insights for assigning a chosen worker to a Kirana store order."},
                            {"role": "user", "content": prompt}
                        ]
                        try:
                            insights = generate_completion(message_history)
                            st.session_state.current_worker_insights = insights
                            st.session_state.last_analyzed_worker_id = selected_worker['id']
                        except Exception as e:
                            st.session_state.current_worker_insights = f"*Error getting insights: {e}*"
                    st.rerun() # Rerun to display

                # Display specific insights
                if st.session_state.current_worker_insights:
                    st.write("") # Spacer
                    st.markdown("**💡 AI Insight on Selection:**")
                    st.markdown(f"<div class='ai-insight-box animate-slideUpFadeIn delay-1'>{st.session_state.current_worker_insights}</div>", unsafe_allow_html=True)
            else:
                st.error("Selected worker details could not be loaded.")
        else:
            st.info("Select a worker from the list on the left to see details and specific AI insights.")

    # --- Navigation --- 
    st.markdown("--- ")
    col1, col2 = st.columns([4, 1]) # Align button right
    with col2:
        next_disabled = st.session_state.selected_worker_id is None
        if st.button("Gen Confirmation →", type="primary", use_container_width=True, disabled=next_disabled, help="Proceed to generate confirmation message"):
            # Clear next step's state
            st.session_state['confirmation_message_content'] = None
            st.session_state['confirmation_message_sent'] = False
            st.session_state['current_step'] = 5
            st.rerun() 