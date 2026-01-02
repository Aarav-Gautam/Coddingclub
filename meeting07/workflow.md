# PyPaste Workflow Documentation

This document explains the technical flow of the PyPaste application.

## 1. Project Initialization
- The Flask application is initialized in `main.py`.
- A data directory (`data/pastes`) is created automatically if it doesn't exist. This directory will host the text files representing each paste.

## 2. Creating a Paste
1. **Request**: User navigates to the root URL (`/`).
2. **Response**: Flask renders `index.html` which contains a `<form>` with a `textarea`.
3. **Submission**: When the user clicks "Create Paste", the form sends a `POST` request to `/create` with the content of the `textarea`.
4. **Processing**:
    - The backend retrieves the text from `request.form`.
    - A unique, URL-safe ID is generated using Python's `secrets` module (e.g., `_A1b2C3d`).
    - The content is saved to a file named `data/pastes/<ID>.txt`.
5. **Redirection**: The user is redirected to `/view/<ID>`.

## 3. Viewing a Paste
1. **Request**: User navigates to `/view/<ID>`.
2. **Retrieval**:
    - Flask checks if a file named `<ID>.txt` exists in `data/pastes`.
    - If it exists, the content is read into memory.
    - If it doesn't exist, a `404` error is raised.
3. **Rendering**: Flask renders `view.html`, injecting the paste content and its ID into the Jinja2 template.

## 4. Technical Constraints
- **Persistence**: Data is stored using native Python File I/O (`open()`, `write()`, `read()`). No external database (SQL/NoSQL) is required.
- **Frontend**: The styling is handled purely via CSS. There is no JavaScript involved; all navigation and data handling rely on standard HTML forms and HTTP redirects.
- **Styling**: A modern, responsive CSS layout is used to provide a premium user experience without dependencies.

## 5. Security Note
- Filenames are generated using `secrets.token_urlsafe`, making them difficult to guess.
- `abort(404)` ensures that users cannot probe for files that don't exist in a way that reveals system information.
go to https://aaravg.pythonanywhere.com/ and use the app
