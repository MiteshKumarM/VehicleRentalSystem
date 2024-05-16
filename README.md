# Vehicle Rental System

A simple vehicle rental system built with Python, Streamlit, and MongoDB. This system allows an admin to add, update, and remove vehicles, and clients to view available vehicles, rent, and return them. The application also supports exporting available vehicles to a JSON file.

## Features

- **Admin Page**:
  - Add new vehicles
  - Update existing vehicles
  - Remove vehicles
- **Client Page**:
  - Rent vehicles
  - Return vehicles
- **Available Vehicles Page**:
  - View list of available vehicles
  - Export available vehicles to a JSON file

## Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/username/VehicleRentalSystem.git
   cd VehicleRentalSystem
   ```

2. **Install the required packages**:
   ```
   pip install streamlit pymongo
   ```

3. **Set up MongoDB**:
   - Install MongoDB and ensure it's running on `localhost:27017`.
   - Create a database named `vehicle_rental`.

## Usage

1. **Run the Streamlit application**:
   ```
   streamlit run vehicle_rental_app.py
   ```

2. **Navigate to the application**:
   - Open a web browser and go to `http://localhost:8501`.

3. **Access the Pages**:
   - **Admin Page**: Requires an admin key to access.
   - **Client Page**: For clients to rent and return vehicles.
   - **Available Vehicles Page**: View and export available vehicles.

## Code Overview

### Admin Page

- Add Vehicle: Allows the admin to add a new vehicle with ID, name, and rental price.
- Update Vehicle: Allows the admin to update the name and rental price of an existing vehicle.
- Remove Vehicle: Allows the admin to remove a vehicle by ID.

### Client Page

- Rent Vehicle: Clients can rent a vehicle by entering their details and the vehicle ID.
- Return Vehicle: Clients can return a rented vehicle by entering the vehicle ID.

### Available Vehicles Page

- View Available Vehicles: Displays a list of all available vehicles with their details.
- Export to JSON: Exports the list of available vehicles to a JSON file.


## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [MongoDB](https://www.mongodb.com/)
