from http import HTTPStatus
from datetime import datetime as dt
from flask import request
from psycopg2.errors import UniqueViolation, UndefinedTable, UndefinedColumn
from app.exceptions.anime_exc import IdNotExistent
from app.models.animes_model import Animes


def create_anime():
    data = request.get_json()
    
    try:
        anime = Animes(**data)

        insert_anime = anime.add_anime()

        return insert_anime, HTTPStatus.CREATED
    except KeyError:
            available_keys = ["anime", "released_date", "seasons"]
            wrong_keys_sended = [key for key in  set(data.keys()) if not key in available_keys]         
            return {'available_keys': available_keys, "wrong_keys_sended": wrong_keys_sended}, HTTPStatus.UNPROCESSABLE_ENTITY
    except UniqueViolation:
        return {"error": "anime is already exists"}, HTTPStatus.UNPROCESSABLE_ENTITY
   
    
def retrieve_animes():
    animes = Animes.read_animes()
       
    return {'data': animes}, HTTPStatus.OK


def retrieve_anime_by_id(anime_id: int):
    try:
        anime = Animes.read_animes_by_id(anime_id)
        return {'data': [anime]}, HTTPStatus.OK
    except (IdNotExistent, UndefinedTable):
        return {'error': 'Not Found'}, HTTPStatus.NOT_FOUND
    
def update_anime(anime_id: int):
    data = request.get_json()
    

    try:
        anime = Animes.update_anime(anime_id, data)
        return anime, HTTPStatus.OK
    except (IdNotExistent, UndefinedTable):
        return {'error': 'Not Found'}, HTTPStatus.NOT_FOUND
    except UndefinedColumn:
        available_keys = ["anime", "released_date", "seasons"]
        wrong_keys_sended = [key for key in  set(data.keys()) if not key in available_keys]         
        return {'available_keys': available_keys, "wrong_keys_sended": wrong_keys_sended}, HTTPStatus.UNPROCESSABLE_ENTITY

def delete(anime_id: int):
    try:
        Animes.delete_anime(anime_id)
        
        return "", HTTPStatus.NO_CONTENT
    except (IdNotExistent, UndefinedTable):
        return {'error': 'Not Found'}, HTTPStatus.NOT_FOUND