#Table creation and updates
create_rooms_table = """CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"""

create_temps_table = """
    CREATE TABLE IF NOT EXISTS temperatures (id SERIAL PRIMARY KEY, room_id INTEGER, temperature REAL,
    date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE);
"""


#CRUD FOR ROOM
create_room_return_id = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"

get_rooms = "SELECT * FROM rooms ORDER BY id"

get_room_name = "SELECT id, name FROM rooms WHERE id = %s;"

update_room = "UPDATE rooms SET name = %s WHERE id = %s;"

delete_room = "DELETE FROM rooms WHERE id = %s;"


#CRUD FOR TEMPERATURE
create_temp_return_id = "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s) RETURNING id;"

get_temperatures = "SELECT id, room_id, temperature, date FROM temperatures;"

get_temperatures_for_room = """
    SELECT id, room_id, temperature, date FROM temperatures 
    WHERE room_id = %s AND date >= %s AND date <= %s
    ORDER by id;
    """

update_temperature = "UPDATE temperatures SET room_id = %s, temperature = %s, date = %s WHERE id = %s;"

delete_temperature = "DELETE FROM temperatures WHERE id = %s;"

delete_temperatures_from_room = "DELETE FROM temperatures WHERE room_id=%s"


#STATISTIC AND REST OF DATA OPERATIONS
global_number_of_days = "SELECT COUNT(DISTINCT DATE(date)) AS days FROM temperatures WHERE room_id = %s;"

global_avg = "SELECT AVG(temperature) AS average FROM temperatures WHERE room_id = %s;"

daily_avg = """
SELECT TO_CHAR(date, 'YYYY-MM-DD') AS date, AVG(temperature) AS average FROM temperatures 
WHERE room_id = %s AND date >= %s and date <= %s
GROUP BY TO_CHAR(date, 'YYYY-MM-DD') ORDER BY TO_CHAR(date, 'YYYY-MM-DD') DESC;
"""

daily_averages = """
SELECT room_id as room_id, TO_CHAR(date, 'YYYY-MM-DD')AS date, AVG(temperature) AS average FROM temperatures 
WHERE date >= %s and date <= %s
GROUP BY room_id, TO_CHAR(date, 'YYYY-MM-DD') ORDER BY date DESC;
"""


