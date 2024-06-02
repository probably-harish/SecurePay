from flask import Flask, request, jsonify, Response
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('SecurePay.sqlite')
cursor = conn.cursor()
cursor.execute(
'''
    create table if not exists qrcodes
    (
               hash char(64) primary key,
               lat double not null,
               long double not null,
               bname varchar(100) not null,
               vpa varchar(100) not null,
               gst char(15)
    )
''')

conn.commit()
conn.close()

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.get_json()
    vpa = data.get('vpa')
    bname = data.get('bname')
    lat = data.get('lat')
    long = data.get('long')
    username = data.get('username')
    password = data.get('password')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7080)