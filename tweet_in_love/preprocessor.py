"""
Utilities to prepare the data for training
"""

from pathlib import Path
from typing import List, Optional, Sequence, Set, Tuple

import pandas as pd
from pydantic import BaseModel, validator
from sklearn.preprocessing import LabelBinarizer
from spacy.language import Language
from spacy.tokens import Doc, DocBin

from .settings import GlobalSettings


def cols_in_df(df: pd.DataFrame, cols: List[str]) -> None:
    """
    Verify that some columns are available in a DataFrame

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to check
    cols : List[str]
        Cols that should be present

    Raises
    ------
    AttributeError
        When column is not present
    """
    not_available = set(cols) - set(df.columns)
    if not_available:
        raise AttributeError(
            f"`{not_available}` not in DataFrame.\nAvailable columns: {df.columns}"
        )


class PreProcessor(BaseModel):
    """
    Prepare data in a format that can be ingested by a model
    """

    nlp: Language
    classes: Set[str]
    text_label: str = "content"
    class_label: str = "sentiment"

    @validator("classes", pre=True)
    @classmethod
    def make_unique(cls, seq: Sequence) -> Set:
        return set(seq)

    def df_to_tuple(
        self,
        df: pd.DataFrame,
    ) -> List[Tuple[str, str]]:
        """
        Transform a DataFrame to a sequence of texts and classes

        Parameters
        ----------
        df : pd.DataFrame
            Input data containing texts and classes
        text_label : str, optional
            Label for the column containing the texts, by default "content"
        class_label : str, optional
            Label for the columns containing the classes, by default "sentiment"

        Returns
        -------
        List[Tuple[str, str]]
            A list of tuples, each composed as: (text, class)
        """
        cols_in_df(df, [self.text_label, self.class_label])
        return list(zip(df[self.text_label], df[self.class_label]))

    def tuple_to_doc(self, tuples: List[Tuple[str, str]]) -> List[Doc]:
        """
        From a sequence of texts and labels, generates a list of SpaCy's docs.

        Internally, it runs the pipeline configured in self.nlp.

        Parameters
        ----------
        nlp : Language
            Spacy's language model to use
        tuples : List[Tuple[str, str]]
            A list of text and classes. See `df_to_tuple` function
        classes : Iterable[str]
            A sequence of unique classes.
            It should contains at least all the values appearing in tuples.
            Repeated values are ignored.

        Returns
        -------
        List[Doc]
            A list of SpaCy's Docs

        Raises
        ------
        AttributeError
            When an undefined class is found
        """

        # check that `classes` contain all unique values found in tuples
        not_defined = set([c for _, c in tuples]) - self.classes
        if not_defined:
            raise AttributeError(f"Some classes are not defined: {not_defined}")

        labels_dict = {label: 0 for label in self.classes}
        docs = []

        for doc, label in self.nlp.pipe(tuples, as_tuples=True):
            # add labels to document
            doc.cats = {**labels_dict}
            doc.cats[label] = 1

            docs.append(doc)
        return docs

    def df_to_doc(self, df: pd.DataFrame) -> List[Doc]:
        """
        Transform a DataFrame into a list of Docs

        Parameters
        ----------
        df : pd.DataFrame
            A dataframe of strings and labels

        Returns
        -------
        List[Doc]
            A list of Docs
        """
        tuples = self.df_to_tuple(df)
        return self.tuple_to_doc(tuples)

    def save_docs(
        self,
        train_docs: List[Doc],
        test_docs: List[Doc],
        tag: Optional[str],
        settings: Optional[GlobalSettings] = None,
    ) -> Tuple[Path, Path]:
        """
        Save a list of Docs to disk as DocBin format.

        Docbin is the binary format required by Spacy v3 models.

        Parameters
        ----------
        train_docs : List[Doc]
            List of Docs to be saved as train dataset
        test_docs : List[Doc]
            List of Docs to be saved as test dataset
        tag : Optional[str]
            A short description (tag)
        settings : Optional[GlobalSettings], optional
            Configuration class used to establish where the data should be saved.
            This function enforces a coherent naming convention for the data.

            By default None, in which case the configuration is read from the environment.

        Returns
        -------
        Tuple[Path, Path]
            Path where the data have been saved
        """
        if settings is None:
            settings = GlobalSettings()
        settings.tag = tag

        # Convert data to binary format required for training
        train_docbin = DocBin(docs=train_docs)
        test_docbin = DocBin(docs=test_docs)

        # save to disk
        train_path = settings.train_spacy_path
        test_path = settings.test_spacy_path

        train_docbin.to_disk(train_path)
        test_docbin.to_disk(test_path)

        return train_path, test_path

    class Config:
        # required to allow Spacy's Language model
        arbitrary_types_allowed = True
