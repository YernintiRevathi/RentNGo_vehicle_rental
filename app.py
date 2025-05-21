from datetime import timedelta
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for,flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import os
import csv
import re
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key in production

# SQLite Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set session to be permanent
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

@app.before_request
def make_session_permanent():
    session.permanent = True  # Ensure the session is permanent

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)  # In production, hash this!

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User
    car_name = db.Column(db.String(100), nullable=False)
    pickup_location = db.Column(db.String(100), nullable=False)
    dropoff_location = db.Column(db.String(100), nullable=False)
    pickup_date = db.Column(db.String(50), nullable=False)
    dropoff_date = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))  # Relationship for easy access

# Create tables
with app.app_context():
    db.create_all()

# CSV file for vehicle data
CSV_FILE = "vehicles.csv"

def read_vehicles():
    """Reads vehicle data from CSV with error handling."""
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found! Creating a default file with sample data.")
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["id", "name", "description", "price", "is_available", "photo", "seaters"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            sample_data = [
                {"id": 1, "name": "Toyota Camry", "description": "4 seats, 30 MPG, Gasoline", "price": 120, "is_available": "true", "photo": "toyota_camry.jpg", "seaters": 4},
                {"id": 2, "name": "Ford Explorer", "description": "6 seats, SUV", "price": 150, "is_available": "true", "photo": "explorer.jpg", "seaters": 6},
            ]
            writer.writerows(sample_data)
        return sample_data

    try:
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                print("Error: CSV file is completely empty.")
                return []
            file.seek(0)
            reader = csv.DictReader(file)
            vehicles = list(reader)
            if not vehicles:
                print("Warning: CSV file has no data rows.")
                return []

            processed_vehicles = []
            for vehicle in vehicles:
                seaters_match = re.search(r"(\d+)\s*seats?", vehicle["description"], re.IGNORECASE)
                seaters = int(seaters_match.group(1)) if seaters_match else int(vehicle.get("seaters", 0))
                processed_vehicle = {
                    "id": int(vehicle.get("id", 0)),
                    "name": vehicle.get("name", "Unknown Vehicle"),
                    "description": vehicle.get("description", ""),
                    "price": float(vehicle.get("price", 0)),
                    "is_available": vehicle["is_available"].strip().lower() == "true",
                    "photo": vehicle.get("photo", "default.jpg"),
                    "seaters": seaters
                }
                processed_vehicles.append(processed_vehicle)
            return processed_vehicles
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def write_vehicles(vehicles):
    """Writes vehicle data to CSV with proper formatting."""
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["id", "name", "description", "price", "is_available", "photo", "seaters"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for vehicle in vehicles:
                writer.writerow({
                    "id": vehicle["id"],
                    "name": vehicle["name"],
                    "description": vehicle["description"],
                    "price": vehicle["price"],
                    "is_available": str(vehicle["is_available"]).lower(),
                    "photo": vehicle["photo"],
                    "seaters": vehicle["seaters"]
                })
        print(f"Successfully updated {CSV_FILE} with {len(vehicles)} vehicles.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def update_vehicle_availability(vehicle_id):
    """Updates the availability of a vehicle in the CSV."""
    vehicles = read_vehicles()
    updated = False
    for vehicle in vehicles:
        if vehicle["id"] == vehicle_id:
            vehicle["is_available"] = not vehicle["is_available"]
            updated = True
            break
    if updated:
        write_vehicles(vehicles)
    return updated

# Routes
@app.route('/')
def home():
    return render_template("home.html")

# ---- Check if User is Logged In ----
@app.route('/is_logged_in')
def is_logged_in():
    if 'user_logged_in' in session:
        return "User is logged in"
    else:
        return "User is not logged in"

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.Try to register with a different one or Login")
            return render_template("registration.html")

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User(name=name, email=email, password=hashed_password)  # Hash in production!
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!! , Login")
        return redirect(url_for('login'))
    return render_template("registration.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template("login.html", error="Email and password are required.")
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode(), user.password):
            session['user_logged_in'] =user.id
            session['user_id'] = True
            session['user_name'] = user.name
            # flash("Logged in successfully !!")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials")
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_logged_in'])
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        password = request.form['password']
        
        if password:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        # new_user = User(name=username, email=email, password=hashed_password)        
        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for('profile'))
    
    return render_template('user.html', user=user)

@app.route('/profile')
def profile():
    if 'user_logged_in' not in session:  # Check if the user is logged in
        return redirect(url_for('login'))  

    user = User.query.get(session['user_logged_in'])  # Fetch user using SQLAlchemy

    if user:
        return render_template('user.html', user=user), 200
    else:
        session.pop('user_logged_in', None)  # Remove invalid session
        return redirect(url_for('login'))  # Redirect to login if user not found

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "admin123":
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template("admin_dashboard.html")

@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    """Admin user management route."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([name, email, password]):
            return render_template('admin_users.html', users=User.query.all(), error="All fields are required.")

        if User.query.filter_by(email=email).first():
            return render_template('admin_users.html', users=User.query.all(), error="Email already exists.")

        new_user = User(name=name, email=email, password=password)  # Hash in production
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('admin_users'))

    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    user = User.query.get_or_404(user_id)
    # session.pop('user_logged_in', None)
    session.pop(user.id, None)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_users'))



# Add allowed file extensions for photo uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin/vehicles', methods=['GET', 'POST'])
def admin_vehicles():
    """Admin vehicle management route."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    vehicles = read_vehicles()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price', 0)
        photo = request.form.get('photo', 'default.jpg')
        seaters = request.form.get('seaters', 0)

        if not name or not description:
            return render_template('admin_vehicles.html', vehicles=vehicles, error="Name and description are required.")

        try:
            price = float(price)
            seaters = int(seaters)
            if price <= 0 or seaters < 0:
                raise ValueError("Price must be positive and seaters must be non-negative.")
        except ValueError as e:
            return render_template('admin_vehicles.html', vehicles=vehicles, error=str(e) if str(e) else "Price and seaters must be valid numbers.")

        new_id = max([v["id"] for v in vehicles], default=0) + 1
        new_vehicle = {
            "id": new_id,
            "name": name,
            "description": f"{seaters} seats, {description}",
            "price": price,
            "is_available": True,
            "photo": photo,
            "seaters": seaters
        }
        vehicles.append(new_vehicle)
        write_vehicles(vehicles)
        return redirect(url_for('admin_vehicles'))

    return render_template('admin_vehicles.html', vehicles=vehicles)


@app.route('/admin/delete_vehicle/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    """Delete a vehicle from the admin panel."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    vehicles = read_vehicles()
    original_length = len(vehicles)
    vehicles = [v for v in vehicles if v["id"] != vehicle_id]

    if len(vehicles) < original_length:
        write_vehicles(vehicles)
        return redirect(url_for('admin_vehicles'))
    else:
        return render_template('admin_vehicles.html', vehicles=vehicles, error=f"Vehicle with ID {vehicle_id} not found.")

@app.route('/admin/update_availability/<int:vehicle_id>', methods=['POST'])
def update_availability(vehicle_id):
    """Toggle vehicle availability from the admin panel."""
    if not session.get('admin_logged_in'):
        return jsonify({"error": "Admin login required."}), 401
    success = update_vehicle_availability(vehicle_id)
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v["id"] == vehicle_id), None)
    return jsonify({"success": success, "vehicle_id": vehicle_id, "is_available": vehicle["is_available"] if vehicle else False})

@app.route('/admin/bookings', methods=['GET'])
def admin_bookings():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    bookings = Booking.query.all()
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/admin/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    booking = Booking.query.get_or_404(booking_id)
    vehicles = read_vehicles()
    for vehicle in vehicles:
        if vehicle["name"] == booking.car_name:
            vehicle["is_available"] = True
            write_vehicles(vehicles)
            break
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('admin_bookings'))

@app.route('/admin/transactions')
def admin_transactions():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Fetch transactions from the database
    transactions = Transaction.query.all()

    # Debugging: Print the template name
    print("Rendering template: admin_transactions.html")

    # Render the correct template
    return render_template("admin_transactions.html", transactions=transactions)

@app.route('/admin/logout',methods=['POST','GET'])
def admin_logout():
        if 'admin_logged_in' in session:
            session.pop('admin_logged_in', None)
        if 'user_logged_in' in session:
            session.pop('user_logged_in',None)
        return redirect(url_for('home'))

@app.route('/explore')
def explore():
    if 'user_logged_in' not in session:
        return redirect(url_for('login'))
    
    vehicles = read_vehicles()
    return render_template('explore.html', vehicles=vehicles)

@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)
    session['user_id']=False
    session.pop('user_name', None)
    return redirect(url_for('home'))


@app.route('/api/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    if not session.get('user_logged_in'):
        return jsonify({"error": "Please log in first."}), 401
    
    vehicles = read_vehicles()
    vehicle = next((v for v in vehicles if v["id"] == vehicle_id), None)
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    return jsonify({
        "id": vehicle["id"],
        "name": vehicle["name"],
        "description": vehicle["description"],
        "seaters": vehicle["seaters"],
        "price_hour": vehicle["price"] / 24,
        "price_day": float(vehicle["price"]),
        "is_available": vehicle["is_available"],
        "photo": vehicle["photo"]
    })

@app.route('/book_vehicle', methods=['GET', 'POST'])
def book_vehicle():
    """User vehicle booking route."""
    if not session.get('user_logged_in'):
        if request.method == 'POST':
            return jsonify({"error": "Please log in first."}), 401
        return redirect(url_for('login'))

    if request.method == 'GET':
        vehicle_id = request.args.get('vehicle_id')
        if not vehicle_id:
            return redirect(url_for('explore'))
        vehicles = read_vehicles()
        vehicle = next((v for v in vehicles if v["id"] == int(vehicle_id)), None)
        if not vehicle or not vehicle["is_available"]:
            return redirect(url_for('explore'))
        return render_template('book_vehicle.html', vehicle_id=vehicle_id)

    if request.method == 'POST':
        data = request.json

        try:
            vehicle_id = int(data["vehicle_id"])
            vehicles = read_vehicles()
            vehicle = next((v for v in vehicles if v["id"] == vehicle_id), None)
            if not vehicle:
                return jsonify({"error": "Vehicle not found"}), 404
            if not vehicle["is_available"]:
                return jsonify({"error": f"Sorry, {vehicle['name']} is not available for booking."}), 400

            pickup_date_str = data["pickup_date"]
            dropoff_date_str = data["dropoff_date"]
            pickup_date = datetime.strptime(pickup_date_str, "%Y-%m-%d %H:%M")
            dropoff_date = datetime.strptime(dropoff_date_str, "%Y-%m-%d %H:%M")

            if dropoff_date <= pickup_date:
                return jsonify({"error": "Drop-off date must be after pickup date."}), 400

            new_booking = Booking(
                user_id=session['user_id'],  # Link booking to logged-in user
                car_name=data["car_name"],
                pickup_location=data["pickup_location"],
                dropoff_location=data["dropoff_location"],
                pickup_date=pickup_date_str,
                dropoff_date=dropoff_date_str,
                duration=data["duration"],
                price_per_unit=float(data["price_per_unit"]),
                total_price=float(data["total_price"]),
                payment_method=data["payment_method"]
            )
            db.session.add(new_booking)
            db.session.commit()

            update_vehicle_availability(vehicle_id)

            session['booking_details'] = {
                "car_name": data["car_name"],
                "pickup_location": data["pickup_location"],
                "dropoff_location": data["dropoff_location"],
                "pickup_date": pickup_date_str,
                "dropoff_date": dropoff_date_str,
                "duration": data["duration"],
                "total_price": float(data["total_price"])
            }

            return jsonify({
                "message": f"Successfully booked {vehicle['name']}!",
                "booking_id": new_booking.id,
                "redirect": url_for('payment')
            }), 200

        except KeyError as e:
            return jsonify({"error": f"Missing field: {str(e)}"}), 400
        except ValueError as e:
            return jsonify({"error": f"Invalid data: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": f"Booking failed: {str(e)}"}), 500

@app.route('/vehicles', methods=["GET"])
def get_vehicles():
    return jsonify(read_vehicles())

@app.route('/payment')
def payment():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    booking_details = session.get('booking_details', {})
    return render_template('payment.html', booking_details=booking_details)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    payment_method = request.form.get('payment_method')
    amount = request.form.get('amount')
    if not payment_method or not amount:
        return "Invalid payment data", 400
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return "Invalid amount", 400
    new_transaction = Transaction(
        user_id=session['user_logged_in'],
        payment_method=payment_method,
        amount=amount
    )
    db.session.add(new_transaction)
    db.session.commit()
    session['payment_details'] = {
        "id": new_transaction.id,
        "method": payment_method,
        "amount": amount,
        "date": new_transaction.date.strftime("%Y-%m-%d %H:%M:%S")
    }
    return redirect(url_for('success'))

@app.route('/success')
def success():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    payment_details = session.get('payment_details', {})
    return render_template("success.html", payment_details=payment_details)

@app.route('/transactions')
def transaction_history():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    transactions = Transaction.query.filter_by(user_id=session['user_logged_in']).all()
    return render_template("transactions.html", transactions=transactions)

@app.route('/dashboard')
def dashboard():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    vehicles = read_vehicles()
    return render_template('dashboard.html', vehicles=vehicles)

@app.route('/admin/profile')
def admin_profile():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_profile.html')

if __name__ == "__main__":
    app.run(debug=True)