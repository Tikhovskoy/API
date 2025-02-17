import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def main():
    try:
        load_dotenv()
        token = os.getenv("VK_TOKEN")
        if not token:
            raise Exception("Ошибка: не найден VK_TOKEN в .env")

        url = input("Введите ссылку: ").strip()

        parsed_url = urlparse(url)
        if parsed_url.netloc.lower() != "vk.cc":
            is_shortened = False
        else:
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
            is_shortened = "response" in response.json()

        if is_shortened:
            api_url = "https://api.vk.com/method/utils.getLinkStats"
            parsed_url = urlparse(url)
            key = parsed_url.path.lstrip('/')

            params = {"access_token": token, "v": "5.131", "key": key, "interval": "forever"}

            response = requests.get(api_url, params=params)
            response.raise_for_status()
            click_stats_data = response.json()

            if "error" in click_stats_data:
                raise Exception(click_stats_data["error"].get("error_msg", "Неизвестная ошибка"))

            count = click_stats_data.get("response", {}).get("stats", [{}])[0].get("count", 0)
            print(f"Количество переходов по ссылке: {count}")
        else:
            api_url = "https://api.vk.com/method/utils.getShortLink"
            params = {"access_token": token, "v": "5.131", "url": url}

            response = requests.get(api_url, params=params)
            response.raise_for_status()
            short_link_data = response.json()

            if "error" in short_link_data:
                raise Exception(short_link_data["error"].get("error_msg", "Неизвестная ошибка"))

            print(f"Сокращенная ссылка: {short_link_data.get('response', {}).get('short_url')}")

    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
