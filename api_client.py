import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.poiskkino.dev/v1.5/movie"
API_TOKEN = os.getenv("API_TOKEN")

HEADERS = {"Content-Type": "application/json",
           "X-API-KEY": API_TOKEN}


def _make_request(params: dict) -> list:
    """
    Внутренняя вспомогательная функция для отправки запросов.
    Она чистит пустые параметры, делает запрос и возвращает список документов [docs].
    """
    cleaned_params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(API_URL, headers=HEADERS, params=cleaned_params)

        if response.status_code == 200:
            return response.json().get("docs", [])
        else:
            print(f"Ошибка API {response.status_code}: {response.text}")
            return []

    except Exception as e:
        print(f"Ошибка сети: {e}")
        return []

def movie_search(name: str, genre: str = None, limit: int = 5) -> list:
    """Функция, которая выполняет поиск фильмов/сериалов по названию (/movie_search)"""
    params = {
        "notNullFields": "id",
        "withCount": "false",
        "name": name,
        "genres.name": genre,
        "limit": limit,
    }

    return _make_request(params)

def movie_by_rating(min_rating: float, max_rating: float = 10.0, genre: str = None, limit: int = 5) -> list:
    """Функция, которая выполняет поиск фильмов/сериалов по рейтингу (/movie_by_rating)"""
    params = {
        "notNullFields": "id",
        "limit": limit,
        "genres.name": genre,
        "rating.kp": f"{min_rating}-{max_rating}",
        "sortField": "rating.kp",
        "sortType": "-1",
        "withCount": "false",
        "type": "movie",
    }

    return _make_request(params)

def low_budget_movie(genre: str = None, limit: int = 5) -> list:
    """Функция, которая выполняет поиск фильмов/сериалов с низким бюджетом (/low_budget_movie)"""
    params = {
        "notNullFields": "id",
        "type": "movie",
        "limit": limit,
        "sortField": "budget.value",
        "sortType": "1",
        "genres.name": genre,
        "withCount": "false",
        "budget.value": "1000-500000"
    }

    return _make_request(params)

def high_budget_movie(genre: str = None, limit: int = 5) -> list:
    """Функция, которая выполняет поиск фильмов/сериалов с высоким бюджетом (/high_budget_movie)"""
    params = {
        "notNullFields": "id",
        "type": "movie",
        "budget.value": "100000000-500000000",
        "limit": limit,
        "sortField": "budget.value",
        "sortType": "-1",
        "withCount": "false",
        "genres.name": genre,
    }

    return _make_request(params)