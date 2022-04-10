from app.exceptions.anime_exc import IdNotExistent
from app.models import DatabaseConnect
from psycopg2 import sql


class Animes(DatabaseConnect):
    animes_columns = ['id', 'anime', 'released_date', 'seasons']
    
    def __init__(self, **kwargs):
        self.anime = kwargs['anime']
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']
        
    def format_title(self):
        self.anime = self.anime.split(' ')
        self.anime = [a.capitalize() for a in self.anime]
        self.anime = " ".join(self.anime)     
        
    @classmethod
    def serialize(cls, data: tuple):
        return dict(zip(cls.animes_columns, data))    
        
    @classmethod
    def create_table(cls):
        cls.table = """
            CREATE TABLE IF NOT EXISTS animes (
                id  BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL
            );           
        """        

    @classmethod
    def read_animes(cls):
        cls.get_conn_cur()
        
        cls.create_table()
        cls.cur.execute(cls.table)  
        
        query = "SELECT * FROM animes;"
        
        cls.cur.execute(query)
        
        animes = cls.cur.fetchall()
        
        cls.commit_and_close()
        
        serialized = [cls.serialize(anime) for anime in animes]
        
        for anime in serialized:
            anime['released_date'] = anime['released_date'].strftime("%d/%m/%Y")
        
        return serialized
    
    @classmethod
    def read_animes_by_id(cls, anime_id):
        cls.get_conn_cur()
        
        sql_anime_id = sql.Literal(anime_id)

        query = sql.SQL(
            """
                SELECT * FROM animes WHERE id = {id}
            """
        ).format(id=sql_anime_id)
        
        cls.cur.execute(query)
        
        anime = cls.cur.fetchone()
        
        cls.commit_and_close()
        
        if not anime:
            raise IdNotExistent
        
        serialized = cls.serialize(anime)
        serialized['released_date'] = serialized['released_date'].strftime("%d/%m/%Y")

        return serialized
    
    
    def add_anime(self):
        self.format_title()
        self.get_conn_cur()
        
        self.create_table()
        self.cur.execute(self.table)
        
        query_values = tuple(self.__dict__.values())
        query = """
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *;
        """        
        
        self.cur.execute(query, query_values)
        
        insert_anime = self.cur.fetchone()
   
        self.commit_and_close(commit = True)
        
        serialized = self.serialize(insert_anime)
        serialized['released_date'] = serialized['released_date'].strftime("%d/%m/%Y")
        
        return serialized
    
    @classmethod
    def update_anime(cls, anime_id, payload: dict):
        for key in payload.keys():
            print(key)
            if key == 'anime':
                payload[key] = payload[key].split(' ')
                payload[key] = [a.capitalize() for a in payload[key]]
                payload[key] = " ".join(payload[key])     
        
        cls.get_conn_cur()
        
        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]
        sql_user_id = sql.Literal(anime_id)
        
        query = sql.SQL(
            """
            UPDATE
                animes
            SET
                ({columns}) = ROW({values})
            WHERE
                ID = {id}
            RETURNING *;
            
            """
        ).format(id=sql_user_id, columns=sql.SQL(',').join(columns), values=sql.SQL(',').join(values))
        
        cls.cur.execute(query)
        
        update_user = cls.cur.fetchone()
        
        cls.commit_and_close(commit = True)
        
        if not update_user:
            raise IdNotExistent
        
        serialized = cls.serialize(update_user)
        serialized['released_date'] = serialized['released_date'].strftime("%d/%m/%Y")
        
        return serialized        
        
    @classmethod    
    def delete_anime(cls, anime_id):
        cls.get_conn_cur()
        
        sql_anime_id = sql.Literal(anime_id)
        
        query = sql.SQL(
            """
                DELETE FROM animes WHERE id = {id} RETURNING *;
            """
        ).format(id=sql_anime_id)
        
        cls.cur.execute(query)
        
        delete_anime = cls.cur.fetchone()
                
        cls.commit_and_close(commit = True)
        
        if not delete_anime:
            raise IdNotExistent
        
