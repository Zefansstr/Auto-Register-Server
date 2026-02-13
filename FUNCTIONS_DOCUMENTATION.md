# Functions Documentation

## Overview

This script automates customer registration from Excel files to the dashboard using Selenium WebDriver. It reads customer data from Excel, logs into the dashboard, opens the registration form, fills all fields automatically, and submits the form. The script can process multiple customers in batch and saves results to a separate Excel file.

---

## Functions

### `load_mappings()`
- **Purpose**: Reads the `mappings.json` file to load mappings for Traffic ID, Bank ID, and Country Code.
- **Behavior**: If the file is not found, uses default mappings.
- **Returns**: Dictionary containing traffic, bank, and country_code mappings.

### `login(username, password)`
- **Purpose**: Logs into the dashboard using the provided username and password.
- **Parameters**: 
  - `username`: Dashboard username
  - `password`: Dashboard password
- **Returns**: `True` if login successful, `False` otherwise.

### `navigate_to_member_add()`
- **Purpose**: Navigates to the Member Add page by clicking the Member menu, Member submenu, then the Add Member button.
- **Behavior**: If already on the Member page, directly clicks the Add button.
- **Returns**: `True` if navigation successful, `False` otherwise.

### `click_add_member_button()`
- **Purpose**: Finds and clicks the "Add Member" button and waits for the registration form modal to appear.
- **Behavior**: 
  - Waits for overlay to disappear (if present)
  - Scrolls to button if needed
  - Uses JavaScript click as fallback if normal click fails
- **Returns**: `True` if button clicked and form appeared, `False` otherwise.

### `fill_register_form(customer_data, mappings)`
- **Purpose**: Fills all 7 fields in the registration form with customer data from Excel.
- **Parameters**:
  - `customer_data`: Dictionary containing customer data from Excel row
  - `mappings`: Dictionary containing traffic, bank, and country_code mappings
- **Fields filled**:
  1. **Username** - From "Username" column in Excel
  2. **Name** - From "Name" column in Excel
  3. **Phone with Country Code** - Takes country from Excel, selects country code from dropdown, removes country code prefix from phone number, fills the number
  4. **Traffic Source** - Maps from Excel to ID, selects in dropdown, supports Select2
  5. **Bank** - Maps from Excel to ID, selects in dropdown
  6. **Bank Account Name** - If empty/NaN, leaves field empty (does not fill "nan")
  7. **Bank Account Number** - If empty/NaN, leaves field empty (does not fill "nan")
- **Returns**: `True` if all fields filled successfully, `False` otherwise.

### `submit_form()`
- **Purpose**: Clicks the Submit button and checks the result (Success/Duplicate/Failed) based on alert messages or form status.
- **Returns**: 
  - `'success'` - Registration successful
  - `'duplicate'` - Customer already registered (form still open)
  - `'failed'` - Registration failed with error

### `close_modal()`
- **Purpose**: Closes the registration form modal by clicking the close button (×), or uses JavaScript/ESC key if needed.
- **Behavior**: 
  - Tries normal click first
  - Falls back to JavaScript click
  - If both fail, presses ESC key
- **Returns**: `True` if modal closed, `False` otherwise.

### `register_customer(customer_data, mappings)`
- **Purpose**: Complete flow for registering one customer.
- **Flow**: 
  1. Navigate to Member Add page
  2. Fill registration form
  3. Submit form
  4. Handle result (success/duplicate/failed)
  5. Close modal if needed
- **Parameters**:
  - `customer_data`: Dictionary containing customer data from Excel row
  - `mappings`: Dictionary containing traffic, bank, and country_code mappings
- **Returns**: 
  - `'success'` - Registration successful
  - `'duplicate'` - Customer already registered
  - `'failed'` - Registration failed

### `register_from_excel(excel_file, username, password, batch_size=15)`
- **Purpose**: Main function for batch processing multiple customers from Excel file.
- **Parameters**:
  - `excel_file`: Path to Excel file containing customer data
  - `username`: Dashboard username
  - `password`: Dashboard password
  - `batch_size`: Number of records to process before saving results (default: 15)
- **Flow**:
  1. Read Excel file
  2. Load mappings
  3. Login to dashboard
  4. Loop through each row in Excel:
     - Register customer
     - Save result (Success/Duplicate/Failed)
     - Save results to `customers_results.xlsx` every batch (default: 15 records)
  5. Display summary (Total, Success, Duplicate, Failed)
  6. Save final results to `customers_results.xlsx`
  7. Close browser
- **Output**: Creates `customers_results.xlsx` with columns:
  - `Row`: Row number in Excel
  - `Username`: Customer username
  - `Status`: Success / Duplicate (Already Registered) / Failed / Error

---

## Excel File Format

The Excel file must contain the following columns:
- **Username** - Customer username
- **Name** - Full name
- **Phone** - Phone number (without country code)
- **Country** - Country name (Malaysia, Indonesia, etc.)
- **Traffic** - Traffic source (must match mapping)
- **Bank** - Bank name (must match mapping)
- **Bank Account Name** - Account holder name (optional, can be empty)
- **Account No** - Bank account number (optional, can be empty)

---

## Notes

- The script handles empty/NaN values for Bank Account Name and Bank Account Number - fields are left empty instead of filling "nan"
- Phone numbers automatically remove country code prefix based on the selected country
- Traffic and Bank matching is case-insensitive
- The script supports both Select2 and standard HTML select dropdowns
- Results are saved incrementally every batch to prevent data loss if the script stops unexpectedly
