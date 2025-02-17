import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


API_VERSION = "5.131"
BASE_URL = "https://api.vk.com/method"


def is_short_link(token: str, url: str) -> bool:
    parsed_url = urlparse(url)
    if parsed_url.netloc.lower() != "vk.cc":
        return False

    key = parsed_url.path.lstrip('/')
    params = {
        "access_token": token,
        "v": API_VERSION,
        "key": key,
        "interval": "forever"
    }

    response = requests.get(f"{BASE_URL}/utils.getLinkStats", params=params)
    response.raise_for_status()
    response_json = response.json()
    
    if "error" in response_json:
        raise Exception(f"Ошибка API VK: {response_json['error'].get('error_msg', 'Неизвестная ошибка')}")

    return response_json.get("response", {})


def count_clicks(link_stats: dict) -> int:
    if not link_stats or "stats" not in link_stats or not link_stats["stats"]:
        return 0
    return link_stats["stats"][0].get("count", 0)


def shorten_link(token: str, url: str) -> str:
    params = {"access_token": token, "v": API_VERSION, "url": url}

    response = requests.get(f"{BASE_URL}/utils.getShortLink", params=params)
    response.raise_for_status()
    response_json = response.json()

    if "error" in response_json:
        raise Exception(f"Ошибка API VK: {response_json['error'].get('error_msg', 'Неизвестная ошибка')}")

    return response_json.get("response", {}).get("short_url")


def main():
    try:
        load_dotenv()
        token = os.getenv("VK_TOKEN")
        if not token:
            raise Exception("Токен VK не найден")

        url = input("Введите ссылку: ").strip()

        link_stats = is_short_link(token, url)

        if link_stats:
            print(f"Количество переходов по ссылке: {count_clicks(link_stats)}")
        else:
            print(f"Сокращенная ссылка: {shorten_link(token, url)}")

    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
