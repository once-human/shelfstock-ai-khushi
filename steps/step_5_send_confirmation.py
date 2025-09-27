import streamlit as st
from utils.data_handler import get_supplier_by_id, get_worker_by_id
from code_library.openai_api_helper import generate_completion
# from utils.email_handler import send_email # No longer sending real email
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configs
import time

def render_send_confirmation():
    """Render the send confirmation step with AI generation and improved layout."""
    st.header("Step 5: Send Order Confirmation")

    # --- Data Validation & Context ---
    supplier_id = st.session_state.get('selected_supplier_id')
    worker_id = st.session_state.get('selected_worker_id')

    if not supplier_id or not worker_id:
        st.error("Missing supplier or worker selection. Please go back to previous steps.")
        if st.button("← Back to Assign Worker"):
            st.session_state['current_step'] = 4
            st.rerun()
        return
        
    supplier = get_supplier_by_id(supplier_id)
    worker = get_worker_by_id(worker_id)
    
    if not supplier or not worker:
        st.error("Could not retrieve supplier or worker details.")
        if st.button("← Back to Assign Worker"):
            st.session_state['current_step'] = 4
            st.rerun()
        return

    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    supplier_email = supplier.get('contact_email')
    supplier_name = supplier.get('name', 'Supplier')
    worker_name = worker.get('name', 'Assigned Contact')
    worker_role = worker.get('role', 'Staff')

    st.write(f"Use the AI to draft the final order confirmation message for **{supplier_name}**. The assigned internal contact is **{worker_name} ({worker_role})**.")
    st.markdown("--- ")

    # Initialize state for this step
    if 'confirmation_message_content' not in st.session_state:
        st.session_state.confirmation_message_content = None
    if 'confirmation_message_sent' not in st.session_state:
        st.session_state.confirmation_message_sent = False

    # --- Message Generation (runs once until sent or regenerated) ---
    if st.session_state.confirmation_message_content is None and not st.session_state.confirmation_message_sent:
        with st.spinner("🤖 Asking AI to draft the confirmation message..."):
            prompt_sections = [
                f"Generate a polite and professional order confirmation message to the supplier '{supplier_name}' for a Kirana store.",
                f"\n**Order Details to Confirm:**",
                f"- Product: {product_name}",
                f"- Quantity: {quantity}",
                f"- Assigned Internal Contact: {worker_name} ({worker_role})",
                f"\n**Instructions:**",
                f"- Start with \"Dear {supplier_name},\"",
                f"- Clearly confirm the order for '{quantity} units of {product_name}'.",
                f"- State that '{worker_name}' is the primary point of contact.",
                "- Express appreciation for their business.",
                "- Maintain a professional and positive tone.",
                "- End *only* with the exact signature block below:",
                "\nBest regards,\n\nKhushi Banthia\nOwner\nBanthia's Quick Store\nkhushibanthia19@gmail.com"
            ]
            prompt = "\n".join(prompt_sections)
            
            message_history = [
                {"role": "system", "content": "You draft professional Kirana store order confirmation emails. Be clear, concise, mention the assigned contact, and follow formatting instructions precisely, especially the signature."},
                {"role": "user", "content": prompt}
            ]
            try:
                generated_message = generate_completion(message_history)
                st.session_state.confirmation_message_content = generated_message.strip()
                st.rerun()
            except Exception as e:
                st.error(f"⚠️ Failed to generate confirmation message: {e}")
                st.session_state.confirmation_message_content = "" # Allow editing even if generation fails

    # --- Display Confirmation Preview & Actions --- 
    elif not st.session_state.confirmation_message_sent:
        st.subheader("📧 Confirmation Message Preview & Edit")
        
        with st.container():
            message_body = st.text_area(
                "Confirmation Message Body (Editable)", 
                value=st.session_state.confirmation_message_content, 
                height=400, 
                key="confirmation_message_edit_area",
                help="Review and edit the AI-drafted confirmation before sending."
            )
            # Update state immediately on edit
            st.session_state.confirmation_message_content = message_body
            
            st.write("") # Spacer
            if supplier_email:
                 st.caption(f"Simulated send to: {supplier_email}")
            else:
                 st.caption(f"Warning: No contact email found for {supplier_name}")

        st.markdown("--- ")
        # --- Buttons --- 
        col1, col2, _ = st.columns([1, 2, 3]) # Buttons left-aligned
        with col1:
             # Secondary style for regenerate
            if st.button("🔄 Regenerate", key="regenerate_confirm_msg", type="secondary"):
                st.session_state.confirmation_message_content = None
                st.rerun()
        with col2:
            if st.button("Confirm & Complete Order →", type="primary"):
                # Content is already up-to-date
                with st.spinner(f"Simulating sending confirmation to {supplier_name}..."):
                    time.sleep(1.2)
                
                st.success(f"✅ Confirmation marked as sent to {supplier_name}. Order process complete!")
                st.session_state.confirmation_message_sent = True
                time.sleep(0.8)
                # Clear state for next step if necessary (though step 6 reads from state)
                st.session_state['current_step'] = 6
                st.rerun()
                
    # --- Show Sent Confirmation --- 
    elif st.session_state.confirmation_message_sent:
        st.success(f"✅ Confirmation successfully marked as sent to **{supplier_name}**. Order process complete!")
        st.info("View the final order summary below or start a new order.")
        st.markdown("--- ")
        col1, col2 = st.columns([4,1]) # Align button right
        with col2:
            # Button to explicitly go to summary (optional, could auto-scroll)
            if st.button("View Summary →", type="primary", use_container_width=True):
                 st.session_state['current_step'] = 6
                 st.rerun() 