
import requests
import json




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


def img_resize(img, w, h):
    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    return img


def json_write(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def file_read(filepath):
    file_append(filepath, '')
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    return text


def file_append(filepath, text):
    with open(filepath, 'a', encoding='utf-8') as f: 
        f.write(text)
