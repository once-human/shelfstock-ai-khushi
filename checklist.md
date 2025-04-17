# Development Checklist: Streamlined Supplier Order UI

This checklist tracks the progress of building the Streamlit application based on `project_info.md` and `project_structure.md`.

## Phase 1: Project Setup & Foundation

- [x] Create base directories: `steps/`, `utils/`, `data/`, `assets/` (and `ai_toolkit/` if moving existing files).
- [x] Create empty Python files with `__init__.py` in `steps/`, `utils/`, and `ai_toolkit/`.
- [x] Create placeholder Python files: `app.py`, `configs.py`, `utils/state_management.py`, `utils/data_handler.py`, `utils/ui_components.py` (optional).
- [x] Create placeholder step files: `steps/step_0_product_details.py` to `steps/step_6_complete.py`.
- [x] Create placeholder data files: `data/suppliers.json`, `data/workers.json`.
- [ ] Create placeholder asset files: `assets/style.css` (optional).
- [x] Update `requirements.txt` with necessary packages (at least `streamlit`).
- [x] Configure `configs.py` with initial settings (e.g., step names list).
- [x] Basic `app.py` setup: Import Streamlit, set page config.

## Phase 2: Core Layout & State Management

- [x] Implement state initialization in `utils/state_management.py` (function to set default `st.session_state` values).
- [x] Call state initialization in `app.py`.
- [x] Implement the sidebar step tracker in `app.py` (using `st.sidebar`).
    - [x] Display all step names.
    - [x] Visually indicate the current step (based on `st.session_state['current_step']`).
    - [x] (Optional) Indicate completed steps.
- [x] Implement main content area switching logic in `app.py` (if/elif based on `st.session_state['current_step']` to call render functions from `steps/` modules).

## Phase 3: Data Handling

- [x] Populate `data/suppliers.json` with sample supplier data (name, rating, id, etc.).
- [x] Populate `data/workers.json` with sample worker data (name, availability, id, etc.).
- [x] Implement data loading functions in `utils/data_handler.py` (e.g., `load_suppliers()`, `load_workers()`).

## Phase 4: Step Implementation (UI & Logic)

- [x] **Step 0: Product Details (`steps/step_0_product_details.py`)**
    - [x] Create `render_product_details()` function.
    - [x] Add input fields for Product Name and Quantity (`st.text_input`, `st.number_input`).
    - [x] Store inputs in `st.session_state`.
    - [x] Add "Next Step" button to advance `st.session_state['current_step']`.
- [x] **Step 1: Select Supplier (`steps/step_1_select_supplier.py`)**
    - [x] Create `render_select_supplier()` function.
    - [x] Load supplier data using `utils/data_handler.py`.
    - [x] Display suppliers (e.g., using `st.radio` or custom cards from `utils/ui_components.py`).
    - [x] Store selected supplier ID in `st.session_state`.
    - [x] Add "Next Step" button.
- [x] **Step 2: Initial Message (`steps/step_2_initial_message.py`)**
    - [x] Create `render_initial_message()` function.
    - [x] Display placeholder text indicating message is being sent (or implement actual sending logic later).
    - [x] Add "Next Step" button (or potentially automate transition).
- [x] **Step 3: Await Response (`steps/step_3_await_response.py`)**
    - [x] Create `render_await_response()` function.
    - [x] Display placeholder text indicating waiting status.
    - [x] (Later) Implement logic to check for/simulate supplier response.
    - [x] Store simulated response ('Accepted'/'Rejected') in `st.session_state`.
    - [x] Add logic to proceed only if 'Accepted'.
    - [x] Add "Next Step" button (or potentially automate transition).
- [x] **Step 4: Assign Worker (`steps/step_4_assign_worker.py`)**
    - [x] Create `render_assign_worker()` function.
    - [x] Load worker data using `utils/data_handler.py`.
    - [x] Filter/display available workers.
    - [x] Add selection widget (`st.selectbox` or similar).
    - [x] Store selected worker ID in `st.session_state`.
    - [x] Add "Next Step" button.
- [x] **Step 5: Send Confirmation (`steps/step_5_send_confirmation.py`)**
    - [x] Create `render_send_confirmation()` function.
    - [x] Display placeholder text indicating confirmation is being sent.
    - [x] Add "Next Step" button (or potentially automate transition).
- [x] **Step 6: Complete (`steps/step_6_complete.py`)**
    - [x] Create `render_complete()` function.
    - [x] Display a summary of the order (Product, Quantity, Supplier, Worker).
    - [x] Display a completion message.
    - [x] (Optional) Add a button to start a new order (reset state).

## Phase 5: Styling & Refinements (Optional)

- [x] Add custom CSS rules to `assets/style.css` for improved UI/UX.
- [x] Load custom CSS in `app.py`.
- [ ] Implement reusable UI components in `utils/ui_components.py` (e.g., styled cards for suppliers/workers).
- [ ] Refine layout, button placement, and visual feedback.

## Phase 6: AI Integration (Optional)

- [ ] Integrate `ai_toolkit/` components if needed.
- [x] Implement actual message/email generation in Step 2 (Initial Message) using `openai_api_helper.py`.
- [x] Implement actual confirmation sending in Step 5 (Send Confirmation).
- [x] Add error handling for API calls.

## Phase 7: Testing & Finalization

- [ ] Test the end-to-end workflow thoroughly.
- [x] Debug any issues with state management or step transitions.
- [x] Add input validation where necessary.
- [x] Clean up code and add comments.

## Phase 8: Deployment (Optional)

- [ ] Prepare for deployment (e.g., Streamlit Cloud, Heroku, Docker).
- [ ] Ensure `requirements.txt` is accurate.
- [ ] Configure secrets management for API keys if deploying. 