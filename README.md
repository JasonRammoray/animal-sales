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
    - `[TOKEN]` followed by the token options on each row below
    - `[LOGGING]` followed by the logging options on each row below. The section should specify these attributes:
        * `audit_http_requests` - a comma-separated list of HTTP verbs (in upper case) that shall be stored in the audit log 
        * `audit_log` - a path to the audit log
* If you don't have a SQLite database created, make sure to have one: ` FLASK_APP=app/main.py flask db init`
* Apply the database migrations: `FLASK_APP=app/main.py flask db upgrade`
* If you're using a JetBrains IDE, create a run configuration for the Flask app by specifying script path as `app/main.py`. Otherwise, run that from the terminal: `FLASK_APP=app/main.py flask run`.

## Registering an animal center
In order to create an animal center, send a POST request to `/register` with a similar-looking payload: 
```
{
    "login": "5-255 characters login",
    "password": "8-255 characters login with at least one capital letter, at least one digit, and at least one alphanumeric character",
    "address": "full address of 5-255 characters"
}
```
