# RentNGo | Vehicle Rental Web Application

**A simple, functional vehicle rental management system built using Python and Flask.**

---

## 🚗 Project Overview

**RentNGo** simulates a real-world vehicle rental service through a clean web interface. It allows users to view and rent vehicles, and provides admin-like functionality for managing inventory and exporting data.

---

## 👤 User Perspectives

### For Customers:

* Browse available **cars and bikes** with images and details.
* Select and rent vehicles directly from the homepage.
* Simple and intuitive navigation, styled with HTML & CSS.

### For Admins:

* Add new vehicles to the system (via script or CSV).
* View vehicle availability.
* Export vehicle records as CSV using the `generate_csv.py` script.

---

## 🛠️ Tech Stack & Skills Used

### 🔙 Backend:

* **Python**: Core logic and scripting
* **Flask**: Web framework for routing and rendering templates
* **CSV File Handling**: For storing and managing vehicle inventory

### 🌐 Frontend:

* **HTML (Jinja2 templates)**: Dynamic content rendering
* **CSS**: Basic styling for layout and appearance
* **Static Images**: Displayed using Flask's `static/` folder

### 🗂️ Project Structure:

* `app.py`: Main application file with Flask routes
* `templates/`: HTML files for rendering pages
* `static/`: Contains vehicle images
* `generate_csv.py`: Script to auto-create vehicle listings

---

## 📦 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/YernintiRevathi/RentNGo_vehicle_rental.git
   cd RentNGo_vehicle_rental
   ```
2. Install Flask:

   ```bash
   pip install Flask
   ```
3. Run the app:

   ```bash
   python app.py
   ```
4. Open your browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

---

## ✨ Future Improvements

* Add login/signup functionality
* Enable booking confirmation and return logic
* Use a proper database like SQLite or PostgreSQL
* Add filtering/search options

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

Built with ❤️ by \*\*[**Revathi Yerninti**](https://github.com/YernintiRevathi)
