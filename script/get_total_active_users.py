import requests, os, json
from bs4 import BeautifulSoup

def main():
    ranking_base = "https://atcoder.jp/ranking"
    algo_ranking_url = f"{ranking_base}?contestType=algo"
    response = requests.get(algo_ranking_url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    total_num_pages_element = soup.select_one("ul.pagination li:last-child a")
    try:
        total_num_pages = int(total_num_pages_element.text.strip())
    except (AttributeError, ValueError) as e:
        msg = f"Failed to get the page numbers in {algo_ranking_url}"
        raise RuntimeError(msg)

    algo_last_page_url = f"{algo_ranking_url}&page={total_num_pages}"
    response = requests.get(algo_last_page_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    num_active_users_text = soup.select_one("table.table tr:last-child > td:first-child")
    try:
        num_active_users = int(num_active_users_text.text.strip())
    except (AttributeError, ValueError) as e:
        msg = f"Failed to get the number of active users in {algo_last_page_url}"
        raise RuntimeError(msg)

    # GitHub Pages does not allow to specify the directory to deploy
    # except the "docs" directory
    """
    - docs
        - script
            - {this file}
    - api
        - v1
            - {json file}
    """
    script_dir_path = os.path.abspath(os.path.dirname(__file__))
    root_dir_path = os.path.dirname(script_dir_path)
    docs_dir_path = os.path.join(root_dir_path, "docs")
    api_dir_path = os.path.join(docs_dir_path, "api")
    api_v1_dir_path = os.path.join(api_dir_path, "v1")
    api_json_name = "total-active-users.json"

    with open(os.path.join(api_v1_dir_path, api_json_name), 'w') as f:
        json.dump({"val": num_active_users}, f)

if __name__ == "__main__":
    main()
