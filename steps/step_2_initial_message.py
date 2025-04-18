import streamlit as st
from utils.data_handler import get_supplier_by_id
from code_library.openai_api_helper import generate_completion
# from utils.email_handler import send_email # No longer sending real email
import configs
import time

def render_initial_message():
    """Render the initial message step: generate message with AI, then simulate sending."""
    st.header("Step 2: Generate Initial Message") # Renamed header for clarity
    
    supplier_id = st.session_state.get('selected_supplier_id')
    supplier = get_supplier_by_id(supplier_id)
    
    if not supplier:
        st.error("Supplier details not found. Please go back and select a supplier.")
        return

    product_name = st.session_state.get('product_name')
    quantity = st.session_state.get('quantity')
    supplier_email = supplier.get('contact_email') # Still useful to display

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
        Generate a polite and professional message to a supplier to inquire about placing an order.
        
        **Supplier Details:**
        - Name: {supplier['name']}
        
        **Order Details:**
        - Product: {product_name}
        - Quantity: {quantity}

        **Instructions:**
        - Keep the tone professional and courteous.
        - Clearly state the product and quantity.
        - Ask for confirmation of availability, estimated lead time, and pricing/quote process.
        - Assume the recipient knows your company.
        """
        message_history = [
            {"role": "system", "content": "You draft concise, professional supplier inquiry messages."},
            {"role": "user", "content": prompt}
        ]

        try:
            with st.spinner("Asking AI to draft the message..."):
                generated_message = generate_completion(message_history)
            st.session_state['initial_message_content'] = generated_message.strip()
            st.rerun()
        except Exception as e:
            st.error(f"Failed to generate message using AI: {e}")
            st.session_state['initial_message_content'] = f"Error generating message: {e}"

    # --- 2. Display Message and Simulate Send Button (if generated, not sent) ---
    elif st.session_state['initial_message_content'] is not None and not st.session_state['initial_message_sent']:
        st.subheader("Message Preview (Drafted by AI)")
        message_body = st.session_state['initial_message_content']
        st.text_area("Message Body", value=message_body, height=250, key="initial_message_display")
        
        if supplier_email:
             st.write(f"(Simulating send to: {supplier_email})")
        else:
             st.warning(f"No contact email found for {supplier['name']}, but proceeding with simulation.", icon="⚠️")

        # Button to simulate sending the email
        if st.button("Confirm and Proceed (Simulate Send)", type="primary"):
            with st.spinner(f"Simulating sending inquiry..."):
                time.sleep(1.5) # Simulate network delay
            
            st.success(f"Inquiry marked as sent to {supplier['name']}.")
            st.session_state['initial_message_sent'] = True
            time.sleep(1) # Short delay for user feedback
            st.session_state['current_step'] = 3
            st.rerun()

    # --- 3. Show Sent Confirmation (if sent) ---
    elif st.session_state['initial_message_sent']:
        st.success(f"Inquiry marked as sent to {supplier.get('name', 'supplier')}. Proceeding to await response.")
        # Auto-advance or provide manual button
        if st.button("Next: Await Response", type="primary"):
             st.session_state['current_step'] = 3
             st.rerun() 