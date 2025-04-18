# Streamlined Supplier Order UI - Technical README

This document provides a technical overview of the Streamlined Supplier Order UI project, built using Streamlit and Python. It details the project structure, core components, workflow logic, and technical implementation choices.

## Project Goal

The primary goal was to develop a single-screen Streamlit application facilitating a guided, 7-step workflow for initiating and tracking supplier orders. Key features include AI-powered message generation for supplier communication (initial inquiry and confirmation), data persistence using a local database, and a modern, user-friendly interface.

## Core Technologies

*   **Language:** Python 3.1x
*   **UI Framework:** Streamlit (`streamlit`)
*   **AI Integration:** OpenAI API (`openai` library) for text generation (GPT-4o or similar).
*   **Data Storage:** SQLite (`sqlite3` built-in library) for managing supplier and worker data.
*   **Styling:** Custom CSS (`assets/style.css`) combined with Streamlit theme configuration (`.streamlit/config.toml`).
*   **Dependencies:** Managed via `requirements.txt`.

## Project Structure

```plaintext
khushi-ai-project/
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration (forces light mode, sets primary color)
├── assets/
│   └── style.css           # Custom CSS for modern UI styling and component overrides
├── code_library/
│   └── openai_api_helper.py # Utility functions wrapping OpenAI API calls (generation)
├── data/
│   └── app_data.db         # SQLite database storing supplier and worker information
├── steps/
│   ├── __init__.py
│   ├── step_0_product_details.py   # UI and logic for Step 0
│   ├── step_1_select_supplier.py   # UI and logic for Step 1
│   ├── step_2_initial_message.py   # UI, AI generation logic, and simulation for Step 2
│   ├── step_3_await_response.py    # UI and logic for Step 3 (manual confirmation)
│   ├── step_4_assign_worker.py     # UI and logic for Step 4
│   ├── step_5_send_confirmation.py # UI, AI generation logic, and simulation for Step 5
│   └── step_6_complete.py          # UI and logic for Step 6 (summary)
├── utils/
│   ├── __init__.py
│   ├── data_handler.py     # Abstraction layer for all database interactions (CRUD operations)
│   ├── db_init.py          # Standalone script to initialize the SQLite DB schema and migrate initial data
│   ├── email_handler.py    # (Defunct) Contains email sending logic (currently unused due to simulation)
│   └── state_management.py # Functions for managing Streamlit session state (initialization, reset)
├── .gitignore                # Specifies intentionally untracked files (e.g., sensitive configs, DB file)
├── app.py                    # Main application entry point, routing logic, sidebar rendering
├── checklist.md              # Development progress tracker
├── configs.py                # Application configuration (API keys via env vars, model names)
├── creator_readme.md         # This file
├── project_info.md           # Initial project description and goals
├── project_structure.md      # Initial planned project structure
├── README.md                 # Original AI Toolkit README (may contain outdated info)
└── requirements.txt          # Python package dependencies
```

## File Descriptions

*   **`app.py`**: The heart of the application. It performs:
    *   Initial setup (page config).
    *   Checks for database existence and triggers initialization if needed.
    *   Loads custom CSS.
    *   Initializes session state using `utils/state_management.py`.
    *   Renders the persistent sidebar using `st.sidebar`, displaying steps and highlighting the current one.
    *   Implements the core routing logic: based on `st.session_state.current_step`, it calls the appropriate `render_` function from the corresponding `steps/step_*.py` module.
*   **`configs.py`**: Centralizes configuration.
    *   Retrieves the OpenAI API key securely from environment variables (`os.getenv`). **Crucially, the API key should NOT be hardcoded here.**
    *   Defines the language model to use (e.g., `gpt-4o`).
    *   (Previously held email configuration, now commented out as email sending is simulated).
*   **`.streamlit/config.toml`**: Forces Streamlit to use the `light` base theme and sets the primary color, background colors, and default text color, ensuring UI consistency regardless of browser/OS settings.
*   **`assets/style.css`**: Contains extensive custom CSS rules to achieve the modern UI look and feel. It overrides default Streamlit styles for:
    *   Layout, spacing, and padding.
    *   Sidebar appearance and step indicators.
    *   Typography and heading styles.
    *   Button styling (primary blue, default grey) with hover/active states.
    *   Input fields (`st.text_input`, `st.number_input`, `st.selectbox`), labels, borders, and focus states.
    *   Radio button (`st.radio`) appearance.
    *   Spinner and alert component styling.
*   **`steps/step_*.py`**: Each file corresponds to one step in the workflow.
    *   Contains a primary `render_*()` function called by `app.py`.
    *   Uses Streamlit widgets (`st.text_input`, `st.number_input`, `st.radio`, `st.selectbox`, `st.button`, `st.markdown`, etc.) to display the UI for that step.
    *   Interacts with `st.session_state` to read previous inputs and store current step data.
    *   Calls functions from `utils/data_handler.py` to fetch necessary data (suppliers, workers).
    *   Calls functions from `code_library/openai_api_helper.py` (in steps 2 and 5) to generate messages.
    *   Handles button clicks to update `st.session_state.current_step` and trigger `st.rerun()` for smooth transitions.
*   **`utils/state_management.py`**: Manages the application's state across user interactions and reruns.
    *   `init_session_state()`: Initializes `st.session_state` with default values for all tracked variables (current step, form inputs, selected IDs, generated messages, status flags) if they don't exist.
    *   `get_default_state()`: Returns the dictionary of default state values.
    *   `reset_state()`: Resets all relevant keys in `st.session_state` to their defaults, used for starting a new order.
*   **`utils/data_handler.py`**: Acts as the data access layer for the SQLite database.
    *   Provides functions (`load_suppliers`, `load_workers`, `get_available_workers`, `get_supplier_by_id`, `get_worker_by_id`) to abstract away SQL queries.
    *   Handles database connections and cursor management.
    *   Includes basic error handling for database operations.
    *   Transforms data between database storage (e.g., boolean as integer, list as JSON string) and Python types.
*   **`utils/db_init.py`**: A utility script to set up the database.
    *   Creates the `suppliers` and `workers` tables if they don't exist.
    *   Contains logic to migrate data from the initial `suppliers.json` and `workers.json` files into the database *only if the tables are empty*. This script should be run manually once.
*   **`code_library/openai_api_helper.py`**: Wraps the OpenAI API call for text generation.
    *   Initializes the OpenAI client using the API key from `configs.py`.
    *   `generate_completion()`: Takes a message history list and sends it to the specified chat model, returning the AI's response.
*   **`requirements.txt`**: Lists all Python dependencies required to run the project (e.g., `streamlit`, `openai`).

## Application Workflow & Logic

The application guides the user through a 7-step process:

1.  **Step 0: Product Details**: User inputs `Product Name` and `Quantity`. These are stored in `st.session_state`.
2.  **Step 1: Select Supplier**: Fetches suppliers from the database (`data_handler.load_suppliers`). Displays them using `st.radio`. The selected supplier's ID is stored in `st.session_state`.
3.  **Step 2: Send Initial Message**: 
    *   Fetches selected supplier details (`data_handler.get_supplier_by_id`).
    *   Constructs a prompt using product details and supplier info.
    *   Calls `openai_api_helper.generate_completion` to draft an inquiry message.
    *   Displays the AI-generated message.
    *   Simulates sending the message upon button click (using `time.sleep`) and updates state (`initial_message_sent`, `current_step`).
4.  **Step 3: Await Response**: 
    *   Displays the status (waiting for external confirmation).
    *   Provides "Mark as ACCEPTED" and "Mark as REJECTED" buttons.
    *   The user manually clicks a button based on actual external communication (e.g., checking their email).
    *   The chosen response (`Accepted`/`Rejected`) is stored in `st.session_state`.
    *   If rejected, the flow stops, allowing the user to start over. If accepted, proceeds to the next step.
5.  **Step 4: Assign Worker**: 
    *   Fetches *available* workers from the database (`data_handler.get_available_workers`).
    *   Displays them in a `st.selectbox`.
    *   Stores the selected worker's ID in `st.session_state` upon button click.
6.  **Step 5: Send Confirmation**: 
    *   Fetches selected supplier and worker details.
    *   Constructs a prompt for a confirmation message including all order details.
    *   Calls `openai_api_helper.generate_completion` to draft the confirmation.
    *   Displays the AI-generated confirmation.
    *   Simulates sending the confirmation upon button click and updates state (`confirmation_message_sent`, `current_step`).
7.  **Step 6: Order Complete**: 
    *   Fetches final order details (supplier, worker, product, quantity).
    *   Displays a success message and a formatted summary of the completed order.
    *   Provides a "Start New Order" button which calls `utils.state_management.reset_state()` to clear session state and return to Step 0.

## State Management

Streamlit's `st.session_state` is used extensively to maintain the application's state across user interactions and script reruns. Key state variables include:

*   `current_step`: Tracks the active step number (0-6).
*   `product_name`, `quantity`: User inputs from Step 0.
*   `selected_supplier_id`: ID chosen in Step 1.
*   `initial_message_content`, `initial_message_sent`: AI message from Step 2 and its simulated send status.
*   `supplier_response`: Manual status ('Accepted'/'Rejected') from Step 3.
*   `selected_worker_id`: ID chosen in Step 4.
*   `confirmation_message_content`, `confirmation_message_sent`: AI message from Step 5 and its simulated send status.

The `utils/state_management.py` module ensures these are initialized correctly and provides a function to reset them.

## Running the Application

1.  **Clone the repository.**
2.  **Install dependencies:** `pip install -r requirements.txt` (preferably within a virtual environment).
3.  **Set up OpenAI API Key:** Create a `.env` file in the root directory and add `OPENAI_API_KEY=sk-YourActualApiKey` OR set the `OPENAI_API_KEY` environment variable system-wide. **Do not commit your API key.**
4.  **Initialize Database:** Run `python utils/db_init.py` once from the project root directory.
5.  **Run Streamlit:** `python -m streamlit run app.py`
6.  Open the provided local URL (e.g., `http://localhost:8501`) in your browser.

## Technical Considerations & Potential Improvements

*   **Security:** API keys and any potential future credentials (like email passwords) *must* be handled securely using environment variables or secrets management, not hardcoded in version control.
*   **Error Handling:** While basic error handling exists (API calls, DB connections), a production application would require more robust logging and user feedback for failures.
*   **Real Email Integration:** The `utils/email_handler.py` exists but is unused. To enable it, uncomment the relevant lines in steps 2 & 5, uncomment and configure SMTP settings in `configs.py` (using secure methods), and ensure the necessary libraries are installed.
*   **Asynchronous Operations:** Real email sending or long API calls could block the Streamlit app. In a larger application, these would typically be handled by background workers (e.g., Celery) to avoid freezing the UI.
*   **Database Migrations:** For schema changes beyond the initial setup, a proper database migration tool (like Alembic) would be necessary.
*   **Testing:** Formal unit and integration tests would improve reliability.
*   **UI Components:** Reusable UI elements (like styled cards for suppliers/workers) could be extracted into `utils/ui_components.py` for better code organization.

This README provides a comprehensive technical overview suitable for understanding the development choices and structure of the application. 