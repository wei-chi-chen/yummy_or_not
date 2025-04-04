import requests
from bs4 import BeautifulSoup
from typing import List


def find_comments_of_the_place(name: str) -> List[str]:
    """
        Fetches comments (replies) from PTT Food board about a given food place.

        :param name: The name of the place (food shop) we want to find.
        :return: A list of comments found on the web.
    """

    url = f'https://www.ptt.cc/bbs/Food/search?q={name}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/134.0.0.0 Mobile Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        print(f"✅ Get the page successfully ...")
    except requests.RequestException as e:
        print(f"❌ 無法獲取頁面: {e}")
        return []

    print(f"Fetching Comments for {name} ...")
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='r-ent')

    comments_list = []

    for article in articles:
        title_element = article.find("div", class_="title")
        if not title_element or not title_element.a:
            continue  # Skip if there's no valid article

        post_url = f"https://www.ptt.cc{title_element.a['href']}"

        try:
            post_response = requests.get(post_url, headers=headers)
            post_response.raise_for_status()
        except requests.RequestException:
            continue  # Skip this article if we fail to fetch comments

        post_soup = BeautifulSoup(post_response.text, 'html.parser')
        pushes = post_soup.find_all('div', class_='push')

        for push in pushes:
            push_content = push.find('span', class_='f3 push-content')
            if push_content:
                comment_text = push_content.text.strip()[1:]  # Remove leading colon ":"
                comments_list.append(comment_text)

    print("\n".join(comments_list) if comments_list else "⚠️ 沒有找到評論")
    return comments_list


# Example usage
if __name__ == "__main__":
    place_name = "海底撈"
    comments = find_comments_of_the_place(place_name)
    print("\n".join(comments) + f"\n\nnums of cmt: {len(comments)}" if comments else "⚠️ 沒有找到評論")
