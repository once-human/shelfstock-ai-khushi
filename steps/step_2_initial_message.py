import streamlit as st
from utils.data_handler import load_suppliers
# Import AI and config helpers
from code_library.openai_api_helper import generate_completion
import configs
import time # Keep time for potential delays

def render_initial_message():
    """Render the initial message step where an AI-generated message is sent to the supplier."""
    st.header("Step 2: Generate Initial Message")
    
    # Get supplier details
    suppliers = load_suppliers()
    supplier = next((s for s in suppliers if s['id'] == st.session_state.get('selected_supplier_id')), None)
    
    if not supplier:
        st.error("No supplier selected. Please go back and select a supplier.")
        return

    # Get product details from session state
    product_name = st.session_state.get('product_name')
    quantity = st.session_state.get('quantity')

    # Generate message content if not already generated
    if 'initial_message_content' not in st.session_state:
        st.session_state['initial_message_content'] = None

    if st.session_state['initial_message_content'] is None:
        st.subheader("AI Message Generation")
        st.write(f"Generating a polite order request message for **{supplier['name']}** regarding **{quantity} x {product_name}**...")
        
        # Construct the prompt for the AI
        prompt = f"""
        Generate a polite and professional message to a supplier to inquire about placing an order.

        **Supplier Details:**
        - Name: {supplier['name']}
        - Contact Email (for reference, don't include in message): {supplier.get('contact_email', 'N/A')}

        **Order Details:**
        - Product: {product_name}
        - Quantity: {quantity}

        **Instructions:**
        - Address the supplier politely by name.
        - Clearly state the product and quantity we wish to order.
        - Ask them to confirm if they can fulfill this order and inquire about the next steps (e.g., lead time, pricing).
        - Keep the message concise and professional.
        - Do not include placeholders like '[Your Company Name]'; assume the message is from a known business contact.
        """

        # Prepare message history for the AI
        message_history = [
            {"role": "system", "content": "You are an assistant responsible for drafting professional supplier communications."},
            {"role": "user", "content": prompt}
        ]

        # Generate message using AI
        try:
            with st.spinner("Asking AI to draft the message..."):
                generated_message = generate_completion(message_history)
            st.session_state['initial_message_content'] = generated_message
            st.rerun() # Rerun to display the generated message
        except Exception as e:
            st.error(f"Failed to generate message using AI: {e}")
            # Provide a fallback manual option or error state
            st.session_state['initial_message_content'] = "Error generating message."
    
    else:
        # Display the generated message
        st.subheader("Generated Message Preview")
        st.text_area("Message", value=st.session_state['initial_message_content'], height=250, key="initial_message_display")
        
        # Button to proceed (simulating sending)
        if st.button("Confirm and Proceed (Simulate Send)"):
            # In a real app, you would add email sending logic here
            st.success("Message confirmed. Proceeding to await response.")
            time.sleep(1) # Short delay for user feedback
            st.session_state['current_step'] = 3
            st.rerun() 