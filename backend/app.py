from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lind@1155@localhost/proyecto_software'
db = SQLAlchemy(app)

@app.route('/')
def hello():
    return 'Hey!'

@app.route('/event', methods=['POST'])
def create_event():
    
    description = request.json['description']

    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO event VALUES(%s)', (description))
        connection.commit()
    cursor.close()
    return 'success'

if __name__ == '__main__':
    app.run()