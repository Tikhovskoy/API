import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def is_shorten_link(token: str, url: str) -> bool:
    parsed_url = urlparse(url)
    if parsed_url.netloc.lower() != "vk.cc":
        return False

    key = parsed_url.path.lstrip('/')
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": "5.131",
        "key": key,
        "interval": "forever"
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    return "response" in response.json()


def shorten_link(token: str, url: str) -> str:
    api_url = "https://api.vk.com/method/utils.getShortLink"
    params = {"access_token": token, "v": "5.131", "url": url}

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    shorten_response = response.json()

    if "response" in shorten_response:
        return shorten_response["response"]["short_url"]

    if "error" in shorten_response:
        error_msg = shorten_response["error"].get("error_msg", "Неизвестная ошибка")
        raise Exception(f"Ошибка API VK: {error_msg}")

    raise Exception("Некорректный ответ от сервера")


def count_clicks(token: str, short_url: str) -> int:
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    parsed_url = urlparse(short_url)
    key = parsed_url.path.lstrip('/')

    params = {"access_token": token, "v": "5.131", "key": key, "interval": "forever"}

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    clicks_response = response.json()

    if "response" in clicks_response:
        stats = clicks_response["response"].get("stats", [])
        return stats[0].get("count", 0) if stats else 0

    if "error" in clicks_response:
        error_msg = clicks_response["error"].get("error_msg", "Неизвестная ошибка")
        raise Exception(f"Ошибка API VK: {error_msg}")

    raise Exception("Некорректный ответ от сервера")


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")
    if not token:
        raise Exception("Не найден VK_TOKEN в .env")

    url = input("Введите ссылку: ").strip()

    if is_shorten_link(token, url):
        return f"Количество переходов по ссылке: {count_clicks(token, url)}"
    return f"Сокращенная ссылка: {shorten_link(token, url)}"


if __name__ == "__main__":
    try:
        print(main())
    except Exception as e:
        print(f"Произошла ошибка: {e}")
