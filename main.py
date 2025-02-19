import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


<<<<<<< HEAD
API_VERSION = "5.131"
BASE_URL = "https://api.vk.com/method"


def is_short_link(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.netloc.lower() == "vk.cc" and bool(parsed_url.path.lstrip('/'))  


def get_click_stats(token: str, key: str) -> dict:
    params = {
        "access_token": token,
        "v": API_VERSION,
=======
def is_shorten_link(token: str, url: str) -> bool:
    parsed_url = urlparse(url)
    if parsed_url.netloc.lower() != "vk.cc":
        return False

    key = parsed_url.path.lstrip('/')
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": "5.131",
>>>>>>> parent of 48846a7 (Отредактировал код)
        "key": key,
        "interval": "forever"
    }

<<<<<<< HEAD
    response = requests.get(f"{BASE_URL}/utils.getLinkStats", params=params)
    response.raise_for_status()
    response_data = response.json()
    
    if "error" in response_data:
        raise Exception(f"Ошибка API VK: {response_data['error'].get('error_msg', 'Неизвестная ошибка')}")
    return response_data.get("response", {})


def count_clicks(link_stats: dict) -> int:
    if not link_stats or "stats" not in link_stats or not link_stats["stats"]:
        return 0
    return link_stats["stats"][0].get("count", 0)


def shorten_link(token: str, url: str) -> str:
    params = {"access_token": token, "v": API_VERSION, "url": url}

    response = requests.get(f"{BASE_URL}/utils.getShortLink", params=params)
    response.raise_for_status()
    response_data = response.json()

    if "error" in response_data:
        raise Exception(f"Ошибка API VK: {response_data['error'].get('error_msg', 'Неизвестная ошибка')}")

    return response_data.get("response", {}).get("short_url")


def main():
    try:
        load_dotenv()
        token = os.getenv("VK_TOKEN")
        if not token:
            raise Exception("Токен VK не найден")
=======
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
>>>>>>> parent of 48846a7 (Отредактировал код)

    url = input("Введите ссылку: ").strip()

<<<<<<< HEAD
        if is_short_link(url):
            key = urlparse(url).path.lstrip('/')
            link_stats = get_click_stats(token, key)
            print(f"Количество переходов по ссылке: {count_clicks(link_stats)}")
        else:
            print(f"Сокращенная ссылка: {shorten_link(token, url)}")

    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
=======
    if is_shorten_link(token, url):
        return f"Количество переходов по ссылке: {count_clicks(token, url)}"
    return f"Сокращенная ссылка: {shorten_link(token, url)}"
>>>>>>> parent of 48846a7 (Отредактировал код)


if __name__ == "__main__":
    try:
        print(main())
    except Exception as e:
        print(f"Произошла ошибка: {e}")
