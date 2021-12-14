import pandas as pd
import pytest
import spacy

from tweet_in_love.preprocessor import PreProcessor, cols_in_df


@pytest.fixture
def dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "body": ["Hello World!", "Not Happy"],
            "label": ["happy", "sad"],
        }
    )


@pytest.fixture
def preprocessor(dataframe) -> PreProcessor:
    nlp = spacy.blank("en")
    prepr = PreProcessor(
        nlp=nlp, classes=dataframe.label, text_label="body", class_label="label"
    )
    return prepr


def test_cols_in_df(dataframe):
    cols_in_df(dataframe, cols=["body", "label"])


def test_cols_in_empty_df():
    dataframe = pd.DataFrame({"body": [], "label": []})
    cols_in_df(dataframe, cols=["body", "label"])


def test_cols_not_in_df():
    dataframe = pd.DataFrame({})
    with pytest.raises(AttributeError):
        cols_in_df(dataframe, cols=["body", "label"])


def test_df_to_tuple(dataframe, preprocessor):
    tups = preprocessor.df_to_tuple(dataframe)
    assert tups == [("Hello World!", "happy"), ("Not Happy", "sad")]


def test_df_to_tuple_no_cols(dataframe, preprocessor):
    preprocessor.text_label = "typoooo"
    with pytest.raises(AttributeError):
        preprocessor.df_to_tuple(dataframe)


def test_df_to_tuple_empy(dataframe, preprocessor):
    dataframe.drop(dataframe.index, inplace=True)
    tups = preprocessor.df_to_tuple(dataframe)
    assert tups == []


def test_tuple_to_doc(dataframe, preprocessor):
    preprocessor.classes = set(("happy", "sad", "other"))
    tups = preprocessor.df_to_tuple(dataframe)
    docs = preprocessor.tuple_to_doc(tuples=tups)

    assert len(docs) == len(tups)
    assert docs[0].cats == {"happy": 1, "sad": 0, "other": 0}


def test_tuple_to_doc_class_not_in_set(dataframe, preprocessor):
    preprocessor.classes = set(("happy", "other"))
    tups = preprocessor.df_to_tuple(dataframe)
    with pytest.raises(AttributeError):
        docs = preprocessor.tuple_to_doc(tuples=tups)


def test_tuple_to_doc_class_not_unique(dataframe):
    nlp = spacy.blank("en")
    preprocessor = PreProcessor(
        nlp=nlp,
        classes=["happy", "happy", "happy", "happy", "sad", "other"],
        text_label="body",
        class_label="label",
    )
    tups = preprocessor.df_to_tuple(dataframe)
    docs = preprocessor.tuple_to_doc(tuples=tups)

    assert len(docs) == len(tups)
    assert docs[0].cats == {"happy": 1, "sad": 0, "other": 0}


def test_tuple_to_doc_empty(preprocessor):
    tups = []
    docs = preprocessor.tuple_to_doc(tuples=tups)

    assert docs == []
