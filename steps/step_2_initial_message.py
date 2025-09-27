import streamlit as st
from utils.data_handler import get_supplier_by_id
from code_library.openai_api_helper import generate_completion
# from utils.email_handler import send_email # No longer sending real email
# Configuration handled via st.secrets
import time

def render_initial_message():
    """Render the initial message step with AI generation and improved layout/styling."""
    st.header("Step 2: Generate Initial Inquiry Message")

    # --- Data Validation ---
    supplier_id = st.session_state.get('selected_supplier_id')
    if not supplier_id:
        st.error("No supplier selected. Please go back to Step 1.")
        if st.button("← Back to Supplier Selection"):
            st.session_state['current_step'] = 1
            st.rerun()
        return
        
    supplier = get_supplier_by_id(supplier_id)
    if not supplier:
        st.error(f"Could not find details for supplier ID: {supplier_id}")
        if st.button("← Back to Supplier Selection"):
            st.session_state['current_step'] = 1
            st.rerun()
        return

    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    supplier_email = supplier.get('contact_email')
    supplier_name = supplier.get('name', 'Supplier')

    st.write(f"Use the AI to draft an initial inquiry message for **{supplier_name}** about **{quantity} x {product_name}**, or edit the draft yourself.")
    st.markdown("--- ")

    # Initialize state for this step
    if 'initial_message_content' not in st.session_state:
        st.session_state.initial_message_content = None
    if 'initial_message_sent' not in st.session_state:
        st.session_state.initial_message_sent = False

    # --- Message Generation (runs only once until sent or regenerated) ---
    if st.session_state.initial_message_content is None and not st.session_state.initial_message_sent:
        with st.spinner("🤖 Asking AI to draft the inquiry message..."):
            prompt_sections = [
                f"Generate a polite and professional initial inquiry message to the supplier '{supplier_name}' for a Kirana store order.",
                f"\n**Order Context:**",
                f"- Product: {product_name}",
                f"- Quantity: {quantity}",
                f"\n**Key Information to Request:**",
                "- Detailed product specifications",
                "- Availability confirmation",
                "- Estimated lead time",
                "- Pricing/quote process",
                "- Relevant quality standards/certifications (e.g., FSSAI)",
                "- Packaging options/details",
                "- Delivery logistics/costs",
                "- Payment terms & conditions",
                f"\n**Formatting Instructions:**",
                f"- Start with \"Dear {supplier_name},\"",
                f"- State the order interest ('{quantity} units of {product_name}') clearly in the first paragraph.",
                "- Maintain a professional, courteous tone suitable for business communication.",
                "- Structure requests clearly, perhaps using bullet points for readability if appropriate.",
                "- End *only* with the exact signature block below (no extra closing remarks):",
                "\nBest regards,\n\nKhushi Banthia\nOwner\nBanthia's Quick Store\nkhushibanthia19@gmail.com"
            ]
            prompt = "\n".join(prompt_sections)
            
            message_history = [
                {"role": "system", "content": "You draft concise, professional supplier inquiry emails for Indian Kirana store owners. Ensure all requested details are covered, the tone is appropriate, and follow formatting instructions precisely, especially the signature."},
                {"role": "user", "content": prompt}
            ]
            try:
                generated_message = generate_completion(message_history)
                st.session_state.initial_message_content = generated_message.strip()
                st.rerun() # Rerun immediately to display the draft
            except Exception as e:
                st.error(f"⚠️ Failed to generate message: {e}")
                # Keep content as None so the user sees the error and the generation doesn't block progress
                st.session_state.initial_message_content = "" # Provide empty string to allow editing

    # --- Display Message Preview & Actions --- 
    elif not st.session_state.initial_message_sent:
        st.subheader("📧 Message Preview & Edit")
        
        # Use a container to apply card styling implicitly if needed, or just layout
        with st.container(): 
            message_body = st.text_area(
                "Message Body (Editable)", 
                value=st.session_state.initial_message_content, 
                height=400, # Increased height
                key="initial_message_edit_area",
                help="Review and edit the AI-drafted message before sending."
            )
            # Update state immediately if user edits
            st.session_state.initial_message_content = message_body
            
            st.write("") # Spacer
            
            # Simulated recipient info
            if supplier_email:
                 st.caption(f"Simulated send to: {supplier_email}")
            else:
                 st.caption(f"Warning: No contact email found for {supplier_name}")

        st.markdown("--- ")
        # --- Buttons --- 
        # Place buttons below the text area
        col1, col2, _ = st.columns([1, 2, 3]) # Buttons left-aligned
        with col1:
            # Use secondary style for regenerate
            if st.button("🔄 Regenerate", key="regenerate_initial_msg", type="secondary", help="Ask AI to draft a new message"):
                st.session_state.initial_message_content = None # Clear content to trigger regeneration
                st.rerun()
        with col2:
             if st.button("Confirm & Simulate Send →", type="primary", help="Mark message as sent and proceed"):
                # Content is already up-to-date in session state due to text_area key
                with st.spinner(f"Simulating sending inquiry to {supplier_name}..."):
                    time.sleep(1.2) # Slightly shorter sleep
                
                st.success(f"✅ Inquiry marked as sent to {supplier_name}.")
                st.session_state.initial_message_sent = True
                time.sleep(0.8) # Short delay for feedback
                # Clear next step state before moving
                st.session_state['supplier_response'] = None
                st.session_state['current_step'] = 3
                st.rerun()

    # --- Show Sent Confirmation --- 
    elif st.session_state.initial_message_sent:
        st.success(f"✅ Inquiry successfully marked as sent to **{supplier_name}**.")
        st.info("Proceed to the next step to await their response.")
        st.markdown("--- ")
        col1, col2 = st.columns([4,1]) # Align button right
        with col2:
            if st.button("Await Response →", type="primary", use_container_width=True):
                 st.session_state['current_step'] = 3
                 st.rerun() 