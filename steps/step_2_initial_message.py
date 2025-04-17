import streamlit as st
from utils.data_handler import get_supplier_by_id # Use new DB function
from code_library.openai_api_helper import generate_completion
from utils.email_handler import send_email # Import email sender
import configs
import time

def render_initial_message():
    """Render the initial message step: generate message with AI, then send it via email."""
    st.header("Step 2: Send Initial Message")
    
    supplier_id = st.session_state.get('selected_supplier_id')
    supplier = get_supplier_by_id(supplier_id) # Fetch from DB
    
    if not supplier:
        st.error("Supplier details not found. Please go back and select a supplier.")
        # Optionally add a button to go back
        # if st.button("Go Back"): 
        #     st.session_state['current_step'] = 1
        #     st.rerun()
        return

    product_name = st.session_state.get('product_name')
    quantity = st.session_state.get('quantity')
    supplier_email = supplier.get('contact_email')

    # State for message generation and sending status
    if 'initial_message_content' not in st.session_state:
        st.session_state['initial_message_content'] = None
    if 'initial_message_sent' not in st.session_state:
        st.session_state['initial_message_sent'] = False

    # --- 1. Generate Message (if not already done) ---
    if st.session_state['initial_message_content'] is None and not st.session_state['initial_message_sent']:
        st.subheader("AI Message Generation")
        st.write(f"Drafting order inquiry for **{supplier['name']}** regarding **{quantity} x {product_name}**...")
        
        prompt = f"""
        Generate a polite and professional email message to a supplier to inquire about placing an order.
        
        **Supplier Details:**
        - Name: {supplier['name']}
        
        **Order Details:**
        - Product: {product_name}
        - Quantity: {quantity}

        **Instructions:**
        - Keep the tone professional and courteous.
        - Clearly state the product and quantity.
        - Ask for confirmation of availability, estimated lead time, and pricing/quote process.
        - Do NOT include a subject line (it will be added separately).
        - Do NOT include salutations like 'Dear [Name]' or closings like 'Best regards'. The email system will handle those.
        - Assume the recipient knows your company.
        """
        message_history = [
            {"role": "system", "content": "You draft concise, professional supplier inquiry emails."},
            {"role": "user", "content": prompt}
        ]

        try:
            with st.spinner("Asking AI to draft the message..."):
                generated_message = generate_completion(message_history)
            st.session_state['initial_message_content'] = generated_message.strip()
            st.rerun()
        except Exception as e:
            st.error(f"Failed to generate message using AI: {e}")
            st.session_state['initial_message_content'] = "Error generating message."

    # --- 2. Display Message and Send Button (if generated, not sent) ---
    elif st.session_state['initial_message_content'] is not None and not st.session_state['initial_message_sent']:
        st.subheader("Message Preview (Drafted by AI)")
        message_body = st.session_state['initial_message_content']
        st.text_area("Email Body", value=message_body, height=250, key="initial_message_display")
        
        if not supplier_email:
             st.warning(f"Supplier {supplier['name']} does not have a contact email in the database. Cannot send email.", icon="⚠️")
        else:
            st.write(f"**Recipient:** {supplier_email}")
            subject = f"Order Inquiry: {quantity} x {product_name}"
            st.write(f"**Subject:** {subject}")

            # Button to actually send the email
            if st.button("Send Inquiry Email", type="primary", disabled=(not supplier_email)):
                with st.spinner(f"Sending email to {supplier_email}..."):
                    success = send_email(
                        recipient_email=supplier_email, 
                        subject=subject, 
                        body=message_body
                    )
                
                if success:
                    st.success(f"Inquiry email sent successfully to {supplier['name']}.")
                    st.session_state['initial_message_sent'] = True
                    # Optionally add a small delay before auto-advancing
                    time.sleep(2)
                    st.session_state['current_step'] = 3
                    st.rerun()
                # Error message is handled within send_email

    # --- 3. Show Sent Confirmation (if sent) ---
    elif st.session_state['initial_message_sent']:
        st.success(f"Inquiry email sent to {supplier.get('name', 'supplier')}. Proceeding to next step.")
        # Auto-advance or provide manual button
        if st.button("Next: Await Response", type="primary"):
             st.session_state['current_step'] = 3
             st.rerun() 