from flask import flash
from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Anime: 
    _db = "AnimeHub_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.studio = data["studio"]
        self.description = data["description"]
        self.stream = data["stream"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @staticmethod
    def form_is_valid(form_data):
        is_valid = True
        # text validator
        if len(form_data["title"]) == 0:
            flash("please enter title")
            print("a")
            is_valid = False
        elif len(form_data["title"]) < 3:
            flash("title must be at least 3 characters")
            print("b")
            is_valid = False
        if len(form_data["studio"]) == 0:
            flash("please enter studio")
            print("c")
            is_valid = False
        elif len(form_data["studio"]) < 3:
            flash("studio must be at least 3 characters")
            print("d")
            is_valid = False
        if len(form_data["description"]) == 0:
            flash("please enter description")
            print("e")
            is_valid = False
        elif len(form_data["description"]) < 3:
            flash("description must be at least 3 characters")
            print("f")
            is_valid = False
        if len(form_data["stream"]) == 0:
            flash("please enter stream")
            print("e")
            is_valid = False
        elif len(form_data["stream"]) < 3:
            flash("stream must be at least 3 characters")
            print("f")
            is_valid = False

        return is_valid



    @classmethod
    def find_all(cls):
        """Finds all animes in the database"""

        query = "SELECT * FROM animes;"
        list_of_dicts = connectToMySQL(Anime._db).query_db(query)

        print("***********************ALL ANIMES****************")
        pprint(list_of_dicts)
        print("***********************ALL ANIMES****************")

        animes = []
        for each_dict in list_of_dicts:
            anime = Anime(each_dict)
            animes.append(anime)
        return animes
        
    @classmethod
    def find_all_with_users(cls):
        """Finds all animes with users in the database"""

        query = """
        SELECT * FROM animes 
        JOIN users 
        ON animes.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Anime._db).query_db(query)

        print("***********************ALL ANIMES****************")
        pprint(list_of_dicts)
        print("***********************ALL ANIMES****************")

        animes = []
        for each_dict in list_of_dicts:
            anime = Anime(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            print(each_dict)
            print(anime.id)
            user = User(user_data)
            anime.user = user
            animes.append(anime)
        return animes

    @classmethod
    def find_by_id(cls, anime_id):
        """Finds one anime by id in the database"""
        query = "SELECT * FROM animes WHERE id = %(anime_id)s;"
        data = {"anime_id": anime_id}
        list_of_dicts = connectToMySQL(Anime._db).query_db(query, data)
        
        anime = Anime(list_of_dicts[0])
        return anime
    
    @classmethod
    def find_by_id_with_users(cls, anime_id):
        """Finds one anime by id and the uploader in the database"""

        query = """
        SELECT * FROM animes 
        JOIN users 
        ON animes.user_id = users.id
        WHERE animes.id = %(anime_id)s;
        """
        data = {"anime_id": anime_id}
        list_of_dicts = connectToMySQL(Anime._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None
        
        anime = Anime(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        anime.user = User(user_data)
        return anime

    @classmethod
    def create(cls, form_data):
        """Creates a new Anime from a form"""
        query = """
        INSERT INTO animes
        (title, studio, description, stream, user_id)
        VALUES
        (%(title)s, %(studio)s, %(description)s, %(stream)s, %(user_id)s);
        """
        anime_id = connectToMySQL(Anime._db).query_db(query, form_data)
        return anime_id
    
    @classmethod
    def update_by_id(cls, form_data):
        """Updates a anime by its ID"""
        query = "UPDATE animes SET title = %(title)s, studio = %(studio)s, description = %(description)s, stream = %(stream)s WHERE id = %(anime_id)s;"
        connectToMySQL(Anime._db).query_db(query, form_data)
        return
    
    @classmethod
    def delete_by_id(cls, anime_id):
        """Deletes an anime by its ID"""
        query = "DELETE FROM animes WHERE id = %(anime_id)s;"
        data = {"anime_id": anime_id}
        connectToMySQL(Anime._db).query_db(query, data)
        return
    
    @classmethod
    def count_by_title(cls, title):
        """This method counts the number of anime by title"""
        query = """SELECT COUNT(title) as "count" 
        FROM animes 
        WHERE title = %(title)s;
        """
        data = {"title": title}
        list_of_dicts = connectToMySQL(Anime._db).query_db(query, data)
        pprint(list_of_dicts)
        return list_of_dicts[0]["count"]
    
    @classmethod
    def add_to_watchlist(cls, data):
        query = """
        INSERT INTO watchlist
        (user_id, anime_id, watch_status)
        VALUES
        (%(user_id)s, %(anime_id)s, %(watch_status)s);
        """
        connectToMySQL(Anime._db).query_db(query, data)
        return
 
