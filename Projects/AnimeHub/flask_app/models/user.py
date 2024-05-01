from flask import flash
from re import compile
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
from flask_app.models import anime

#parent table (User model)
class User:
    _db = "AnimeHub_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.animes = []
        self.user_watchlist = []

    @staticmethod
    def registration_is_valid(form_data):
        """This method validates the registration form"""
        is_valid = True

        if len(form_data["first_name"].strip()) == 0:
            flash("please enter first name" , "register")
            is_valid = False
        elif len(form_data["first_name"].strip()) < 2:
            flash("First name must be at least 2 characters" , "register")
        
        if len(form_data["last_name"].strip()) == 0:
            flash("please enter last name" , "register")
            is_valid = False
        elif len(form_data["last_name"].strip()) < 2:
            flash("Last name must be at least 2 characters" , "register")

        if len(form_data["email"].strip()) == 0:
            flash("please enter email" , "register")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("invalid email address" , "register")
            is_valid = False

        if len(form_data["password"].strip()) == 0:
            flash("please enter password" , "register")
            is_valid = False
        elif len(form_data["password"].strip()) < 8:
            flash("Password must be at least 8 characters" , "register")
            is_valid = False
        elif form_data["password"] != form_data["confirm_password"]:
            flash("Passwords do not match" , "register")
            is_valid = False

        return is_valid

    @staticmethod
    def login_is_valid(form_data):
            is_valid = True

            if len(form_data["email"].strip()) == 0:
                flash("please enter email" , "login")
                is_valid = False
            elif not EMAIL_REGEX.match(form_data["email"].strip()):
                flash("invalid email address" , "login")
                is_valid = False

            if len(form_data["password"].strip()) == 0:
                flash("please enter password" , "login")
                is_valid = False
            elif len(form_data["password"].strip()) < 6:
                flash("Password must be at least 6 characters" , "login")
                is_valid = False
           
            return is_valid

    @classmethod
    def register(cls, user_data):
           """Creates a new user from a form"""
           query = """
           INSERT INTO users
           (first_name, last_name, email, password)
           VALUES
           (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
           """
           user_id = connectToMySQL(User._db).query_db(query, user_data)
           return user_id
    
    @classmethod
    def find_by_email(cls, email):
        """Finds one user by email in the db"""
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email": email}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user
    
    @classmethod
    def find_by_id(cls, user_id):
        """Finds one user by id in the db"""
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user
    
    @classmethod
    def find_by_id_with_animes(cls, user_id):
        """Finds one user by id and their animes in the db"""
        query = """
        SELECT * FROM users
        LEFT JOIN animes ON users.id = animes.user_id
        WHERE users.id = %(user_id)s;
        """
        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        for each_dict in list_of_dicts:
            for key in each_dict.keys():
                print(key)
            if each_dict["animes.id"] != None:
                anime_data = {
                    "id": each_dict["animes.id"],
                    "title": each_dict["title"],
                    "studio": each_dict["studio"],
                    "description": each_dict["description"],
                    "created_at": each_dict["animes.created_at"],
                    "updated_at": each_dict["animes.updated_at"],
                    "user_id": each_dict["user_id"],
                }
                anime = anime.Anime(anime_data)
                user.animes.append(anime)
        return user
    
