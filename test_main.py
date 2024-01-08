import random
import requests
import pytest

# Define the base URL of your server
BASE_URL = 'http://localhost:8000'

# define a random url path (to ensure clean uploads)
prefix = random.getrandbits(32)
BASE_URL += f'/{prefix}'

###
# Tests
###
def test_put_inline_data():
    url = BASE_URL + '/f1/test_2'
    data = 'Not Super Content!'

    response = requests.put(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"created": True, "size": 24, "size_human": "24 Bytes"}

def test_change_put_inline_data():
    url = BASE_URL + '/f1/test_2'
    data = 'Super Content!'

    response = requests.put(url, data=data)

    assert response.status_code == 200
    assert response.json() == {"created": False, "size": 20, "size_human": "20 Bytes"}

def test_put_inline_data_folder():
    url = BASE_URL + '/f1'
    data = 'FOLDER'

    response = requests.put(url, data=data)

    assert response.status_code == 409

def test_put_upload_file():
    url = BASE_URL + 'file.txt'
    files = {'file': ('file.txt', open('file.txt', 'rb'))}

    response = requests.put(url, files=files)

    assert response.status_code == 200
    assert response.json() == {"created": True, "size": 364, "size_human": "364 Bytes"}

def test_get_metadata():
    url = BASE_URL + '/f1/test_2'

    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['size'] == 20
    assert data['size_human'] == "20 Bytes"
    assert 'timestamp' in data
    assert 'content' in data

def test_get_metadata_base64():
    url = BASE_URL + '/f1/test_2?b64=true'

    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['size'] == 20
    assert data['size_human'] == "20 Bytes"
    assert 'timestamp' in data
    assert 'content' in data
    assert data['content'] == "U3VwZXIgQ29udGVudCE="

def test_get_plain_data():
    url = BASE_URL + '/f1/test_2?plain=true'

    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/plain; charset=utf-8'
    assert response.text == 'Super Content!'

def test_cors_headers_present():
    url = BASE_URL + '/f1/test_2?plain=true'

    response = requests.options(url)

    assert 'Access-Control-Allow-Origin' in response.headers
    assert 'Access-Control-Allow-Methods' in response.headers
    assert 'Access-Control-Allow-Headers' in response.headers
    assert 'Access-Control-Max-Age' in response.headers


if __name__ == '__main__':
    pytest.main()
