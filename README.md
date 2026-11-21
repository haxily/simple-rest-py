# Project overview
Main focus of this project is to understand API design in Python(Django).

## Cloning
You can clone the repo with:
```bash
git clone https://github.com/haxily/simple-rest-py.git
```

## Requirements
Requirements for the project can be found in requirements.txt file.  
First create your python environment:

## On linux/mac
```bash
python3 -m venv .venv
source .venv/bin/activate
```
## On windows
```bash
py -m venv .venv
.venv\scripts\activate
```
Then install using:
```bash
pip install -r requirements.txt
```

## Running the Project
After you can navigate to the main project folder
```bash
cd djangorest
```
Then run the project with
## On Linux/mac
```bash
python3 manage.py runserver
```
## Windows
```bash
py manage.py runserver
```
On the terminal should be similar to:

<img width="909" height="191" alt="image" src="https://github.com/user-attachments/assets/7a37050d-725b-4e38-8277-c1ee8e4f7c47" />

Open the link in the terminal to localhost

## Create
In the browser open url
```url
http://localhost:{port}/api/users/create
```
Send a POST request with a JSON body for example:
```json
{
"name": "Peter",
"age": 25
}
```
## GET
You can get all users using:
```url
http://localhost:{port}/api/users
```
Or a specific user with their id added in the url:
```url
http://localhost:{port}/api/users/1
```
## Update
To update a user open the url:
```url
http://localhost:{port}/api/users/1
```
and send a PUT request with JSON body for example:
```json
{
"name": "Bob",
"age": 30
}
```
## Delete
To delete a user open the url:
```url
http://localhost:{port}/api/users/1
```
and send a DELETE request.
