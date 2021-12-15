from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


DB = "recipes_schema"

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.time = data['time']
        self.instruction = data['instruction']
        self.date_made_on = data['date_made_on']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    
    @classmethod
    def create_recipe(cls,data):
        query = """
            INSERT INTO recipes (name, description, time, instruction, date_made_on, updated_at, created_at, user_id) 
            VALUE (%(name)s,%(description)s, %(time)s, %(instruction)s, %(date_made_on)s, NOW(), NOW(), %(user_id)s);
        """
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def get_recipe(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DB).query_db(query)
        print(results)
        recipe = []
        for result in results:
            recipe.append(cls(result))
        return recipe

    @classmethod
    def get_one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        return cls(results[0])


    @classmethod
    def edit_recipe(cls,data):
        query = """
            UPDATE recipes SET name = %(name)s, description=%(description)s, time=%(time)s, instruction=%(instruction)s, 
            date_made_on=%(date_made_on)s, created_at =NOW(), updated_at= NOW() WHERE id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def delete_message(cls,data):
        query = "DELETE FROM recipes WHERE id =  %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        return results

    def date_time_string(cls):
        return cls.date_made_on.strftime("%d %b, %Y")

    @staticmethod
    def is_valid(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash ('Name must be at least 3 characters.','name')
        if len(recipe['description']) < 3:
            is_valid = False
            flash ('Description must be at least 3 characters.','name')
        if len(recipe['instruction']) < 3:
            is_valid = False
            flash ('Instruction must be at least 3 charactors.','name')
        return is_valid    


