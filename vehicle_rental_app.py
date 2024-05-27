import streamlit as st
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["vehicle_rental"]
vehicles_collection = db["vehicles"]
rentals_collection = db["rentals"]
users_collection = db["users"]

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Sign Up", "Login", "Admin", "Client", "Available Vehicles", "Checkout"])

# Define the admin key (in a real application, store this securely)
ADMIN_KEY = "admin123"

def create_user(username, password, name, address, phone, license_no):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user = {
        "username": username,
        "password": hashed_password,
        "name": name,
        "address": address,
        "phone": phone,
        "license_no": license_no
    }
    users_collection.insert_one(user)

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        return True
    return False

def signup_page():
    st.title("Client Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    name = st.text_input("Name")
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    license_no = st.text_input("License Number")
    if st.button("Sign Up"):
        if username and password and name and address and phone and license_no:
            if users_collection.find_one({"username": username}):
                st.error("Username already exists")
            else:
                create_user(username, password, name, address, phone, license_no)
                st.success("Signup successful! Please login.")
        else:
            st.warning("Please fill out all fields")

def login_page():
    st.title("Client Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

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
    rental_duration = st.number_input("Enter Rental Duration in Hours", min_value=1, step=1)
    client_name = st.text_input("Client Name", value=st.session_state.get("username", ""))
    client_address = st.text_area("Client Address")
    client_phone = st.text_input("Client Phone Number")
    client_license = st.text_input("Client License Number")
    if st.button("Rent Vehicle"):
        if vehicle_to_rent and rental_duration and client_name and client_address and client_phone and client_license:
            vehicle = vehicles_collection.find_one({"id": vehicle_to_rent, "rented": False})
            if vehicle:
                st.session_state["rental_details"] = {
                    "vehicle_id": vehicle_to_rent,
                    "vehicle_name": vehicle["name"],
                    "rental_price_per_hour": vehicle["rental_price"],
                    "rental_duration": rental_duration,
                    "client_name": client_name,
                    "client_address": client_address,
                    "client_phone": client_phone,
                    "client_license": client_license
                }
                st.experimental_rerun()
            else:
                st.warning("Invalid vehicle ID or vehicle already rented.")
        else:
            st.warning("Please provide all client information.")

    # Return a Vehicle
    st.header("Return a Vehicle")
    vehicle_to_return = st.text_input("Enter Vehicle ID to Return")
    review = st.slider("Rate your experience (1-5 stars)", 1, 5, 5)
    if st.button("Return Vehicle"):
        result = vehicles_collection.update_one({"id": vehicle_to_return, "rented": True}, {"$set": {"rented": False}})
        if result.modified_count > 0:
            rentals_collection.update_one(
                {"vehicle_id": vehicle_to_return, "rental_status": "rented"},
                {"$set": {"rental_status": "returned", "review": review}}
            )
            st.success(f"Vehicle {vehicle_to_return} returned successfully with a review of {review} stars!")
        else:
            st.warning("Invalid vehicle ID or vehicle not rented.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.experimental_rerun()

def checkout_page():
    st.title("Checkout Page")
    
    if "rental_details" in st.session_state:
        rental_details = st.session_state["rental_details"]
        vehicle_name = rental_details["vehicle_name"]
        rental_duration = rental_details["rental_duration"]
        rental_price_per_hour = rental_details["rental_price_per_hour"]
        total_cost = rental_duration * rental_price_per_hour
        
        st.write(f"Vehicle ID: {rental_details['vehicle_id']}")
        st.write(f"Vehicle Name: {vehicle_name}")
        st.write(f"Rental Duration: {rental_duration} hour(s)")
        st.write(f"Rental Price per Hour: ${rental_price_per_hour:.2f}")
        st.write(f"Total Cost: ${total_cost:.2f}")
        
        if st.button("Confirm Rental"):
            rental = {
                "vehicle_id": rental_details["vehicle_id"],
                "client_name": rental_details["client_name"],
                "client_address": rental_details["client_address"],
                "client_phone": rental_details["client_phone"],
                "client_license": rental_details["client_license"],
                "rental_duration": rental_duration,
                "total_cost": total_cost,
                "rental_status": "rented"
            }
            rentals_collection.insert_one(rental)
            vehicles_collection.update_one({"id": rental_details["vehicle_id"]}, {"$set": {"rented": True}})
            st.success("Rental confirmed!")
            del st.session_state["rental_details"]
            st.experimental_rerun()
    else:
        st.warning("No rental details found.")
        st.stop()

def available_vehicles_page():
    st.title("Available Vehicles")
    
    # Display Available Vehicles
    st.header("List of Available Vehicles")
    available_vehicles = vehicles_collection.find({"rented": False})
    vehicle_list = []
    for vehicle in available_vehicles:
        rental_price = vehicle.get("rental_price", "N/A")
        if rental_price != "N/A":
            rental_price = f"${rental_price:.2f}"
        vehicle_list.append({
            "ID": vehicle["id"],
            "Name": vehicle["name"],
            "Rental Price": rental_price
        })
    
    if vehicle_list:
        df = pd.DataFrame(vehicle_list)
        st.table(df)
    else:
        st.write("No available vehicles at the moment.")

# Navigation to Admin, Client, Available Vehicles, or Checkout page
if page == "Admin":
    admin_key = st.sidebar.text_input("Enter Admin Key", type="password")
    if admin_key == ADMIN_KEY:
        admin_page()
    else:
        st.sidebar.error("Invalid Admin Key")
elif page == "Client":
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        client_page()
    else:
        st.warning("Please login to access this page.")
elif page == "Available Vehicles":
    available_vehicles_page()
elif page == "Checkout":
    checkout_page()
elif page == "Sign Up":
    signup_page()
elif page == "Login":
    login_page()
