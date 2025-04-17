# Development Checklist: Streamlined Supplier Order UI

This checklist tracks the progress of building the Streamlit application based on `project_info.md` and `project_structure.md`.

## Phase 1: Project Setup & Foundation

- [ ] Create base directories: `steps/`, `utils/`, `data/`, `assets/` (and `ai_toolkit/` if moving existing files).
- [ ] Create empty Python files with `__init__.py` in `steps/`, `utils/`, and `ai_toolkit/`.
- [ ] Create placeholder Python files: `app.py`, `configs.py`, `utils/state_management.py`, `utils/data_handler.py`, `utils/ui_components.py` (optional).
- [ ] Create placeholder step files: `steps/step_0_product_details.py` to `steps/step_6_complete.py`.
- [ ] Create placeholder data files: `data/suppliers.json`, `data/workers.json`.
- [ ] Create placeholder asset files: `assets/style.css` (optional).
- [ ] Update `requirements.txt` with necessary packages (at least `streamlit`).
- [ ] Configure `configs.py` with initial settings (e.g., step names list).
- [ ] Basic `app.py` setup: Import Streamlit, set page config.

## Phase 2: Core Layout & State Management

- [ ] Implement state initialization in `utils/state_management.py` (function to set default `st.session_state` values).
- [ ] Call state initialization in `app.py`.
- [ ] Implement the sidebar step tracker in `app.py` (using `st.sidebar`).
    - [ ] Display all step names.
    - [ ] Visually indicate the current step (based on `st.session_state['current_step']`).
    - [ ] (Optional) Indicate completed steps.
- [ ] Implement main content area switching logic in `app.py` (if/elif based on `st.session_state['current_step']` to call render functions from `steps/` modules).

## Phase 3: Data Handling

- [ ] Populate `data/suppliers.json` with sample supplier data (name, rating, id, etc.).
- [ ] Populate `data/workers.json` with sample worker data (name, availability, id, etc.).
- [ ] Implement data loading functions in `utils/data_handler.py` (e.g., `load_suppliers()`, `load_workers()`).

## Phase 4: Step Implementation (UI & Logic)

- [ ] **Step 0: Product Details (`steps/step_0_product_details.py`)**
    - [ ] Create `render_product_details()` function.
    - [ ] Add input fields for Product Name and Quantity (`st.text_input`, `st.number_input`).
    - [ ] Store inputs in `st.session_state`.
    - [ ] Add "Next Step" button to advance `st.session_state['current_step']`.
- [ ] **Step 1: Select Supplier (`steps/step_1_select_supplier.py`)**
    - [ ] Create `render_select_supplier()` function.
    - [ ] Load supplier data using `utils/data_handler.py`.
    - [ ] Display suppliers (e.g., using `st.radio` or custom cards from `utils/ui_components.py`).
    - [ ] Store selected supplier ID in `st.session_state`.
    - [ ] Add "Next Step" button.
- [ ] **Step 2: Initial Message (`steps/step_2_initial_message.py`)**
    - [ ] Create `render_initial_message()` function.
    - [ ] Display placeholder text indicating message is being sent (or implement actual sending logic later).
    - [ ] Add "Next Step" button (or potentially automate transition).
- [ ] **Step 3: Await Response (`steps/step_3_await_response.py`)**
    - [ ] Create `render_await_response()` function.
    - [ ] Display placeholder text indicating waiting status.
    - [ ] (Later) Implement logic to check for/simulate supplier response.
    - [ ] Store simulated response ('Accepted'/'Rejected') in `st.session_state`.
    - [ ] Add logic to proceed only if 'Accepted'.
    - [ ] Add "Next Step" button (or potentially automate transition).
- [ ] **Step 4: Assign Worker (`steps/step_4_assign_worker.py`)**
    - [ ] Create `render_assign_worker()` function.
    - [ ] Load worker data using `utils/data_handler.py`.
    - [ ] Filter/display available workers.
    - [ ] Add selection widget (`st.selectbox` or similar).
    - [ ] Store selected worker ID in `st.session_state`.
    - [ ] Add "Next Step" button.
- [ ] **Step 5: Send Confirmation (`steps/step_5_send_confirmation.py`)**
    - [ ] Create `render_send_confirmation()` function.
    - [ ] Display placeholder text indicating confirmation is being sent.
    - [ ] Add "Next Step" button (or potentially automate transition).
- [ ] **Step 6: Complete (`steps/step_6_complete.py`)**
    - [ ] Create `render_complete()` function.
    - [ ] Display a summary of the order (Product, Quantity, Supplier, Worker).
    - [ ] Display a completion message.
    - [ ] (Optional) Add a button to start a new order (reset state).

## Phase 5: Styling & Refinements (Optional)

- [ ] Add custom CSS rules to `assets/style.css` for improved UI/UX.
- [ ] Load custom CSS in `app.py`.
- [ ] Implement reusable UI components in `utils/ui_components.py` (e.g., styled cards for suppliers/workers).
- [ ] Refine layout, button placement, and visual feedback.

## Phase 6: AI Integration (Optional)

- [ ] Integrate `ai_toolkit/` components if needed.
- [ ] Implement actual message/email generation in Step 2 (Initial Message) using `openai_api_helper.py`.
- [ ] Implement actual confirmation sending in Step 5 (Send Confirmation).
- [ ] Add error handling for API calls.

## Phase 7: Testing & Finalization

- [ ] Test the end-to-end workflow thoroughly.
- [ ] Debug any issues with state management or step transitions.
- [ ] Add input validation where necessary.
- [ ] Clean up code and add comments.

## Phase 8: Deployment (Optional)

- [ ] Prepare for deployment (e.g., Streamlit Cloud, Heroku, Docker).
- [ ] Ensure `requirements.txt` is accurate.
- [ ] Configure secrets management for API keys if deploying. 