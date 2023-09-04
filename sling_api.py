import requests

#  photos {
# 'description': 'xxx',
# 'id': 11,
# 'url': 'https://api.slingacademy.com/public/sample-photos/11.jpeg',
# 'title': 'Commercial kitchen',
# 'user': 29
# }


def get_image_urls(offset: int = 0, limit: int = 20):
    res = requests.get(
        f"https://api.slingacademy.com/v1/sample-data/photos?offset={offset}&limit={limit}"
    )
    photos = res.json()["photos"]

    urls = [photo["url"] for photo in photos]

    return urls
