import requests
import sqlite3
from flask import Flask, request, jsonify, Response
#import vicinity
import math 

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('secure_pay.db')
c = conn.cursor()

# Create the user login table
c.execute('''CREATE TABLE IF NOT EXISTS user_login 
             (username TEXT PRIMARY KEY, password TEXT)''')

# Create the qrtable
c.execute('''CREATE TABLE IF NOT EXISTS qrtable 
             (id TEXT PRIMARY KEY, latitude REAL, longitude REAL, b_name TEXT, vpa TEXT, gst TEXT)''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def insert_user_login(username, password):
    conn = sqlite3.connect('secure_pay.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_login (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def insert_qr_code(id, latitude, longitude, b_name, vpa, gst):
    conn = sqlite3.connect('secure_pay.db')
    c = conn.cursor()
    c.execute("INSERT INTO qrtable (id, latitude, longitude, b_name, vpa, gst) VALUES (?, ?, ?, ?, ?, ?)", (id, latitude, longitude, b_name, vpa, gst))
    conn.commit()
    conn.close()

def get_user_login(username):
    conn = sqlite3.connect('secure_pay.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_login WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_qr_codes(username):
    conn = sqlite3.connect('secure_pay.db')
    c = conn.cursor()
    c.execute("SELECT * FROM qrtable WHERE id=?", (username,))
    qr_codes = c.fetchall()
    conn.close()
    return qr_codes

@app.route('/', methods=['GET'])
def func():
    return "<h1>Secure Pay application Homepage</h1>"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user_login(username)
    if user is not None:
        return jsonify({'error': 'Username already exists'}), 400

    insert_user_login(username, password)

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = get_user_login(username)
    if user is None or user[1] != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful'}), 200

@app.route('/qrcodes', methods=['PUT'])
def add_qrcode():
    data = request.get_json()
    username = data.get('username')
    qrcode = data.get('qrcode')

    user = get_user_login(username)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    qr_codes = get_qr_codes(username)
    if any(qr_code[0] == qrcode['id'] for qr_code in qr_codes):
        return jsonify({'message': 'QR code already exists for this user'})

    insert_qr_code(qrcode['id'], qrcode['latitude'], qrcode['longitude'], qrcode['b_name'], qrcode['vpa'], qrcode['gst'])

    return jsonify({'message': 'QR code added successfully'}), 200

@app.route('/users')
def display_users():
    conn = sqlite3.connect('secure_pay.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_login")
    users = c.fetchall()
    conn.close()
    return jsonify(users)

def generate_qr_code(user_info):
    response = requests.get("https://upiqr.in/api/qr?name={}&vpa={}".format(user_info['merchant_name'], user_info['vpa']))
    svg_qr = response.content.decode('utf-8')
    return svg_qr


def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)*2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)*2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km    

@app.route('/view_qr', methods=['GET'])
def view_qr():
    username = request.args.get('username')
    password = request.args.get('password')

    user = get_user_login(username)
    if user is None:
        return jsonify({'error': 'User not found in the database'}), 401

    if user[1] != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    qr_codes = get_qr_codes(username)
    svg_content = [qr_code[0] for qr_code in qr_codes]
    return Response(svg_content, content_type='image/svg+xml')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    current_location = data.get('current_location')
    merchant_name = data.get('merchant_name')
    vpa = data.get('vpa')
    gst = data.get('gst')

    user = get_user_login(username)
    if user is None or user[1] != password:
        return jsonify({'error': 'Invalid credentials'}), 401

    qr_codes = get_qr_codes(username)
    for qr_code in qr_codes:
        if calculate_distance((qr_code[1], qr_code[2]), current_location) < 0.05:  # 50 meter threshold here
            return jsonify({'error': 'Another QR code exists in the vicinity'}), 400

    new_qr_code = generate_qr_code({'merchant_name': merchant_name, 'vpa': vpa})
    insert_qr_code(new_qr_code, current_location[0], current_location[1], merchant_name, vpa, gst)

    return jsonify({'message': 'QR code generated and added successfully'}), 200

if __name__ == '__main__':
    app.run(port=7070, host='0.0.0.0')