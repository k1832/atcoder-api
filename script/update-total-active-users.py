"""Scrape AtCoder ranking page to get the total number of active users."""
import json
import os
import requests

from bs4 import BeautifulSoup

def main():
    """Scrape AtCoder ranking page to get the total number of active users."""
    rank_page_url = "https://atcoder.jp/ranking"
    algo_rank_page_url = f"{rank_page_url}?contestType=algo"
    response = requests.get(algo_rank_page_url, timeout=10)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    total_num_pages_element = soup.select_one("ul.pagination li:last-child a")
    try:
        total_num_pages = int(total_num_pages_element.text.strip())
    except (AttributeError, ValueError) as e:
        msg = f"Failed to get the page numbers in {algo_rank_page_url}"
        raise RuntimeError(msg) from e

    algo_rank_last_page_url = f"{algo_rank_page_url}&page={total_num_pages}"
    response = requests.get(algo_rank_last_page_url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    num_active_users_text = soup.select_one("table.table tr:last-child > td:first-child")
    try:
        num_active_users = int(num_active_users_text.text.strip())
    except (AttributeError, ValueError) as e:
        msg = f"Failed to get the number of active users in {algo_rank_last_page_url}"
        raise RuntimeError(msg) from e

    # GitHub Pages does not allow to specify the directory to deploy
    # except the "docs" directory
    # (root)
    #   - script
    #       - {this Python script}
    #   - docs
    #       - api
    #           - v1
    #               - {JSON file}
    script_dir_path = os.path.abspath(os.path.dirname(__file__))
    root_dir_path = os.path.dirname(script_dir_path)
    docs_dir_path = os.path.join(root_dir_path, "docs")
    api_dir_path = os.path.join(docs_dir_path, "api")
    api_v1_dir_path = os.path.join(api_dir_path, "v1")
    api_json_name = "total-active-users.json"

    with open(os.path.join(api_v1_dir_path, api_json_name), 'w', encoding='utf-8') as f:
        json.dump({"val": num_active_users}, f)
        f.write("\n")

if __name__ == "__main__":
    main()
