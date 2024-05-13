# API Documentation

This RESTful API provides endpoints to manage temperature data for different rooms.

---

## Endpoints:

1. **Create Room**
   - **Method:** POST
   - **URL:** `/api/v1/room`
   - **Description:** Creates a new room with the provided name.
   - **Request Body:** JSON object with the following field:
     - `name` (string): The name of the room.
   - **Response:** JSON object containing the ID of the newly created room.

2. **Get All Rooms**
   - **Method:** GET
   - **URL:** `/api/v1/room`
   - **Description:** Retrieves a list of all rooms.
   - **Response:** JSON object containing an array of room objects, each containing:
     - `id` (int): The ID of the room.
     - `name` (string): The name of the room.

3. **Get Room by ID**
   - **Method:** GET
   - **URL:** `/api/v1/room/<int:room_id>`
   - **Description:** Retrieves the name of a room by its ID.
   - **Response:** JSON object containing:
     - `id` (int): The ID of the room.
     - `name` (string): The name of the room.

4. **Update Room**
   - **Method:** PUT
   - **URL:** `/api/v1/room/<int:room_id>`
   - **Description:** Updates the name of a room.
   - **Request Body:** JSON object with the following field:
     - `name` (string): The new name of the room.
   - **Response:** JSON object confirming the update.

5. **Delete Room**
   - **Method:** DELETE
   - **URL:** `/api/v1/room/<int:room_id>`
   - **Description:** Deletes a room by its ID.
   - **Response:** JSON object confirming the deletion.

6. **Create Temperature Record**
   - **Method:** POST
   - **URL:** `/api/v1/temperature`
   - **Description:** Records a new temperature measurement for a specific room.
   - **Request Body:** JSON object with the following fields:
     - `temperature` (float): The temperature value.
     - `room_id` (int): The ID of the room where the temperature was recorded.
     - `date` (string, optional): The date and time of the measurement in the format `%d-%m-%Y %H:%M`.
   - **Response:** JSON object containing the ID of the newly created temperature record.

7. **Get All Temperatures**
   - **Method:** GET
   - **URL:** `/api/v1/temperature`
   - **Description:** Retrieves all temperature records.
   - **Response:** JSON object containing an array of temperature records, each containing:
     - `id` (int): The ID of the temperature record.
     - `room_id` (int): The ID of the room.
     - `temperature` (float): The temperature value.
     - `date` (string): The date and time of the measurement.

8. **Get Temperatures for a Room**
   - **Method:** GET
   - **URL:** `/api/v1/temperature/<int:room_id>`
   - **Description:** Retrieves temperature records for a specific room within a specified date range.
   - **Query Parameters:**
     - `start_date` (string, optional): The start date of the range in the format `%Y-%m-%dT%H:%M`.
     - `end_date` (string, optional): The end date of the range in the format `%Y-%m-%dT%H:%M`.
   - **Response:** JSON object containing an array of temperature records, each containing:
     - `id` (int): The ID of the temperature record.
     - `room_id` (int): The ID of the room.
     - `temperature` (float): The temperature value.
     - `date` (string): The date and time of the measurement.

9. **Update Temperature Record**
   - **Method:** PUT
   - **URL:** `/api/v1/temperature/<int:temp_id>`
   - **Description:** Updates a temperature record.
   - **Request Body:** JSON object with the following fields:
     - `temperature` (float): The new temperature value.
     - `room_id` (int): The new room ID.
     - `date` (string, optional): The new date and time of the measurement in the format `%d-%m-%Y %H:%M`.
   - **Response:** JSON object confirming the update.

10. **Delete Temperature Record**
    - **Method:** DELETE
    - **URL:** `/api/v1/temperature/<int:temp_id>`
    - **Description:** Deletes a temperature record by its ID.
    - **Response:** JSON object confirming the deletion.

11. **Delete Temperatures from a Room**
    - **Method:** DELETE
    - **URL:** `/api/v1/temperature_room/<int:room_id>`
    - **Description:** Deletes all temperature records associated with a specific room.
    - **Response:** JSON object confirming the deletion.

12. **Get Global Average Temperature for a Room**
    - **Method:** GET
    - **URL:** `/api/v1/average/<int:room_id>`
    - **Description:** Calculates the global average temperature for a room.
    - **Response:** JSON object containing:
      - `average` (float): The global average temperature.
      - `days` (int): The number of days with recorded temperatures.

13. **Get Daily Average Temperatures for a Room**
    - **Method:** GET
    - **URL:** `/api/v1/daily_avg/<int:room_id>`
    - **Description:** Calculates the daily average temperatures for a room within a specified date range.
    - **Query Parameters:**
      - `start_date` (string): The start date of the range in the format `%Y-%m-%dT%H:%M`.
      - `end_date` (string): The end date of the range in the format `%Y-%m-%dT%H:%M`.
    - **Response:** JSON object containing arrays of dates and corresponding average temperatures:
      - `dates` (array of strings): The dates of the measurements.
      - `averages` (array of floats): The corresponding average temperatures.

14. **Get Daily Average Temperatures for All Rooms**
    - **Method:** GET
    - **URL:** `/api/v1/daily_averages`
    - **Description:** Calculates the daily average temperatures for all rooms within a specified date range.
    - **Query Parameters:**
      - `start_date` (string): The start date of the range in the format `%Y-%m-%dT%H:%M`.
      - `end_date` (string): The end date of the range in the format `%Y-%m-%dT%H:%M`.
    - **Response:** JSON object containing an array of average temperature records, each containing:
      - `room_id` (int): The ID of the room.
      - `date` (string): The date of the measurement.
      - `temperature` (float): The average temperature for that day.
