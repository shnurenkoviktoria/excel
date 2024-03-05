# Excel Sheet API

This README describes an API for managing Excel sheets and cells using Django Rest Framework.

## CellViewSet

- This viewset handles operations related to individual cells within an Excel sheet.
- Supported actions: Retrieve, Update, Delete.

### Retrieve

- Retrieves the data of a specific cell identified by `sheet_id` and `cell_id`.
- If the sheet with the specified `sheet_id` doesn't exist, it creates a new sheet.
- If the cell with the specified `cell_id` doesn't exist in the sheet, it creates a new cell.
- Returns the data of the cell in the response.

### Update

- Updates the data of a specific cell identified by `sheet_id` and `cell_id`.
- If the sheet with the specified `sheet_id` doesn't exist, it creates a new sheet.
- If the cell with the specified `cell_id` doesn't exist in the sheet, it creates a new cell.
- Calculates the result of the cell based on the updated value.
- Returns the updated data of the cell in the response.

### Delete

- Deletes a specific cell identified by `sheet_id` and `cell_id`.
- If the sheet with the specified `sheet_id` doesn't exist, it creates a new sheet.
- If the cell with the specified `cell_id` doesn't exist in the sheet, it creates a new cell.
- Returns a success response with status code 204 (No Content).

## SheetList

- This viewset handles operations related to the list of sheets.
- Supported actions: Get, Delete.

### Get

- Retrieves the data of all cells in a specific sheet identified by `sheet_id`.
- Returns a JSON response containing the values and results of all cells in the sheet.

### Delete

- Deletes a specific sheet identified by `sheet_id`.
- Returns a success response with status code 204 (No Content).

## Dependencies

- Django Rest Framework
