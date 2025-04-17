# Project Information: Streamlined Supplier Order Management UI

## Goal

To create a single-screen Streamlit application that provides a guided, 7-step workflow for managing supplier orders efficiently.

## Core Features

1.  **Single-Screen Interface:** All steps are managed within one view to minimize navigation complexity.
2.  **Vertical Step Tracker:** A persistent sidebar visualizes the user's progress through the 7 steps.
3.  **Dynamic Content Area:** The main section of the screen updates to show the relevant inputs, information, or actions for the current step.
4.  **Automated Workflow:** Certain steps involve automated actions like sending messages or emails (implementation details TBD, potentially leveraging the existing AI toolkit).
5.  **User Interaction:** Users input data (product details, quantity), make selections (supplier, worker), and trigger actions (next step).

## 7-Step Order Process

1.  **Product Details:** User inputs product name and quantity.
2.  **Select Supplier:** User selects a supplier from a presented list (including details like ratings).
3.  **Initial Message:** System sends an automated message/request to the selected supplier.
4.  **Await Response:** System waits for and displays the supplier's response (acceptance/rejection).
5.  **Assign Worker:** If accepted, user assigns an available salesperson/worker from a list.
6.  **Send Confirmation:** System sends an automated confirmation email to the supplier.
7.  **Complete:** Final confirmation step, potentially displaying a summary or status update.

## Technology Stack

*   **Language:** Python
*   **UI Framework:** Streamlit
*   **Potential AI Integration:** Leveraging components from the existing AI Prototyping Toolkit (`openai_api_helper`, etc.) for automated communication, if desired.

## UI Reference

*   Initial UI concepts are provided in the attached screenshots.
*   The final UI aims to be significantly improved for better aesthetics and user experience. 