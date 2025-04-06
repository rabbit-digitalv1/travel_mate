import os
import csv
import json
import logging
import requests
from urllib.parse import urlparse
from pygments import formatters, highlight, lexers
from enum import Enum
import logging
import random
import time
import traceback
from typing import Callable


def retry_with_backoff(
    retries: int = 3,
    backoff_factor: float = 0.5,
    allowed_exceptions: tuple = (Exception,),
):
    """
    Decorator to retry a function with exponential backoff in case of failure.
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    wait = backoff_factor * (2 ** attempt)
                    logging.warning(
                        f"[Retry Attempt {attempt + 1}/{retries}] {e}. Retrying in {wait:.2f} seconds."
                    )
                    time.sleep(wait)
            logging.error("Maximum retry attempts reached. Traceback:")
            traceback.print_exc()
            return None

        return wrapper

    return decorator



logging.basicConfig(
    level=logging.INFO, filename="YARS.log", format="%(asctime)s - %(message)s"
)


Post_Type = Enum("Post_Type", ["BEST", "HOT", "TOP", "NEW", "RISING", "USERHOT", "USERTOP"])

def display_results(results, title):

    try:
        print(f"\n{'-'*20} {title} {'-'*20}")

        if isinstance(results, list):
            for item in results:
                if isinstance(item, dict):
                    formatted_json = json.dumps(item, sort_keys=True, indent=4)
                    colorful_json = highlight(
                        formatted_json,
                        lexers.JsonLexer(),
                        formatters.TerminalFormatter(),
                    )
                    print(colorful_json)
                else:
                    print(item)
        elif isinstance(results, dict):
            formatted_json = json.dumps(results, sort_keys=True, indent=4)
            colorful_json = highlight(
                formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter()
            )
            print(colorful_json)
        else:
            logging.warning(
                "No results to display: expected a list or dictionary, got %S",
                type(results),
            )
            print("No results to display.")

    except Exception as e:
        logging.error(f"Error displaying results: {e}")
        print("Error displaying results.")


def download_image(image_url, output_folder="images", session=None):

    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.basename(urlparse(image_url).path)
    filepath = os.path.join(output_folder, filename)

    if session is None:
        session = requests.Session()

    try:
        response = session.get(image_url, stream=True)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        logging.info("Downloaded: %s", filepath)
        return filepath
    except requests.RequestException as e:
        logging.error("Failed to download %s: %s", image_url, e)
        return None
    except Exception as e:
        logging.error("An error occurred while saving the image: %s", e)
        return None


def export_to_json(data, filename="output.json"):
    try:
        # print(data)
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully exported to {filename}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")


def export_to_csv(data, filename="output.csv"):
    try:
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"Data successfully exported to {filename}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")