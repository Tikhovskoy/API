import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def is_shorten_link(url: str) -> bool:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    return "vk.cc" in domain


def shorten_link(token: str, url: str) -> str:
    api_url = "https://api.vk.com/method/utils.getShortLink"
    params = {"access_token": token, "v": "5.131", "url": url}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "response" in data:
            return data["response"]["short_url"]
        elif "error" in data:
            error_msg = data["error"].get("error_msg", "Неизвестная ошибка")
            raise Exception(f"Ошибка API VK: {error_msg}")
        else:
            raise Exception("Некорректный ответ от сервера")
    except requests.RequestException as e:
        raise Exception(f"Ошибка сети: {e}")


def count_clicks(token: str, short_url: str) -> int:
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    parsed_url = urlparse(short_url)
    key = parsed_url.path.lstrip('/')
    params = {"access_token": token, "v": "5.131", "key": key, "interval": "forever"}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if "response" in data:
            stats = data["response"].get("stats", [])
            return stats[0].get("count", 0) if stats else 0
        elif "error" in data:
            error_msg = data["error"].get("error_msg", "Неизвестная ошибка")
            raise Exception(f"Ошибка API VK: {error_msg}")
        else:
            raise Exception("Некорректный ответ от сервера")
    except requests.RequestException as e:
        raise Exception(f"Ошибка сети: {e}")


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")
    if not token:
        raise Exception("Не найден VK_TOKEN в .env")

    url = input("Введите ссылку: ").strip()

    if is_shorten_link(url):
        clicks = count_clicks(token, url)
        return {"action": "count", "data": clicks}
    else:
        short_url = shorten_link(token, url)
        return {"action": "shorten", "data": short_url}


if __name__ == "__main__":
    try:
        result = main()
        if result["action"] == "count":
            print(f"Количество переходов по ссылке: {result['data']}")
        elif result["action"] == "shorten":
            print("Сокращенная ссылка:", result["data"])
    except Exception as e:
        print(f"Произошла ошибка: {e}")
