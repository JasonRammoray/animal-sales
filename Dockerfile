FROM python:3.7
EXPOSE 5000
RUN pip3 install pipenv
COPY . /app
WORKDIR /app
RUN pipenv install --system --deploy --ignore-pipfile
RUN pipenv lock --requirements > requirements.txt
RUN pip3 install -r requirements.txt
#RUN FLASK_APP=app/main.py flask db init
RUN FLASK_APP=app/main.py flask db upgrade
ENTRYPOINT FLASK_APP=app/main.py flask run --host=0.0.0.0
