from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "locations"


class Location:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.type = db_data['type']
        self.address = db_data['address']
        self.description = db_data['description']
        self.date_made = db_data['date_made']
        self.amount = db_data['amount']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['users_id']
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM locations
                JOIN users on locations.users_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        locations = []
        for row in results:
            this_location = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_location.creator = user.User(user_data)
            locations.append(this_location)
        return locations

    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM locations
                JOIN users on locations.users_id = users.id
                WHERE locations.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False

        result = result[0]
        this_location = cls(result)
        user_data = {
            "id": result['users.id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "password": "",
            "created_at": result['users.created_at'],
            "updated_at": result['users.updated_at']
        }
        this_location.creator = user.User(user_data)
        return this_location

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO locations (type,address,description,date_made,amount,users_id)
                VALUES (%(type)s,%(address)s,%(description)s,%(date_made)s,%(amount)s,%(users_id)s);
                """
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def update(cls, form_data):
        query = """
                UPDATE locations
                SET type = %(type)s,
                address = %(address)s,
                description = %(description)s,
                date_made = %(date_made)s,
                amount = %(amount)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def destroy(cls, data):
        query = """
                DELETE FROM locations
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_location(form_data):
        is_valid = True

        if len(form_data['type']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Description must be at least 3 characters long.")
            is_valid = False
        if form_data['date_made'] == '':
            flash("When did this occur!?")
            is_valid = False
        if 'amount' not in form_data:
            flash("How many!?")
            is_valid = False

        return is_valid
