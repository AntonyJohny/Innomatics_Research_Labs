# Library Management System - FastAPI Backend

🚀 A fully functional RESTful API built with **FastAPI** as part of the **Feb 2026 Internship at Innomatics Research Labs**. This project demonstrates complete CRUD operations, Pydantic data validation, and advanced API features like search, sorting, and pagination.

## 📌 Project Overview
The **Library Management System** allows users to manage a digital catalog of books. It includes features for adding new books, updating details, searching through the collection, and a multi-step workflow for borrowing and returning items.

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Language:** Python 3.11+
* **Validation:** Pydantic
* **Server:** Uvicorn
* **Documentation:** Swagger UI (OpenAPI)

## ✨ Key Features (20 Tasks Implemented)
1. **Core GET APIs:** Home route, list all books, and summary statistics.
2. **POST + Pydantic:** Secure data entry with field constraints and validation.
3. **Full CRUD:** Create, Read, Update, and Delete operations for book records.
4. **Multi-Step Workflow:** A connected logic flow: `Check Availability` -> `Borrow Book` -> `Verify Status` -> `Return Book`.
5. **Advanced APIs:** Keyword search, result sorting, and paginated responses.
6. **Error Handling:** Custom 404 (Not Found) and 422 (Validation Error) responses.

## 📂 Project Structure
```text
fastapi-library-system/
├── main.py            # Main FastAPI application code
├── requirements.txt   # List of dependencies
├── README.md          # Project documentation
└── screenshots/       # 20 Task execution screenshots from Swagger UI