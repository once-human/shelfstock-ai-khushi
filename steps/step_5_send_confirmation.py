import streamlit as st
from utils.data_handler import get_supplier_by_id, get_worker_by_id
from code_library.openai_api_helper import generate_completion
# from utils.email_handler import send_email # No longer sending real email
import configs
import time

def render_send_confirmation():
    """Render the send confirmation step: AI drafts message, user confirms, simulates sending."""
    st.header("Step 5: Generate Order Confirmation") # Renamed header
    
    supplier_id = st.session_state.get('selected_supplier_id')
    worker_id = st.session_state.get('selected_worker_id')
    
    supplier = get_supplier_by_id(supplier_id)
    worker = get_worker_by_id(worker_id)
    
    if not supplier or not worker:
        st.error("Missing supplier or worker information. Please restart the process or go back.")
        return

    product_name = st.session_state.get('product_name')
    quantity = st.session_state.get('quantity')
    supplier_email = supplier.get('contact_email') # Still useful to display

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
        Generate a polite and professional order confirmation message to be sent to a supplier.
        
        **Order Details:**
        - Product Name: {product_name}
        - Quantity: {quantity}
        - Supplier Name: Yashwi Ladda
        - Assigned Internal Contact: {worker['name']} ({worker.get('role', '')})
        
        **Instructions:**
        - Start with "Dear Yashwi Ladda,"
        - Keep the tone professional and appreciative.
        - In the first paragraph, clearly state: "This email confirms our order for {quantity} units of {product_name}."
        - Mention that {worker['name']} ({worker.get('role', '')}) will be the dedicated point of contact for this order.
        - Provide the contact details of the assigned worker.
        - Express appreciation for their business.
        - End the message with the following signature exactly as shown:

        Best regards,

        Khushi Banthia
        cofounder  
        VIA Rides  
        khushi@viarides.in
        """
        message_history = [
            {"role": "system", "content": "You draft professional order confirmation messages that are clear, concise, and include all necessary details."},
            {"role": "user", "content": prompt}
        ]

        try:
            with st.spinner("Asking AI to draft the confirmation..."):
                generated_confirmation = generate_completion(message_history)
            st.session_state['confirmation_message_content'] = generated_confirmation.strip()
            st.rerun()
        except Exception as e:
            st.error(f"Failed to generate confirmation using AI: {e}")
            st.session_state['confirmation_message_content'] = f"Error generating confirmation: {e}"

    # --- 2. Display Confirmation and Simulate Send Button (if generated, not sent) ---
    elif st.session_state['confirmation_message_content'] is not None and not st.session_state['confirmation_message_sent']:
        st.subheader("Confirmation Preview (Drafted by AI)")
        confirmation_body = st.session_state['confirmation_message_content']
        st.text_area("Confirmation Body", value=confirmation_body, height=300, key="confirmation_message_display")
        
        if supplier_email:
             st.write(f"(Simulating send to: {supplier_email})")
        else:
             st.warning(f"No contact email found for {supplier['name']}, but proceeding with simulation.", icon="⚠️")
            
        # Button to simulate sending the email
        if st.button("Confirm and Complete Order (Simulate Send)", type="primary"):
            with st.spinner(f"Simulating sending confirmation..."):
                time.sleep(1.5) # Simulate network delay
            
            st.success(f"Confirmation marked as sent to {supplier['name']}. Order complete!")
            st.session_state['confirmation_message_sent'] = True
            time.sleep(1)
            st.session_state['current_step'] = 6
            st.rerun()
                
    # --- 3. Show Sent Confirmation (if sent) ---
    elif st.session_state['confirmation_message_sent']:
        st.success(f"Confirmation marked as sent to {supplier.get('name', 'supplier')}. Order complete!")
        if st.button("View Summary", type="primary"):
             st.session_state['current_step'] = 6
             st.rerun() 