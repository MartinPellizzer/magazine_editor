
import requests


def unsplash_image_get():
    with open('C:/api-keys/unsplash-api-key.txt', 'r') as f:
        ACCESS_KEY = f.read().strip()

    url = f'https://api.unsplash.com/photos/random?client_id={ACCESS_KEY}'
    url = f'https://api.unsplash.com/search/photos?page=1&query=travel&client_id={ACCESS_KEY}'
    response = requests.get(url)
    print(response)

    data = response.json()['results']
    random_image = random.choice(data)

    filename = 'picture.jpg'
    image_url = random_image['urls']['regular']
    image_response = requests.get(image_url, stream=True)
    if image_response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in image_response:
                f.write(chunk)

    print(image_url)
