from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Show:
    def __init__(self,data):
        self.id = data ['id']
        self.user_id = data ['user_id']
        self.title = data ['title']
        self.network = data ['network']
        self.date = data ['date']
        self.description = data ['description']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']
    
    @staticmethod
    def validate_show(form):
        is_valid = True
        if len(form['title']) < 3:
            flash ('Title must be longer than 3 characters', 'title')
            is_valid = False
        if len(form['network']) < 3:
            flash ('Network must be longer than 3 characters', 'network')
            is_valid = False
        if form['date'] == "":
            flash('Date must be given!', 'date')
            is_valid = False
        if len(form['description']) < 3:
            flash ('Description must be longer than 3 characters', 'description')
            is_valid = False
        
        return is_valid
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (user_id, title, network, date, description) VALUES (%(user_id)s, %(title)s, %(network)s, %(date)s, %(description)s);"
        new_shows = connectToMySQL ('TV_shows').query_db(query, data)
    
        return new_shows
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results = connectToMySQL('TV_shows').query_db(query)
        shows = []

        for row in results:
            shows.append( cls(row) )
        
        return shows
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id WHERE shows.id = %(id)s;"
        result = connectToMySQL('TV_shows').query_db(query, data)
        return result[0]
    
    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET user_id=%(user_id)s, title=%(title)s, date=%(date)s, description=%(description)s, network=%(network)s WHERE id=%(id)s;"
        return connectToMySQL('TV_shows').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        connectToMySQL('TV_shows').query_db(query, data)