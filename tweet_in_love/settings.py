from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


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
        return self.model_folder / f"model_name_{self.tag}_{self.version:02d}"

    @property
    def model_cfg(self) -> Path:
        return self.model_folder / f"config_{self.tag}_{self.version:02d}.cfg"

    class Config:
        env_file = ".env"
