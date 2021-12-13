FROM python:3.9.9

EXPOSE 8080
WORKDIR /code

# copy package definitions
COPY poetry.lock pyproject.toml ./

# install packages
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . ./
ENV PYTHONPATH app
ENV PYTHONPATH tweet_in_love
ENTRYPOINT ["python", "app/main.py"]