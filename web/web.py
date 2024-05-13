import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
import requests
from datetime import datetime, timezone
from flask_cors import CORS

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("DATABASE_URL"),
        port=os.getenv("PORT")
    )
    return conn

web = Flask(__name__, template_folder='templates', static_url_path='/static')
CORS(web)
conn = get_db_connection()
conn.autocommit = True


@web.route('/')
def menu():
    return render_template('menu.html')


@web.route('/create_room', methods=['POST'])
def create_room():
    try:
        # Extract form data from the request
        form_data = request.json
        room_name = form_data.get('name')
        print(room_name)
        # Make POST request to the API endpoint
        api_url = 'http://127.0.0.1:5001/api/v1/room'
        data = {'name': room_name}

        response = requests.post(api_url, json=data)
        data_retrieved = response.json()
        room_id = data_retrieved.get("id")

        # Check if the request was successful
        if response.status_code == 201:
            return jsonify({'message': 'Temperature data added successfully!', "room_id": room_id, "name": room_name}), 201
        else:
            return jsonify({'error': f'Error: {response.status_code} - {response.text}'}), 500

    except requests.RequestException as e:
        # Handle any errors that occur during the request to the API
        return jsonify({"error": "Error while creating new room: " + str(e)}), 500
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


@web.route('/get_rooms')
def get_rooms():
    try:
        # Make a request to the API endpoint to fetch rooms data
        response = requests.get('http://127.0.0.1:5001/api/v1/room')
        rooms_data = response.json()

        # Extract the rooms data from the response
        rooms = rooms_data.get('rooms', [])

        today = datetime.today()
        start_date = today.replace(hour=0, minute=0).strftime("%Y-%m-%dT%H:%M")
        end_date = today.replace(hour=23, minute=59).strftime("%Y-%m-%dT%H:%M")
        try:
            response = requests.get(f"http://127.0.0.1:5001/api/v1/daily_averages",
                                    params={"start_date": start_date, "end_date": end_date})
            data = response.json()
            averages = data['averages']
            for room in rooms:
                room_id = room["id"]
                room["avg_temperature"] = None
                for avg in averages:
                    if room_id == avg.get("room_id"):
                        room["avg_temperature"] = round(avg.get("temperature"),2)
                        break


        except Exception as e:
            print("An error occurred:", e)

        # Return the list of rooms in JSON format along with the response code
        return jsonify({'rooms': rooms}), 200

    except requests.RequestException as e:
        # Handle any errors that occur during the request to the API
        return jsonify({"error": "Error fetching rooms data: " + str(e)}), 500
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


@web.route('/get_room_temperatures', methods=['GET'])
def get_room_temperatures():
    try:
        room_id = request.args.get('room_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not isinstance(int(room_id), int):
            return jsonify({"error": "Wrong room_id. You have to provide it."}), 500

        start_date += "T00:00"
        end_date += "T23:59"
        print(start_date, end_date, room_id)
        response = requests.get(f"http://127.0.0.1:5001/api/v1/temperature/{room_id}",
                                params={"start_date": start_date, "end_date": end_date})
        print(response.status_code)
        data = response.json()
        temperatures = data.get("temperatures")

        if len(temperatures) > 0:
            return jsonify({"temperatures": temperatures}), 200
        else:
            return jsonify({'message': "No temperatures for that room"}), 404

    except requests.RequestException as e:
        # Handle any errors that occur during the request to the API
        return jsonify({"error": "Error fetching rooms data: " + str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Error fetching rooms data: " + str(e)}), 500


@web.route("/delete_room",  methods=['DELETE'])
def delete_room():
    try:
        form_data = request.json
        room_id = form_data.get('room_id')

        #First we have to delete all temperatures from the room
        api_url = f'http://127.0.0.1:5001/api/v1/temperature_room/{room_id}'

        response = requests.delete(api_url)

        if response.status_code == 200 or response.status_code == 404:

            api_url = f'http://127.0.0.1:5001/api/v1/room/{room_id}'

            response = requests.delete(api_url)

            # Check if the request was successful
            if response.status_code == 200:
                return jsonify({'message': 'The selected room deleted successfully', "room_id": room_id}), 200
            else:
                return jsonify({'error': f'Error: {response.status_code} - {response.text}'}), 500
        else:
            return jsonify({'error': f'Error: {response.status_code} - {response.text}',
                            'detail': 'Problem with deleting the temperatures from room'}), 500

    except requests.RequestException as e:
        # Handle any errors that occur during the request to the API
        return jsonify({"error": "Error while creating new room: " + str(e)}), 500
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500


@web.route('/room/<int:room_id>')
def room(room_id):
    return render_template('room.html', room_id=room_id)


@web.route('/submit_temperature', methods=['POST'])
def submit_temperature():
    # Extract form data from the request
    form_data = request.json
    temperature = form_data.get('temperature')
    room_id = form_data.get('room_id')
    date = form_data.get('date')

    try:
        datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M")
    except KeyError:
        datetime_object = datetime.now(timezone.utc)

    date = str(datetime_object.strftime("%d-%m-%Y %H:%M"))

    # Make POST request to the API endpoint
    api_url = 'http://127.0.0.1:5001/api/v1/temperature'
    data = {'temperature': temperature, 'room_id': room_id, 'date': date}

    response = requests.post(api_url, json=data)
    data_retrieved = response.json()

    # Check if the request was successful
    if response.status_code == 201:
        temp_id = data_retrieved.get("id")
        return jsonify({'id': temp_id, 'message': 'Temperature data added successfully!'}), 201
    else:
        return jsonify({'error': f'Error: {response.status_code} - {response.text}'}), 500


@web.route('/update_temperature', methods=['PUT'])
def update_temperature():
    # Extract form data from the request
    form_data = request.json
    temperature = form_data.get('temperature')
    room_id = form_data.get('room_id')
    date = form_data.get('date')
    id = form_data.get('id')

    try:
        datetime_object = datetime.strptime(date, "%Y-%m-%dT%H:%M")
    except KeyError:
        datetime_object = datetime.now(timezone.utc)

    date = str(datetime_object.strftime("%d-%m-%Y %H:%M"))
    # Make POST request to the API endpoint
    api_url = f'http://127.0.0.1:5001/api/v1/temperature/{id}'
    data = {'temperature': temperature, 'room_id': room_id, 'date': date}
    response = requests.put(api_url, json=data)
    # Check if the request was successful
    if response.status_code == 200:
        return jsonify({'message': 'Temperature data updated successfully!'}), 200
    else:
        return jsonify({'error': f'Error: {response.status_code} - {response.text}'}), 500


@web.route("/delete_temperature",  methods=['DELETE'])
def delete_temperature():
    try:
        form_data = request.json
        id = form_data.get('id')

        #First we have to delete all temperatures from the room
        api_url = f'http://127.0.0.1:5001/api/v1/temperature/{id}'

        response = requests.delete(api_url)

        if response.status_code == 200:
            return jsonify({'message': 'The selected temperature deleted successfully'}), 200
        elif response.status_code == 404:
            return jsonify({'message': 'The selected temperature not existing in the data file'}), 404
        else:
            return jsonify({'error': f'Error: {response.status_code} - {response.text}',
                            'detail': 'Problem with deleting the temperatures from room'}), 500

    except requests.RequestException as e:
        # Handle any errors that occur during the request to the API
        return jsonify({"error": "Error while creating new room: " + str(e)}), 500
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500



web.run(host='0.0.0.0', port=5000, debug=True)
