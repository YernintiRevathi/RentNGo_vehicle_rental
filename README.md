**RentNGo | Vehicle Rental Web Application**

A simple, functional vehicle rental management system built using Python and Flask.

---

### 🚗 Project Overview

RentNGo simulates a real-world vehicle rental service through a clean web interface. It allows users to view and rent vehicles, and provides admin-like functionality for managing inventory and exporting data.

---

### 👤 User Perspectives

*   **For Customers:**
    *   Register and Login.
    *   Browse available cars and bikes with images and details.
    *   Select and rent vehicles.
    *   Payment.
    *   View booking details and transaction history.
    *   Simple and intuitive navigation, styled with HTML & CSS.
    *   Secure user registration and login.
    *   User profile management.

*   **For Admins:**
    *   Secure admin login to access management dashboard.
    *   Add new vehicles to the system.
    *   View, update, and delete vehicles, including toggling availability.
    *   Manage user accounts (view, delete).
    *   View all active bookings.
    *   View all payment transactions.

---

### 🛠️ Tech Stack & Skills Used

This project leverages a modern and efficient set of technologies to deliver a full-stack web application.

#### 🔙 Backend:

*   **Python:** The core programming language for all application logic, scripting, and server-side operations.
*   **Flask:** A lightweight and flexible micro-web framework used for:
    *   Defining application routes (`@app.route`).
    *   Handling HTTP requests (GET, POST).
    *   Managing application context and request/response cycles.
    *   Building RESTful API endpoints (e.g., `/api/vehicle/<int:vehicle_id>`).
*   **Flask-SQLAlchemy:** An extension for Flask that provides SQLAlchemy integration, an Object-Relational Mapper (ORM) for:
    *   Defining database models (`User`, `Transaction`, `Booking`).
    *   Interacting with the database using Python objects instead of raw SQL.
    *   Managing database sessions and commits.
*   **SQLite:** A lightweight, file-based relational database used for:
    *   Storing application data (users, transactions, bookings).
    *   Easy setup and portability for development environments.
*   **Bcrypt:** A password hashing library used for:
    *   Securely hashing user passwords before storing them in the database.
    *   Verifying user passwords during login to protect against data breaches.
*   **CSV File Handling:** Utilized for:
    *   Storing and managing the vehicle inventory data (`vehicles.csv`).
    *   Providing a simple, human-readable way to update vehicle information.
    *   Demonstrating data persistence outside of a traditional database for specific datasets.

#### 🌐 Frontend:

*   **HTML (Jinja2 templates):** Used for structuring web pages and rendering dynamic content. Jinja2, Flask's default templating engine, enables:
    *   Embedding Python logic (e.g., `{% if ... %}`, `{% for ... %}`) directly into HTML.
    *   Displaying data passed from Flask routes (e.g., `{{ user.name }}`).
*   **CSS:** For styling the web application, ensuring a clean, responsive, and intuitive user interface.
*   **JavaScript/jQuery (Implicit):** While not explicitly listed as a core dependency in `pip install`, the `jsonify` and `request.json` usage in `/book_vehicle` and `/admin/update_availability` implies client-side JavaScript (likely with Fetch API or jQuery's AJAX) for asynchronous communication with the backend.
*   **Static Images:** Displayed using Flask's `static/` folder for vehicle photos and other visual assets.

---

### 🗂️ Project Structure:

*   **`app.py`:** The main application file containing all Flask routes, database model definitions, and core business logic.
*   **`templates/`:** Directory housing all HTML files rendered by Flask, utilizing Jinja2 templating.
*   **`static/`:** Contains static assets such as CSS files, JavaScript files, and vehicle images.
*   **`instance/`:** (Auto-generated) Contains the SQLite database file (`payment.db`).
*   **`vehicles.csv`:** Stores the list of vehicles available for rent.
*   **`generate_csv.py`:** Implies a script to auto-create vehicle listings if `vehicles.csv` is not present, though this functionality is integrated directly into `read_vehicles()` in `app.py`.

---

### 📦 How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YernintiRevathi/RentNGo_vehicle_rental.git
    cd RentNGo_vehicle_rental
    ```
2.  **Install dependencies (ideally in a virtual environment):**
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    pip install Flask Flask-SQLAlchemy bcrypt
    ```
3.  **Run the application:**
    ```bash
    python app.py
    ```
4.  **Open your browser and navigate to:**
    ```
    http://127.0.0.1:5000/
    ```
    (Admin credentials: `username: admin`, `password: admin123`)

---

### ✨ Future Improvements

*   Implement more robust input validation for all forms.
*   Logging in using Google account and other options.
*   Add advanced filtering and search options for vehicles.
*   Improve UI/UX with modern frontend frameworks or more extensive CSS.
*   Implement booking confirmation emails or notifications.
*   Integrate a more advanced payment gateway.
*   Transition vehicle data from CSV to the main SQLAlchemy database for unified data management.

---

### 📄 License

This project is open-source and available under the MIT License.

Built with ❤️ by **Revathi Yerninti**
