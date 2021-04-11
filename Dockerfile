FROM python:3.9-buster

RUN pip install pipenv

COPY . .
RUN pipenv install --system --dev

CMD python run.py