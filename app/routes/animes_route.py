from flask import Blueprint
from app.controllers import animes_controller

bp = Blueprint("animes", __name__, url_prefix="/animes")

bp.post("")(animes_controller.create_anime)

bp.get("")(animes_controller.retrieve_animes)

bp.get("/<int:anime_id>")(animes_controller.retrieve_anime_by_id)

bp.patch("/<int:anime_id>")(animes_controller.update_anime)

bp.delete("/<int:anime_id>")(animes_controller.delete)