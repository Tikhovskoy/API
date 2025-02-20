import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse

API_VERSION = "5.131"
BASE_URL = "https://api.vk.com/method"


class APIError(Exception):
    """Исключение для ошибок API."""
    pass


def is_shorten_link(token: str, url: str):
    parsed_url = urlparse(url)

    if parsed_url.netloc.lower() != "vk.cc":
        return False

    key = parsed_url.path.lstrip('/')
    api_url = f"{BASE_URL}/utils.getLinkStats"
    params = {
        "access_token": token,
        "v": API_VERSION,
        "key": key,
        "interval": "forever"
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    response_data = response.json()

    return "error" not in response_data and "response" in response_data


def shorten_link(token: str, url: str) -> str:
    api_url = f"{BASE_URL}/utils.getShortLink"
    params = {"access_token": token, "v": API_VERSION, "url": url}

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    shorten_response_data = response.json()

    if "response" in shorten_response_data:
        return shorten_response_data["response"]["short_url"]

    error_msg = shorten_response_data.get("error", {}).get("error_msg", "Неизвестная ошибка")
    raise APIError(f"Ошибка API VK: {error_msg}")


def count_clicks(token: str, short_url: str) -> int:
    api_url = f"{BASE_URL}/utils.getLinkStats"
    parsed_url = urlparse(short_url)
    key = parsed_url.path.lstrip('/')

    params = {"access_token": token, "v": API_VERSION, "key": key, "interval": "forever"}
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    link_stats_data = response.json()

    response_data = link_stats_data.get("response")
    if response_data:
        stats = response_data.get("stats", [])
        return stats[0].get("count", 0) if stats else 0

    error_msg = link_stats_data.get("error", {}).get("error_msg", "Неизвестная ошибка")
    raise APIError(f"Ошибка API VK: {error_msg}")


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")
    if not token:
        raise APIError("Не найден VK_TOKEN в .env")

    parser = argparse.ArgumentParser(description="Работа с сокращенными ссылками VK")
    parser.add_argument("url", type=str, help="Ссылка для проверки или сокращения")
    args = parser.parse_args()

    url = args.url.strip()

    try:
        if is_shorten_link(token, url):
            clicks = count_clicks(token, url)
            print(f"Количество переходов по ссылке: {clicks}")
        else:
            shortened_url = shorten_link(token, url)
            print(f"Сокращенная ссылка: {shortened_url}")

    except APIError as e:
        print(f"Ошибка при запросе к API: {e}")


if __name__ == "__main__":
    main()
