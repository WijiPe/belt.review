from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import math
from datetime import datetime

DB = "private_wall_schema"

class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.message = data['message']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.receiver_id = data['receiver_id']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif math.floor(delta.total_seconds()/60) >= 60:
            return f'{math.floor(math.floor(delta.total_seconds() /60)/60)} hours ago'
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minute ago"
        else:
            return f"{math.floor(delta.total_seconds())}"
    
    @classmethod
    def save_message(cls,data):
        query = "INSERT INTO message (message, sender_id, receiver_id, updated_at, created_at) VALUE (%(message)s,%(sender_id)s, %(receiver_id)s, NOW(), NOW());"
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def get_message(cls,data):
        query = "SELECT message.id, users.first_name AS sender, users2.first_name AS receiver, message.* FROM users LEFT JOIN message ON users.id = message.sender_id LEFT JOIN users AS users2 ON users2.id = message.receiver_id WHERE users2.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        print(results)
        message1 = []
        for message in results:
            message1.append(cls(message))
        return message1

    @classmethod
    def destroy_message(cls,data):
        query = "DELETE FROM message WHERE id =  %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def get_message_by_id(cls,data):
        query = "SELECT * FROM message WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        data = {**results[0], 'sender': '', 'receiver': ''}
        return cls(data)

