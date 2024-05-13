# Flask Web Application Documentation

## Introduction
This documentation provides an overview of the web.py Flask application. 
This application interacts with a RESTful API to manage room and temperature data.

## Prerequisites
Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- psycopg2
- python-dotenv
- requests
- flask-cors

You can simply run this line to install all necessary libraries at one go.

```bash
pip install -r requirements.txt
```

## Setup
1. Clone the repository containing the application.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Create a `.env` file in the root directory of the project and provide the required environment variables:
   ```
   USER=<database_user>
   PASSWORD=<database_password>
   DATABASE_URL=<database_host>
   PORT=<database_port>
   ```
4. Ensure the RESTful API server is running at `http://127.0.0.1:5001/api/v1`.

## Running the Application
To run the application, execute the following command:
```bash
python app.py
```

You can also go into the directory of app.py in terminal and type:
```bash
flask run
```
The application will run on `http://0.0.0.0:5000/`.

## Endpoints

### GET /
- **Description:** Displays the menu.
- **Response:** Renders the `menu.html` template.

### POST /create_room
- **Description:** Creates a new room.
- **Request Body:**
  ```json
  {
    "name": "RoomName"
  }
  ```
- **Response:**
  - 201: Room created successfully.
    ```json
    {
      "message": "Temperature data added successfully!",
      "room_id": "roomId",
      "name": "RoomName"
    }
    ```
  - 500: Error occurred.
    ```json
    {
      "error": "Error: statusCode - errorMessage"
    }
    ```

### GET /get_rooms
- **Description:** Retrieves all rooms with average temperatures.
- **Response:**
  - 200: Success.
    ```json
    {
      "rooms": [
        {
          "id": "roomId",
          "name": "RoomName",
          "avg_temperature": "averageTemperature"
        },
        ...
      ]
    }
    ```
  - 500: Error occurred.
    ```json
    {
      "error": "Error fetching rooms data: errorMessage"
    }
    ```

### GET /get_room_temperatures
- **Description:** Retrieves temperatures for a specific room within a date range.
- **Query Parameters:**
  - room_id: ID of the room.
  - start_date: Start date (format: YYYY-MM-DD).
  - end_date: End date (format: YYYY-MM-DD).
- **Response:**
  - 200: Success.
    ```json
    {
      "temperatures": [
        {
          "id": "temperatureId",
          "temperature": "temperatureValue",
          "date": "date"
        },
        ...
      ]
    }
    ```
  - 404: No temperatures found.
    ```json
    {
      "message": "No temperatures for that room"
    }
    ```
  - 500: Error occurred.
    ```json
    {
      "error": "Error fetching rooms data: errorMessage"
    }
    ```

### DELETE /delete_room
- **Description:** Deletes a room and its associated temperatures.
- **Request Body:**
  ```json
  {
    "room_id": "roomId"
  }
  ```
- **Response:**
  - 200: Room deleted successfully.
    ```json
    {
      "message": "The selected room deleted successfully",
      "room_id": "roomId"
    }
    ```
  - 500: Error occurred.
    ```json
    {
      "error": "Error: statusCode - errorMessage",
      "detail": "Problem with deleting the temperatures from room"
    }
    ```

### GET /room/<int:room_id>
- **Description:** Displays information about a specific room.
- **Response:** Renders the `room.html` template.

### POST /submit_temperature
- **Description:** Submits a temperature reading for a room.
- **Request Body:**
  ```json
  {
    "temperature": "temperatureValue",
    "room_id": "roomId",
    "date": "date" // Optional
  }
  ```
- **Response:**
  - 201: Temperature data added successfully.
    ```json
    {
      "id": "temperatureId",
      "message": "Temperature data added successfully!"
    }
    ```
  - 500: Error occurred.
    ```json
    {
      "error": "Error: statusCode - errorMessage"
    }
    ```

### PUT /update_temperature
- **Description:** Updates a temperature reading.
- **Request Body:**
  ```json
  {
    "temperature": "temperatureValue",
    "room_id": "roomId",
    "date": "date", // Optional
    "id": "temperatureId"
  }
  ```
- **Response:**
  - 200: Temperature data updated successfully.
    ```json
    {
      "message": "Temperature data updated successfully!"
    }
    ```
  - 500: Error occurred.
    ```json
    {
      "error": "Error: statusCode - errorMessage"
    }
    ```

### DELETE /delete_temperature
- **Description:** Deletes a temperature reading.
- **Request Body:**
  ```json
  {
    "id": "temperatureId"
  }
  ```
- **Response:**
  - 200: Temperature deleted successfully.
    ```json
    {
      "message": "The selected temperature deleted successfully"
    }
    ```
  - 404: Temperature not found.
    ```json
    {
      "message": "The selected temperature not existing in the data file"
    }
    ```
  - 500: Error occurred.
    ```json
    {
      "error": "Error: statusCode - errorMessage",
      "detail": "Problem with deleting the temperatures from room"
    }
    ```

## Error Handling
- All endpoints return JSON responses in case of errors, providing details about the error.
- Error responses include an error message and, if applicable, additional details about the error.

