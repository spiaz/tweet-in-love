# tweet-in-love - tweet sentiment prediction AAS

A simple end-to-end sentiment-prediction project on english tweets.

## Table of Contents

- [tweet-in-love - tweet sentiment prediction AAS](#tweet-in-love---tweet-sentiment-prediction-aas)
  - [Table of Contents](#table-of-contents)
  - [General info](#general-info)
  - [Project structure](#project-structure)
  - [Technologies](#technologies)
  - [Installation](#installation)
  - [Serving API Documentation](#serving-api-documentation)

## General info

In this project we explore a dataset of English tweets.
The dataset is composed by tweets a tweets (text) and their associated sentiment (categories).

The repository contains:

- some data exploration
- data preprocessing
- training of few models
- deployment of the models with a REST API
- a Docker file to serve the model and reproduce the results
- a Makefile to facilitate your life if you want to install it locally and re-run the code on your env ;)

## Project structure

```text
├── app             <- Code to serve the models
│   └── ...
├── data
│   ├── raw         <- The original, immutable data dump.
│   ├── test        <- Test data for model validation.
│   └── train       <- Data sets for modeling.
│
├── notebooks       <- Jupyter notebooks. Naming convention is a number (for ordering).
│   └── ...            Contains notebooks for exploration, dataset generation and training.
│
├── models          <- Trained and serialized models
│   └── ...
│
├── tweet_in_love   <- Source code for use in this project.
│   └── ...
│
├── tests           <- Unit tests
│   └── ...
│
├── Makefile        <- Makefile with commands like `make install` or `make deploy`
│
├── poetry.lock     <- All requirements not explicitly defined
│
├── pyproject.toml  <- The requirements file for reproducing the environment
│
├── README.md
```

## Technologies

Project is based principally on the follownig technologies:

- Python (v.3.9.5)
- SpaCy (NLP)
- Pydantic (typing and input validation)
- FastAPI (serving)
- Docker (deployment)
- Poetry (env and dependencies management)

## Installation

To run this project with Docker:

1. build the image

```sh
❯ make docker_build
```

1. run the volume

```sh
❯ make docker_up
```

The app will be serving on [localhost:8080](http://127.0.0.1:8080/)

To install it locally on your physical machine:

1. Prerequirement (Optional)\
   To avoid conflicts, I'd suggest to activate a virtual environment.
   You can follow this instructions:
   1. install [pyenv](https://github.com/pyenv/pyenv).
   2. Install [poetry](https://python-poetry.org/).
   3. install the virtual env:

       ```sh
       ❯ pyenv install 3.9.5 # Install Python 3.9.5

       ❯ pyenv local 3.9.5  # Activate Python 3.9.5 for the current project

       ❯ poetry env use 3.9.5 # let poetry know to use that version of python
       ```

2. Installation
   - User (model serving only):

        ```sh
        ❯ make install
        ```

   - Development (to execute notebooks and install the development libs)

        ```sh
        ❯ make install_dev
        ```

The Makefile contains also other facilities for the developer:

```sh
❯ make help

black                format all code
clean                delete all files in .gitignore
docker_build         create docker volume
docker_down          Shut down docker volume
docker_up            run docker volume
generate_dot_env     Cenerate an example .env file
help                 this help message
install              install requirements
install_dev          install dev requirements
install_poetry       install virtual env
isort                sort all imports
lint                 run the static type checker and the linter
test                 run test and show coverage
up                   launch the app locally
```

## Serving API Documentation

To launch the server:

```sh
❯ poetry run main.py
```

or

```sh
❯ make up
```

Once the server is up, the entrypoints are

- [http://0.0.0.0:8080/predict_one](http://0.0.0.0:8080/predict_one) <- predict one single tweet
- [http://0.0.0.0:8080/predict_batch](http://0.0.0.0:8080/predict_batch) <- predict a batch of tweets

Please refer to the complete API documentation at:

- [http://0.0.0.0:8080/doc](http://0.0.0.0:8080/doc)
- [http://0.0.0.0:8080/redoc](http://0.0.0.0:8080/docs)
