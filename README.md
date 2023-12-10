# k(ey-)v(alue-)v(ault)

Simple key/value storage server that saves data in files on disk.

## PUT

Write data to the server with `PUT`:

```
curl http://localhost:8000/path/to/my/file/test_2 -XPUT -d 'Super C0ntent!' -i
HTTP/1.1 200 OK
date: Sun, 10 Dec 2023 20:08:07 GMT
server: uvicorn
content-length: 51
content-type: application/json

{"created":false,"size":20,"size_human":"20 Bytes"}
```

from a file:

```
curl -s -X PUT --upload-file picture.png http://localhost:8000/path/to/my/file/picture.png -i
HTTP/1.1 100 Continue

HTTP/1.1 200 OK
date: Sun, 10 Dec 2023 20:05:20 GMT
server: uvicorn
content-length: 53
content-type: application/json

{"created":true,"size":5492528,"size_human":"5.5 MB"}
```

## GET data

Data can be retrieved with `metadata` (default), with `metadata` and `base64` encoded or as `plain` data:

```
curl http://localhost:8000/path/to/my/file/test_2 -i
HTTP/1.1 200 OK
date: Sun, 10 Dec 2023 20:08:30 GMT
server: uvicorn
content-length: 103
content-type: application/json

{"size":20,"size_human":"20 Bytes","timestamp":"2023-12-10T20:08:08.245010","content":"Super C0ntent!"}
```

```
curl http://localhost:8000/path/to/my/file/test_2?b64=true -i
HTTP/1.1 200 OK
date: Sun, 10 Dec 2023 20:08:47 GMT
server: uvicorn
content-length: 109
content-type: application/json

{"size":20,"size_human":"20 Bytes","timestamp":"2023-12-10T20:08:08.245010","content":"U3VwZXIgQzBudGVudCE="}
```

```
curl http://localhost:8000/path/to/my/file/test_2?plain=true -i
HTTP/1.1 200 OK
date: Sun, 10 Dec 2023 20:09:06 GMT
server: uvicorn
content-length: 14
content-type: text/plain; charset=utf-8

Super C0ntent!
```

## Development

Create a virtualenv and install all requirements

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run dev server:

```
uvicorn main:app --reload
```

