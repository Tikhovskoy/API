import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


API_VERSION = "5.131"
BASE_URL = "https://api.vk.com/method"


def is_short_link(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.netloc.lower() == "vk.cc" and bool(parsed_url.path.lstrip('/'))  


def get_click_stats(token: str, key: str) -> dict:
    params = {
        "access_token": token,
        "v": API_VERSION,
        "key": key,
        "interval": "forever"
    }

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

        url = input("Введите ссылку: ").strip()

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


if __name__ == "__main__":
    main()
