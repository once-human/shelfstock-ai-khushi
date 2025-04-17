import streamlit as st
from utils.data_handler import get_supplier_by_id, get_worker_by_id # Use DB functions
from code_library.openai_api_helper import generate_completion
from utils.email_handler import send_email # Import email sender
import configs
import time

def render_send_confirmation():
    """Render the send confirmation step: AI drafts message, user confirms, email sent."""
    st.header("Step 5: Send Order Confirmation")
    
    supplier_id = st.session_state.get('selected_supplier_id')
    worker_id = st.session_state.get('selected_worker_id')
    
    supplier = get_supplier_by_id(supplier_id)
    worker = get_worker_by_id(worker_id)
    
    if not supplier or not worker:
        st.error("Missing supplier or worker information. Please restart the process or go back.")
        return

    product_name = st.session_state.get('product_name')
    quantity = st.session_state.get('quantity')
    supplier_email = supplier.get('contact_email')

    # State for confirmation generation and sending
    if 'confirmation_message_content' not in st.session_state:
        st.session_state['confirmation_message_content'] = None
    if 'confirmation_message_sent' not in st.session_state:
        st.session_state['confirmation_message_sent'] = False

    # --- 1. Generate Confirmation (if not done) ---
    if st.session_state['confirmation_message_content'] is None and not st.session_state['confirmation_message_sent']:
        st.subheader("AI Confirmation Generation")
        st.write(f"Drafting order confirmation for **{supplier['name']}** regarding **{quantity} x {product_name}**...")
        
        prompt = f"""
        Generate a polite and professional order confirmation email to be sent to a supplier.
        
        **Order Details:**
        - Product: {product_name}
        - Quantity: {quantity}
        - Supplier Name: {supplier['name']}
        - Assigned Internal Contact: {worker['name']} ({worker.get('role', '')})
        
        **Instructions:**
        - Keep the tone professional and appreciative.
        - Confirm the specific product and quantity ordered.
        - State that the order is confirmed and provide the name/role of the internal contact person ({worker['name']}).
        - Thank the supplier for their business.
        - Do NOT include a subject line.
        - Do NOT include salutations or closings.
        """
        message_history = [
            {"role": "system", "content": "You draft concise, professional supplier order confirmation emails."},
            {"role": "user", "content": prompt}
        ]

        try:
            with st.spinner("Asking AI to draft the confirmation..."):
                generated_confirmation = generate_completion(message_history)
            st.session_state['confirmation_message_content'] = generated_confirmation.strip()
            st.rerun()
        except Exception as e:
            st.error(f"Failed to generate confirmation using AI: {e}")
            st.session_state['confirmation_message_content'] = "Error generating confirmation."

    # --- 2. Display Confirmation and Send Button (if generated, not sent) ---
    elif st.session_state['confirmation_message_content'] is not None and not st.session_state['confirmation_message_sent']:
        st.subheader("Confirmation Preview (Drafted by AI)")
        confirmation_body = st.session_state['confirmation_message_content']
        st.text_area("Email Body", value=confirmation_body, height=300, key="confirmation_message_display")
        
        if not supplier_email:
            st.warning(f"Supplier {supplier['name']} does not have a contact email in the database. Cannot send email.", icon="⚠️")
        else:
            st.write(f"**Recipient:** {supplier_email}")
            subject = f"Order Confirmation: {quantity} x {product_name}"
            st.write(f"**Subject:** {subject}")
            
            # Button to actually send the email
            if st.button("Send Confirmation Email", type="primary", disabled=(not supplier_email)):
                with st.spinner(f"Sending confirmation to {supplier_email}..."):
                    success = send_email(
                        recipient_email=supplier_email, 
                        subject=subject, 
                        body=confirmation_body
                    )
                
                if success:
                    st.success(f"Confirmation email sent successfully to {supplier['name']}.")
                    st.session_state['confirmation_message_sent'] = True
                    time.sleep(2)
                    st.session_state['current_step'] = 6
                    st.rerun()
                # Error handled in send_email
                
    # --- 3. Show Sent Confirmation (if sent) ---
    elif st.session_state['confirmation_message_sent']:
        st.success(f"Confirmation email sent to {supplier.get('name', 'supplier')}. Order complete!")
        if st.button("View Summary", type="primary"):
             st.session_state['current_step'] = 6
             st.rerun() 