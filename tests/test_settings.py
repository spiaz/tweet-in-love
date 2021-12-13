from pathlib import Path
from dotenv import load_dotenv

import pytest
from tweet_in_love.settings import GlobalSettings

ENV = {
    "project_name": "a_project",
    "model_path": "a/model/here.mdl",
    "raw_csv_file": "a_file.csv",
    "raw_folder": "a/folder",
}


@pytest.fixture()
def dotenv(tmpdir) -> str:
    path = tmpdir / ".env"
    env_settings = f"""
PROJECT_NAME={ENV["project_name"]}
MODEL_PATH={ENV["model_path"]}
RAW_CSV_FILE={ENV["raw_csv_file"]}
RAW_FOLDER={ENV["raw_folder"]}
"""
    path.write(env_settings)
    return str(path)


def test_import_env(dotenv: str):
    load_dotenv(dotenv, override=True)
    settings = GlobalSettings(_env_file=dotenv)
    assert settings.project_name == ENV["project_name"]
    raw_csv_path = Path(ENV["raw_folder"]) / ENV["raw_csv_file"]
    assert settings.raw_csv_path == raw_csv_path
