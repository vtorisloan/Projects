from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.anime import Anime

class Hub: 
    _db = "AnimeHub_schema"
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.anime_id = data["anime_id"]
        self.watch_status = data["watch_status"]


    @classmethod
    def remove(cls, data):
        """Removes an anime from our watch list."""
        query = """
        DELETE FROM watchlist
        WHERE user_id = %(user_id)s AND anime_id = %(anime_id)s;
        """
        connectToMySQL(Hub._db).query_db(query, data)
        return 
    
    @classmethod
    def add(cls, data):
        """Adds an anime to our watch list."""
        query = """
        INSERT INTO watchlist
        (user_id, anime_id, watch_status)
        VALUES
        (%(user_id)s, %(anime_id)s, %(watch_status)s);
        """
        connectToMySQL(Hub._db).query_db(query, data)
        return


    
    @classmethod
    def get_all_by_id(cls, data):
        """Gets all anime from our watch list."""
        query = """
        select *
        from watchlist w inner join animes a 
        on w.anime_id = a.id
        where w.user_id = %(user_id)s;
        """
        data = {"user_id": data}
        result = connectToMySQL(Hub._db).query_db(query, data)
        watchlist = []
        for dict in result: 
            for key, value in dict.items():
                print(key, "\t\t", value )
            # print(dict)
            anime_data = {
                "id": dict["a.id"],
                "title": dict["title"],
                "studio": dict["studio"],
                "description": dict["description"],
                "stream": dict["stream"],
                "user_id": dict["user_id"],
                "created_at": dict["created_at"],
                "updated_at": dict["updated_at"],
            }
            this_anime = Anime(anime_data)
            watchlist.append(this_anime)
        # print("A", result)
        return watchlist

