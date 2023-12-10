# KV-Vault

KV-Vault is a lightweight key/value storage server that efficiently stores data as files on disk. It is built on the FastAPI framework and provides a simple yet powerful interface for managing data with support for PUT and GET operations. You can retrieve data with metadata, in base64-encoded format, or as plain data.

## Features

- Store and retrieve data as key/value pairs.
- Efficiently manage data on disk.
- Retrieve data with optional metadata, base64 encoding, or as plain data.




## Running the Server

You can start KV-Vault server with `uvicorn`, specify the port and host as follow:

```bash
export DATA_PATH=/opt/kv/data/
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

- `--host`: Specifies the host where the server should listen. In this example, we use '0.0.0.0' to allow connections from any IP address. You can replace it with a specific IP address if needed.
- `--port`: Specifies the port number on which the server should listen. In this example, we use port 8000, but you can choose a different port if necessary.
- `--workers`: Specifies the number of worker processes to run. Adjust the value based on your server's hardware and performance requirements.

Once the server is running, it will be accessible at the specified host and port (e.g., http://localhost:8000).

KV-Vault stores data as files on disk. You can specify the path where data should be stored using the `DATA_PATH` environment variable. By default, it stores data in a directory named `data/` in the current working directory.

## PUT Data

Write data to the server using PUT requests. You can either provide the data inline or upload a file.
The `created` key will indicate if a key was created (did not exist before) or overwritten.

### Inline Data

```bash
curl http://localhost:8000/path/to/my/folder/test_2 -XPUT -d 'Super Content!'
```

Response:

```json
{
  "created": false,
  "size": 20,
  "size_human": "20 Bytes"
}
```

### Upload a File

```bash
curl -s -X PUT --upload-file file.txt http://localhost:8000/path/to/my/folder/file.txt
```

Response:

```json
{
  "created": true,
  "size": 364,
  "size_human": "364 Bytes"
}
```

## Search

Given a path (without a key/file) will return a list of all keys:

```bash
curl http://localhost:8000/path/to/my/folder
```

Response:

```json
{
  "keys": [
    "picture.png",
    "test_2"
  ]
}
```

If a `prefix` query parameter is present in the request the `keys` list will be filtered with the prefix. In the following example only `keys` that start with `test_` will be returned.

```bash
curl http://localhost:8000/path/to/my/folder?prefix=test_
```

Response:

```json
{
  "keys": [
    "test_2"
  ]
}
```

## GET Data

Retrieve data from the server with optional parameters for different output formats.

### Metadata (Default)
Retrieve data with metadata.

```bash
curl http://localhost:8000/path/to/my/folder/test_2
```

Response:

```json
{
  "size": 20,
  "size_human": "20 Bytes",
  "timestamp": "2023-12-10T20:08:08.245010",
  "content": "Super Content!"
}
```

### Metadata and Base64 Encoding
Retrieve data with metadata and base64 encoding.

```bash
curl http://localhost:8000/path/to/my/folder/test_2?b64=true
```

Response:

```json
{
  "size": 20,
  "size_human": "20 Bytes",
  "timestamp": "2023-12-10T20:08:08.245010",
  "content": "U3VwZXIgQ29udGVudCE="
}
```

### Plain Data
Retrieve data as plain text.

```bash
curl http://localhost:8000/path/to/my/folder/file.txt?plain=true
```

Response:

```plaintext
  Upload Test file
     *******
   **       **
 **   O   O   **
 *               *
 **  \     /  **
   **  ****  **
     *******
```

## Development

To set up a development environment:

Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
````

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Run the development server with automatic reload:
```bash
uvicorn main:app --reload
```

# Contribution

For any issues or questions, please open an issue.

Enjoy using KV-Vault!