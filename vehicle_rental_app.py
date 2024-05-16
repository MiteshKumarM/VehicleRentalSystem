import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["vehicle_rental"]
vehicles_collection = db["vehicles"]
rentals_collection = db["rentals"]

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Admin", "Client", "Available Vehicles"])

# Define the admin key (in a real application, store this securely)
ADMIN_KEY = "admin123"

def admin_page():
    st.title("Admin Page")
    
    # Add Vehicle Section
    st.header("Add a New Vehicle")
    vehicle_id = st.text_input("Vehicle ID")
    vehicle_name = st.text_input("Vehicle Name")
    rental_price = st.number_input("Dollar(s) per Hour", min_value=0.0, step=0.1)
    if st.button("Add Vehicle"):
        if vehicle_id and vehicle_name and rental_price:
            vehicle = {
                "id": vehicle_id,
                "name": vehicle_name,
                "rental_price": rental_price,
                "rented": False
            }
            vehicles_collection.insert_one(vehicle)
            st.success(f"Vehicle {vehicle_name} added successfully!")
        else:
            st.warning("Please provide vehicle ID, name, and rental price.")

    # Update Vehicle Section
    st.header("Update a Vehicle")
    update_vehicle_id = st.text_input("Enter Vehicle ID to Update")
    new_vehicle_name = st.text_input("New Vehicle Name")
    new_rental_price = st.number_input("Dollar(s) per Hour", min_value=0.0, step=0.1, key='update_price')
    if st.button("Update Vehicle"):
        if update_vehicle_id:
            update_fields = {}
            if new_vehicle_name:
                update_fields["name"] = new_vehicle_name
            if new_rental_price:
                update_fields["rental_price"] = new_rental_price
            if update_fields:
                vehicles_collection.update_one({"id": update_vehicle_id}, {"$set": update_fields})
                st.success(f"Vehicle {update_vehicle_id} updated successfully!")
            else:
                st.warning("No new values provided for update.")
        else:
            st.warning("Please provide a vehicle ID to update.")

    # Remove Vehicle Section
    st.header("Remove a Vehicle")
    remove_vehicle_id = st.text_input("Enter Vehicle ID to Remove")
    if st.button("Remove Vehicle"):
        if remove_vehicle_id:
            vehicles_collection.delete_one({"id": remove_vehicle_id})
            st.success(f"Vehicle {remove_vehicle_id} removed successfully!")
        else:
            st.warning("Please provide a vehicle ID to remove.")

def client_page():
    st.title("Client Page")

    # Rent a Vehicle
    st.header("Rent a Vehicle")
    vehicle_to_rent = st.text_input("Enter Vehicle ID to Rent")
    client_name = st.text_input("Client Name")
    client_address = st.text_area("Client Address")
    client_phone = st.text_input("Client Phone Number")
    client_license = st.text_input("Client License Number")
    if st.button("Rent Vehicle"):
        if vehicle_to_rent and client_name and client_address and client_phone and client_license:
            result = vehicles_collection.update_one({"id": vehicle_to_rent, "rented": False}, {"$set": {"rented": True}})
            if result.modified_count > 0:
                rental = {
                    "vehicle_id": vehicle_to_rent,
                    "client_name": client_name,
                    "client_address": client_address,
                    "client_phone": client_phone,
                    "client_license": client_license,
                    "rental_status": "rented"
                }
                rentals_collection.insert_one(rental)
                st.success(f"Vehicle {vehicle_to_rent} rented successfully!")
            else:
                st.warning("Invalid vehicle ID or vehicle already rented.")
        else:
            st.warning("Please provide all client information.")

    # Return a Vehicle
    st.header("Return a Vehicle")
    vehicle_to_return = st.text_input("Enter Vehicle ID to Return")
    if st.button("Return Vehicle"):
        result = vehicles_collection.update_one({"id": vehicle_to_return, "rented": True}, {"$set": {"rented": False}})
        if result.modified_count > 0:
            rentals_collection.update_one({"vehicle_id": vehicle_to_return, "rental_status": "rented"}, {"$set": {"rental_status": "returned"}})
            st.success(f"Vehicle {vehicle_to_return} returned successfully!")
        else:
            st.warning("Invalid vehicle ID or vehicle not rented.")

def available_vehicles_page():
    st.title("Available Vehicles")
    
    # Display Available Vehicles
    st.header("List of Available Vehicles")
    available_vehicles = vehicles_collection.find({"rented": False})
    for vehicle in available_vehicles:
        rental_price = vehicle.get("rental_price", "N/A")
        st.write(f"ID: {vehicle['id']}, Name: {vehicle['name']}, Rental Price: ${rental_price} per hour")

# Navigation to Admin, Client, or Available Vehicles page
if page == "Admin":
    admin_key = st.sidebar.text_input("Enter Admin Key", type="password")
    if admin_key == ADMIN_KEY:
        admin_page()
    else:
        st.sidebar.error("Invalid Admin Key")
elif page == "Client":
    client_page()
elif page == "Available Vehicles":
    available_vehicles_page()
