import streamlit as st
from utils.data_handler import load_suppliers, load_workers
# Import AI and config helpers
from code_library.openai_api_helper import generate_completion
import configs
import time # Keep time for potential delays

def render_send_confirmation():
    """Render the send confirmation step where an AI generates the final confirmation message."""
    st.header("Step 5: Generate Confirmation Message")
    
    # Get all relevant data
    suppliers = load_suppliers()
    workers = load_workers()
    
    supplier = next((s for s in suppliers if s['id'] == st.session_state.get('selected_supplier_id')), None)
    worker = next((w for w in workers if w['id'] == st.session_state.get('selected_worker_id')), None)
    
    if not supplier or not worker:
        st.error("Missing supplier or worker information. Please go back and complete previous steps.")
        return

    product_name = st.session_state.get('product_name')
    quantity = st.session_state.get('quantity')

    # Generate confirmation content if not already generated
    if 'confirmation_message_content' not in st.session_state:
        st.session_state['confirmation_message_content'] = None

    if st.session_state['confirmation_message_content'] is None:
        st.subheader("AI Confirmation Generation")
        st.write(f"Generating a confirmation message for **{supplier['name']}** regarding order for **{quantity} x {product_name}**...")
        
        # Construct the prompt for the AI
        prompt = f"""
        Generate a polite and professional order confirmation message to be sent to a supplier.

        **Order Details:**
        - Product: {product_name}
        - Quantity: {quantity}
        - Supplier Name: {supplier['name']}
        - Assigned Internal Worker: {worker['name']}

        **Instructions:**
        - Address the supplier politely.
        - Confirm the order details (product, quantity).
        - Mention the assigned internal worker who will be handling the order.
        - Express thanks for their business.
        - Keep the message concise and professional.
        - Do not include placeholders like '[Your Company Name]'.
        """

        # Prepare message history for the AI
        message_history = [
            {"role": "system", "content": "You are an assistant responsible for drafting professional supplier order confirmations."},
            {"role": "user", "content": prompt}
        ]

        # Generate message using AI
        try:
            with st.spinner("Asking AI to draft the confirmation..."):
                generated_confirmation = generate_completion(message_history)
            st.session_state['confirmation_message_content'] = generated_confirmation
            st.rerun() # Rerun to display the generated message
        except Exception as e:
            st.error(f"Failed to generate confirmation using AI: {e}")
            st.session_state['confirmation_message_content'] = "Error generating confirmation."

    else:
        # Display the generated confirmation
        st.subheader("Generated Confirmation Preview")
        st.text_area("Confirmation", value=st.session_state['confirmation_message_content'], height=300, key="confirmation_message_display")
        
        # Button to proceed (simulating sending)
        if st.button("Confirm and Complete Order (Simulate Send)"):
            # In a real app, you would add email sending logic here
            st.success("Confirmation confirmed. Order complete!")
            time.sleep(1) # Short delay for user feedback
            st.session_state['current_step'] = 6
            st.rerun() 