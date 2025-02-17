import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


API_VERSION = "5.131"
BASE_URL = "https://api.vk.com/method"


def api_request(method: str, params: dict) -> dict:
    api_url = f"{BASE_URL}/{method}"
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()

    if "error" in response_data:
        error_msg = response_data["error"].get("error_msg", "Неизвестная ошибка")
        raise Exception(f"Ошибка API VK: {error_msg}")

    return response_data


def is_shortened_link(token: str, url: str) -> bool:
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

    response_data = api_request("utils.getLinkStats", params)
    return "response" in response_data


def get_click_count(token: str, url: str) -> int:
    parsed_url = urlparse(url)
    key = parsed_url.path.lstrip('/')

    params = {"access_token": token, "v": API_VERSION, "key": key, "interval": "forever"}

    click_stats_data = api_request("utils.getLinkStats", params)

    stats = click_stats_data.get("response", {}).get("stats", [])
    return stats[0].get("count", 0) if stats else 0


def get_short_link(token: str, url: str) -> str:
    params = {"access_token": token, "v": API_VERSION, "url": url}

    short_link_data = api_request("utils.getShortLink", params)
    return short_link_data.get("response", {}).get("short_url")


def main():
    try:
        load_dotenv()
        token = os.getenv("VK_TOKEN")
        if not token:
            raise Exception("Токен VK не найден")

        url = input("Введите ссылку: ").strip()

        if is_shortened_link(token, url):
            print(f"Количество переходов по ссылке: {get_click_count(token, url)}")
        else:
            print(f"Сокращенная ссылка: {get_short_link(token, url)}")

    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
