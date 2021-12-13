import pandas as pd
import spacy
import pytest

from tweet_in_love.preprocess import df_to_tuple, tuple_to_doc


@pytest.fixture
def dataframe():
    return pd.DataFrame(
        {
            "body": ["Hello World!", "Not Happy"],
            "class": ["happy", "sad"],
        }
    )


def test_cols_in_df():
    dataframe = pd.DataFrame({})
    with pytest.raises(AttributeError):
        df_to_tuple(dataframe, text_label="body", class_label="class")


def test_df_to_tuple(dataframe):
    tups = df_to_tuple(dataframe, text_label="body", class_label="class")
    assert tups == [("Hello World!", "happy"), ("Not Happy", "sad")]


def test_df_to_tuple_no_cols(dataframe):
    with pytest.raises(AttributeError):
        df_to_tuple(dataframe, text_label="typoooo", class_label="class")


def test_df_to_tuple_empy(dataframe):
    dataframe.drop(dataframe.index, inplace=True)
    tups = df_to_tuple(dataframe, text_label="body", class_label="class")
    assert tups == []


def test_tuple_to_doc(dataframe):
    tups = df_to_tuple(dataframe, text_label="body", class_label="class")

    nlp = spacy.blank("en")
    docs = tuple_to_doc(nlp=nlp, tuples=tups, classes={"happy", "sad", "other"})

    assert len(docs) == len(tups)
    assert docs[0].cats == {"happy": 1, "sad": 0, "other": 0}


def test_tuple_to_doc_class_not_in_set(dataframe):
    tups = df_to_tuple(dataframe, text_label="body", class_label="class")

    nlp = spacy.blank("en")
    with pytest.raises(AttributeError):
        tuple_to_doc(nlp=nlp, tuples=tups, classes={"happy", "other"})


def test_tuple_to_doc_class_not_unique(dataframe):
    tups = df_to_tuple(dataframe, text_label="body", class_label="class")

    nlp = spacy.blank("en")
    docs = tuple_to_doc(
        nlp=nlp,
        tuples=tups,
        classes=["happy", "happy", "happy", "happy", "sad", "other"],
    )

    assert len(docs) == len(tups)
    assert docs[0].cats == {"happy": 1, "sad": 0, "other": 0}


def test_tuple_to_doc_empty():
    tups = []

    nlp = spacy.blank("en")
    docs = tuple_to_doc(nlp=nlp, tuples=tups, classes={"happy", "sad", "other"})

    assert docs == []
