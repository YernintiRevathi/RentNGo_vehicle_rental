import csv

# Define CSV file name
csv_file = "vehicles.csv"

# Define vehicle headers
headers = ["name", "description", "price_per_hour", "price_per_day", "price_per_week", "is_available", "photo"]

# Predefined vehicle listings
vehicles = [
    ["Toyota Camry", "4 seats, 30 MPG, Gasoline", 5.00, 50.00, 300.00, True, "vehicles/toyota_camry.jpg"],
    ["Honda Civic", "5 seats, 35 MPG, Gasoline", 4.50, 45.00, 270.00, True, "vehicles/honda_civic.jpg"],
    ["Ford Truck", "6 seats, 20 MPG, Diesel", 6.00, 60.00, 350.00, False, "vehicles/ford_truck.jpg"],
]

# Generate 22 more vehicle listings dynamically (Total: 25)
for i in range(4, 26):
    vehicle = [
        f"Vehicle {i}",
        f"{(i % 5) + 2} seats, {20 + (i % 15)} MPG, {'Gasoline' if i % 2 == 0 else 'Diesel'}",
        round(4.00 + (i % 3) * 0.5, 2),
        round(40.00 + (i % 5) * 10, 2),
        round(250.00 + (i % 7) * 30, 2),
        i % 3 != 0,
        f"vehicles/vehicle_{i}.jpg"
    ]
    vehicles.append(vehicle)

# Write data to CSV file
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write headers
    writer.writerows(vehicles)  # Write data

print(f"CSV file '{csv_file}' created successfully with {len(vehicles)} vehicles!")
