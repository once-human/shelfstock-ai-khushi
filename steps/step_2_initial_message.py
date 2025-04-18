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

    # Get product details from session state
    product_name = st.session_state.get('product_name', '')
    quantity = st.session_state.get('quantity', 1)
    supplier_email = supplier.get('contact_email') # Still useful to display

    # Debug information
    st.write(f"Debug - Product Name: {product_name}")
    st.write(f"Debug - Quantity: {quantity}")

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
        - Name: Yahswi Ladda
        
        **Order Details:**
        - Product Name: {product_name}
        - Quantity Required: {quantity}
        - Product Description: Please provide detailed specifications for {product_name}
        - Quality Requirements: Please specify any quality standards or certifications needed
        - Packaging Requirements: Please specify any special packaging needs
        - Delivery Timeline: Please provide estimated delivery time
        - Payment Terms: Please specify payment terms and conditions

        **Instructions:**
        - Keep the tone professional and courteous.
        - Start the message with "Dear Yashwi Ladda,"
        - In the first paragraph, clearly state: "We are interested in ordering {quantity} units of {product_name}."
        - Request detailed information about the product specifications for {product_name}.
        - Ask for confirmation of availability, estimated lead time, and pricing/quote process.
        - Request information about quality standards and certifications.
        - Inquire about packaging options and requirements.
        - Ask about delivery timelines and logistics.
        - Discuss payment terms and conditions.
        - End the message with the following signature exactly as shown:
        
        Best regards,
        
        Khushi Banthia
        cofounder  
        VIA Rides  
        khushi@viarides.in
        """
        message_history = [
            {"role": "system", "content": "You draft detailed, professional supplier inquiry messages that include comprehensive product specifications and business requirements. Always include the product name and quantity in the first paragraph."},
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
        st.text_area("Message Body", value=message_body, height=300, key="initial_message_display")
        
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