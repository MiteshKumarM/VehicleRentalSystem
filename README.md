# Vehicle Rental Management System

This Python script implements a simple vehicle rental management system using Streamlit for the user interface and MongoDB for data storage. The system allows users to sign up, log in, rent vehicles, return vehicles, and perform administrative tasks such as adding, updating, and removing vehicles.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 
- Streamlit
- pymongo
- Werkzeug

You can install the required dependencies using pip:

```
pip install streamlit pymongo Werkzeug
```

## Usage

1. Clone the repository or download the script (`vehicle_rental.py`).
2. Install the required dependencies as mentioned above.
3. Make sure MongoDB is running locally on port `27017`.
4. Run the script:

```
streamlit run vehicle_rental.py
```

5. Access the application through your browser at the provided URL.

## Features

### User Authentication

- Users can sign up with a unique username and password.
- Passwords are securely hashed before storing them in the database.
- Existing users can log in using their credentials.

### Client Page

- Logged-in users can rent vehicles by providing necessary details such as name, address, phone number, and license number.
- They can also return rented vehicles.

### Admin Page

- Admins can perform CRUD operations on vehicles.
- They can add new vehicles, update existing ones, and remove vehicles from the system.

### Available Vehicles Page

- Displays a list of vehicles available for rent.

## Security

- User passwords are securely hashed using the PBKDF2 algorithm provided by Werkzeug.
- An admin key is required to access the admin page, providing an additional layer of security.
