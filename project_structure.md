# Project Structure: Streamlined Supplier Order Management UI

This document outlines the proposed file and directory structure for the Streamlit application.

```plaintext
khushi-ai-project/
├── .gitignore
├── README.md                 # Existing project readme (AI Toolkit)
├── project_info.md           # Overview of the Supplier Order UI project
├── project_structure.md      # This file
├── checklist.md              # Development checklist (to be created)
├── requirements.txt          # Python dependencies (streamlit, etc.)
├── configs.py                # Configuration (API keys, step names, file paths)
├── app.py                    # Main Streamlit application entry point
│
├── steps/                    # Directory containing modules for each step
│   ├── __init__.py
│   ├── step_0_product_details.py
│   ├── step_1_select_supplier.py
│   ├── step_2_initial_message.py
│   ├── step_3_await_response.py
│   ├── step_4_assign_worker.py
│   ├── step_5_send_confirmation.py
│   └── step_6_complete.py
│
├── utils/                    # Utility functions and helpers
│   ├── __init__.py
│   ├── state_management.py   # Functions to manage st.session_state
│   ├── data_handler.py       # Functions to load/save data (suppliers, workers)
│   └── ui_components.py      # Reusable UI elements (optional)
│
├── data/                     # Static data files (can be replaced by DB later)
│   ├── suppliers.json        # Example supplier data
│   └── workers.json          # Example worker data
│
├── assets/                   # Static assets (images, CSS)
│   └── style.css             # Optional custom CSS
│
└── ai_toolkit/             # Optional: Existing AI helpers (if used)
    ├── __init__.py
    ├── openai_api_helper.py
    ├── ai_memory_helper.py
    ├── data_save_helper.py
    └── voice_helper.py
```

## Component Descriptions

*   **`app.py`**:
    *   The main script executed by `streamlit run app.py`.
    *   Initializes `st.session_state` if not already done (using functions from `utils/state_management.py`).
    *   Defines the overall page layout (e.g., using `st.columns` or `st.sidebar`).
    *   Renders the left-side vertical step tracker (likely using `st.sidebar`). The current step will be highlighted.
    *   Determines the current step based on `st.session_state`.
    *   Calls the appropriate function from the `steps/` directory to render the content for the current step in the main page area.
    *   Handles navigation logic (e.g., updating the current step in `st.session_state` when a "Next Step" button is clicked).

*   **`steps/`**:
    *   Each `step_*.py` file contains a primary function (e.g., `render_product_details()`) responsible for displaying the UI elements and handling logic for that specific step.
    *   These functions will read from and write to `st.session_state` to get required data (e.g., product name entered in step 0) and store results (e.g., selected supplier in step 1).
    *   They will display input fields (`st.text_input`, `st.number_input`), selection widgets (`st.selectbox`, `st.radio`), informational text (`st.write`, `st.markdown`), and action buttons (`st.button`).
    *   The "Next Step" button's `on_click` callback will typically update `st.session_state['current_step']`.

*   **`utils/`**:
    *   **`state_management.py`**: Contains functions for initializing `st.session_state` with default values (e.g., `current_step = 0`, `product_name = ''`, `selected_supplier = None`, etc.) and potentially functions to safely get/set state variables.
    *   **`data_handler.py`**: Functions to load data like supplier lists or worker availability from files (`data/`) or potentially external sources/databases in the future.
    *   **`ui_components.py`**: (Optional) If complex UI elements are repeated (like styled cards for suppliers/workers), they can be defined here as reusable functions.

*   **`data/`**:
    *   Holds static data used by the application, initially as JSON files. This makes it easy to modify sample data without changing code.

*   **`assets/`**:
    *   Stores static files like custom CSS (`style.css`) if needed to override default Streamlit styling.

*   **`ai_toolkit/`**:
    *   (Optional) The existing AI helper modules can be placed here or kept at the root level. They might be called from within specific `steps/` modules (e.g., `step_2_initial_message.py` could call `openai_api_helper.py` to generate/send a message).

*   **`configs.py`**:
    *   Central place for configurations like API keys, fixed lists (e.g., step names for the tracker), file paths, or other constants.

*   **`requirements.txt`**:
    *   Lists all necessary Python packages (e.g., `streamlit`, `openai`, `pydantic` if used).

*   **`checklist.md`**:
    *   Tracks the development progress step-by-step.

## State Management (`st.session_state`)

Streamlit's `st.session_state` is crucial for maintaining data across steps and user interactions. Key variables will include:

*   `current_step`: An integer indicating the active step (0-6).
*   Variables for data collected at each step: `product_name`, `quantity`, `selected_supplier_id`, `supplier_response`, `assigned_worker_id`, etc.

Initialization and updates to `st.session_state` will be managed primarily in `app.py` and the functions within `steps/*.py`, potentially using helper functions from `utils/state_management.py`. 