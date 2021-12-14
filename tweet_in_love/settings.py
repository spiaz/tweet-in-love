from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class GlobalSettings(BaseSettings):
    project_name: str
    raw_csv_file: str
    tag: Optional[str] = None
    raw_folder: Path = Path("data/raw")
    train_folder: Path = Path("data/train")
    test_folder: Path = Path("data/test")

    @property
    def raw_csv_path(self) -> Path:
        return self.raw_folder / self.raw_csv_file

    def _tagged(self, name: str, ext: str) -> str:
        file = name
        if self.tag:
            file += f"_{self.tag}"
        file += f".{ext}"
        return file

    @property
    def train_csv_path(self) -> Path:
        return self.train_folder / self._tagged("train", "csv")

    @property
    def train_spacy_path(self) -> Path:
        return self.train_folder / self._tagged("train", "spacy")

    @property
    def test_csv_path(self) -> Path:
        return self.test_folder / self._tagged("test", "csv")

    @property
    def test_spacy_path(self) -> Path:
        return self.test_folder / self._tagged("test", "spacy")

    class Config:
        env_file = ".env"


class ModelSettings(BaseSettings):
    tag: str
    version: int
    model_folder: Path = Path("models")

    @property
    def model_path(self) -> Path:
        return self.model_folder / f"model_{self.tag}_{self.version:02d}"

    @property
    def model_best(self) -> Path:
        return self.model_path / "model-best"

    @property
    def model_cfg(self) -> Path:
        return self.model_path / f"{self.tag}_{self.version:02d}.cfg"

    @property
    def model_full_cfg(self) -> Path:
        return self.model_path / "config.cfg"

    def create_folder(self):
        self.model_path.mkdir(parents=True, exist_ok=True)

    class Config:
        env_file = ".env"


class DeployedModelSettings(ModelSettings):
    tag: str = Field(env="DEPLOYED_MODEL_TAG")
    version: int = Field(env="DEPLOYED_MODEL_VERSION")
