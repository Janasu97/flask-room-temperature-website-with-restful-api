import os
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request, jsonify


from dbqueries import (
    create_rooms_table,
    create_temps_table,
    create_room_return_id,
    get_rooms,
    get_room_name,
    update_room,
    delete_room,
    create_temp_return_id,
    get_temperatures,
    get_temperatures_for_room,
    update_temperature,
    delete_temperature,
    delete_temperatures_from_room,
    global_avg,
    global_number_of_days,
    daily_avg,
    daily_averages
)

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("DATABASE_URL"),
        port=os.getenv("PORT")
    )
    return conn

api = Flask(__name__)

conn = get_db_connection()
conn.autocommit = True


@api.post("/api/v1/room")
def createRoom():
    data = request.get_json()
    name = data["name"]

    # Ensure data is in the right format
    if not name:
        return jsonify({"error": "Name is required."}), 400

    try:
        with conn.cursor() as cur:
            cur.execute(create_rooms_table)
            cur.execute(create_room_return_id, (name,))
            room_id = cur.fetchone()[0]
        return jsonify({"id": room_id, "message": f"Room {name} created."}), 201
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.get("/api/v1/room")
def getRooms():
    try:
        with conn.cursor() as cur:
            cur.execute(get_rooms)
            rooms = cur.fetchall()

        rooms_list = [{"id": room[0], "name": room[1]} for room in rooms]

        # Return the list of rooms in JSON format along with the response code
        return jsonify({'rooms': rooms_list}), 200

    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.get("/api/v1/room/<int:room_id>")
def getRoomName(room_id):
    try:
        with conn.cursor() as cur:
            cur.execute(get_room_name, (room_id,))
            room = cur.fetchone()
            if cur.rowcount == 0:
                return jsonify({"message": f"No room with id {room_id}"}), 400
        # Return the room id and name
        return jsonify({"id": room[0], "name": room[1]}), 200

    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.put("/api/v1/room/<int:room_id>")
def updateRoom(room_id):
    if not isinstance(room_id, int):
            return jsonify({"error": "Invalid room ID."}), 400

    data = request.get_json()
    new_name = data.get("name")

    # Ensure data is in the right format
    if not new_name:
            return jsonify({"error": "New name is required."}), 400

    try:
        with conn.cursor() as cur:
            cur.execute(update_room, (new_name, room_id))
            if cur.rowcount == 0:
                return jsonify({"message": f"Room {room_id} not found."}), 404
            else:
                return jsonify({"message": f"Room {room_id} updated with name {new_name}."}), 200
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.delete("/api/v1/room/<int:room_id>")
def deleteRoom(room_id):
    if not isinstance(room_id, int):
        return jsonify({"error": "Invalid room ID."}), 400
    try:
        with conn.cursor() as cur:
            cur.execute(delete_room, (room_id,))
            if cur.rowcount == 0:
                return jsonify({"message": f"Room {room_id} not found."}), 404
            else:
                return jsonify({"message": f"Room {room_id} deleted."}), 200
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500




@api.post("/api/v1/temperature")
def createTemp():
    data = request.get_json()
    temperature = data["temperature"]
    room_id = data["room_id"]
    print(temperature)

    #Ensure data is in the right format
    if not temperature:
        return jsonify({"error": "Temperature is required."}), 400

    try:
        temperature = float(temperature)
    except ValueError:
        return jsonify({"error": "Invalid temperature. Must be a number."}), 400

    if not room_id:
        return jsonify({"error": "Room id is required."}), 400

    try:
        room_id = int(room_id)
    except ValueError:
        return jsonify({"error": "Invalid room id. Must be a number."}), 400

    try:
        date = datetime.strptime(data["date"], "%d-%m-%Y %H:%M")
    except KeyError:
        date = datetime.now(timezone.utc)
    except ValueError:
        print("Got data in the incorrect format")
        date = datetime.now(timezone.utc)

    try:
        with conn.cursor() as cur:
            cur.execute(create_temps_table)
            cur.execute(create_temp_return_id, (room_id, temperature, date))
            temp_id = cur.fetchone()[0]
            if cur.rowcount == 0:
                return jsonify({"message": f"Room {room_id} not found."}), 404
            else:
                return jsonify({"id": temp_id, "message": f"New temperature added in room {room_id}.", }), 201
    except psycopg2.IntegrityError as integrity_error:
        # Handle integrity constraint violation errors (e.g., foreign key constraint violation)
        return jsonify({"error": "Integrity constraint violation: " + str(integrity_error)}), 400
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.get("/api/v1/temperature")
def getTemp():
    try:
        with conn.cursor() as cur:
            cur.execute(get_temperatures)
            temp_data = cur.fetchall()

        temperatures = [{"id": temp[0], "room_id":temp[1], "temperature": temp[2], "date":temp[3]} for temp in temp_data]

        return jsonify({"temperatures": temperatures}), 200
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.get("/api/v1/temperature/<int:room_id>")
def getTempForRoom(room_id):
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if start_date is None:
            start_date = datetime(1, 1, 1, 0, 0)
        if end_date is None:
            end_date = datetime.now()

        def validateDateTime(datetime_str):
            try:
                datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
                return True
            except ValueError:
                return False

        if not validateDateTime(start_date):
            return jsonify({"error": "Invalid datetime format. Please use '%Y-%m-%dT%H:%M'"}), 400
        if not validateDateTime(end_date):
            return jsonify({"error": "Invalid datetime format. Please use '%Y-%m-%dT%H:%M'"}), 400
    except:
        #In case the dates would not be provided just use the earliest date possible for start, and now for end date
        start_date = datetime(1, 1, 1, 0, 0)
        end_date = datetime.now()

    try:
        with conn.cursor() as cur:
            cur.execute(get_temperatures_for_room, (room_id, start_date, end_date))
            temp_data = cur.fetchall()

        temperatures = [{"id": temp[0], "room_id":temp[1], "temperature": temp[2], "date":temp[3]} for temp in temp_data]

        return jsonify({"temperatures": temperatures}), 200
    except psycopg2.IntegrityError as integrity_error:
        # Handle integrity constraint violation errors (e.g., foreign key constraint violation)
        return jsonify({"error": "Integrity constraint violation: " + str(integrity_error)}), 400
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.put("/api/v1/temperature/<int:temp_id>")
def updateTemp(temp_id):
    if not isinstance(temp_id, int):
        return jsonify({"error": "Invalid room ID."}), 400

    data = request.get_json()
    new_temperature = data.get("temperature")
    new_date = data.get("date")
    new_room_id = data.get("room_id")

    #Ensure data is in the right format
    if not new_temperature:
        return jsonify({"error": "Temperature is required."}), 400

    try:
        new_temperature = float(new_temperature)
    except ValueError:
        return jsonify({"error": "Invalid temperature. Must be a number."}), 400

    if not new_room_id:
        return jsonify({"error": "Room id is required."}), 400

    try:
        new_room_id = int(new_room_id)
    except ValueError:
        return jsonify({"error": "Invalid room id. Must be a number."}), 400

    try:
        new_date = datetime.strptime(data["date"], "%d-%m-%Y %H:%M")
    except KeyError:
        new_date = datetime.now(timezone.utc)
    except ValueError:
        print("Got data in the incorrect format")
        new_date = datetime.now(timezone.utc)

    try:
        with conn.cursor() as cur:
            cur.execute(update_temperature, (new_room_id, new_temperature, new_date, temp_id))
            if cur.rowcount == 0:
                return jsonify({"message": f"Temp with id {temp_id} not found."}), 404
            else:
                return jsonify({"message": f"Temp with id {temp_id} updated."}), 200
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.delete("/api/v1/temperature/<int:temp_id>")
def deleteTemp(temp_id):
    if not isinstance(temp_id, int):
        return jsonify({"error": "Invalid temperature ID."}), 400
    try:
        with conn.cursor() as cur:
            cur.execute(delete_temperature, (temp_id,))
            if cur.rowcount == 0:
                return jsonify({"message": f"Temperature with id {temp_id} not found."}), 404
            else:
                return jsonify({"message": f"Temperature with id {temp_id} deleted."}), 200
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.delete("/api/v1/temperature_room/<int:room_id>")
def deleteTempFromRoom(room_id):
    if not isinstance(room_id, int):
        return jsonify({"error": "Invalid room ID."}), 400
    try:
        with conn.cursor() as cur:
            cur.execute(delete_temperatures_from_room, (room_id,))
            if cur.rowcount == 0:
                return jsonify({"message": f"No temperatures in room with id {room_id}."}), 404
            else:
                return jsonify({"message": f"All temperatures from room with id {room_id} deleted."}), 200
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500




@api.get("/api/v1/average/<int:room_id>")
def getGlobalAvg(room_id):
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(global_avg, (room_id,))
                average = cur.fetchone()[0]
                cur.execute(global_number_of_days, (room_id,))
                days = cur.fetchone()[0]
                if average != None:
                    return jsonify({"average": round(average, 2), "days": days}), 200
                else:
                    return jsonify({"Message": "No temperatures data for that room"}), 200
    except psycopg2.IntegrityError as integrity_error:
        # Handle integrity constraint violation errors (e.g., foreign key constraint violation)
        return jsonify({"error": "Integrity constraint violation: " + str(integrity_error)}), 400
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.get("/api/v1/daily_avg/<int:room_id>")
def getDailyAvg(room_id):

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date is None:
        return jsonify({"error": "The start date have to be provided"}), 400
    if end_date is None:
        return jsonify({"error": "The end date have to be provided"}), 400

    def validateDateTime(datetime_str):
        try:
            datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
            return True
        except ValueError:
            return False

    if not (validateDateTime(start_date) and validateDateTime(end_date)):
        return jsonify({"error": "Invalid datetime format. Please use '%Y-%m-%dT%H:%M'"}), 400

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(daily_avg, (room_id, start_date, end_date))
                avg_data = cur.fetchall()
                date_list = []
                average_list = []
                for avg_day in avg_data:
                    date_list.append(avg_day[0])
                    average_list.append(round(avg_day[1], 2))

                if len(average_list) > 0:
                    return jsonify({"dates": date_list, "averages": average_list}), 200
                else:
                    return jsonify({"Message": "No temperatures data for that room"}), 200
    except psycopg2.IntegrityError as integrity_error:
        # Handle integrity constraint violation errors (e.g., foreign key constraint violation)
        return jsonify({"error": "Integrity constraint violation: " + str(integrity_error)}), 400
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


@api.get("/api/v1/daily_averages")
def getDailyAverages():

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date is None:
        return jsonify({"error": "The start date have to be provided"}), 400
    if end_date is None:
        return jsonify({"error": "The end date have to be provided"}), 400

    def validateDateTime(datetime_str):
        try:
            datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
            return True
        except ValueError:
            return False

    if not (validateDateTime(start_date) and validateDateTime(end_date)):
        return jsonify({"error": "Invalid datetime format. Please use '%Y-%m-%dT%H:%M'"}), 400

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(daily_averages, (start_date, end_date))
                data = cur.fetchall()
                averages = [{"room_id": rec[0], "date":rec[1], "temperature": rec[2]} for rec in data]

                if len(averages) > 0:
                    return jsonify({"averages": averages}), 200
                else:
                    return jsonify({"Message": "No daily averages that day"}), 200
    except psycopg2.IntegrityError as integrity_error:
        # Handle integrity constraint violation errors (e.g., foreign key constraint violation)
        return jsonify({"error": "Integrity constraint violation: " + str(integrity_error)}), 400
    except psycopg2.DatabaseError as db_error:
        # Handle database-related errors
        return jsonify({"error": "Database error: " + str(db_error)}), 500
    except Exception as e:
        api.logger.error("An unexpected error occurred: %s", str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


api.run(host='0.0.0.0', port=5001, debug=True)


