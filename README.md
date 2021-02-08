## Animals sales clinic
This is a demo application prepared as part of the final project in the "Python from scratch" learning path.

## Installation instructions
* Make sure you have Python 3.7 installed. If that isn't the case, you can use [pyenv](https://github.com/pyenv/pyenv).
* Install [pipenv](https://pypi.org/project/pipenv/)
* Install the packages:
    - `pipenv shell`
    - `pipenv install`
* Create a `config.ini` file in the root directory with the following structure:
    - `[DATABASE]` followed by the database options on each row below. The section should specify these attributes:
        * `uri` - a database uri
    - `[COMMON]` followed by the common app options. The section should specify these attributes:
        * `secret_key` - the app secret key. You generate one as follows:
            ```
            import secrets
            print(secrets.token_hex(64))
            ```
    - `[TOKEN]` followed by the token options on each row below
        * `expiration_time` - an expiration time in seconds
    - `[LOGGING]` followed by the logging options on each row below. The section should specify these attributes:
        * `audit_http_requests` - a comma-separated list of HTTP verbs (in upper case) that shall be stored in the audit log 
        * `audit_log` - a path to the audit log relative to the project folder
* Initialize a database: ` FLASK_APP=app/main.py flask db init`
* Create the database migrations: `FLASK_APP=app/main.py flask db migrate`
* Apply the database migrations: `FLASK_APP=app/main.py flask db upgrade`
* If you're using a JetBrains IDE, create a run configuration for the Flask app by specifying script path as `app/main.py`. Otherwise, run that from the terminal: `FLASK_APP=app/main.py flask run`.

## App shell
In order to activate the app shell mode run: `FLASK_APP=app/main.py flask shell`. Make sure you've migrated and have upgraded your database first.

## Registering an animal center
In order to create an animal center, send a POST request to `/register` with a similar-looking payload: 
```
{
    "login": "5-255 characters login",
    "password": "8-255 characters login with at least one capital letter, at least one digit, and at least one alphanumeric character",
    "address": "full address of 5-255 characters"
}
```
Example:
`curl -X POST -H 'Content-type: application/json' -d '{"login": "x_lab", "password": "v0rYS@cre!", "address": "123 Lab str., 20A"}' localhost:5000/register`

## Getting a token
In order to obtain a token for a particular animal center, send a POST request to `/login` with a similar-looking payload:
```
{
    "login": "5-255 characters login",
    "password": "8-255 characters password"
}
```
Example:
`curl -X POST -H 'Content-type: application/json' -d '{"login": "x_lab", "password": "v0rYS@cre!"}' localhost:5000/login`

## Running tests
Run `pytest -v` in a terminal.
