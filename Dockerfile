FROM python:3.9.5

ENV PYTHONUNBUFFERED 1

EXPOSE 8080
WORKDIR /code

COPY Makefile .python-version ./

RUN make install_poetry

# copy package definitions
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.in-project true
RUN make install

COPY . ./

ENTRYPOINT ["make", "up"]