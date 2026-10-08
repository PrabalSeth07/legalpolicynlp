from legalease.preprocessing import normalize_whitespace, preprocess_document, split_sentences, tokenize


def test_normalize_whitespace_removes_extra_spaces():
    assert normalize_whitespace("Hello    world\n\n\nAgain") == "Hello world\n\nAgain"


def test_split_sentences_basic():
    assert split_sentences("One sentence. Another sentence!") == ["One sentence.", "Another sentence!"]


def test_tokenize_counts_words():
    assert tokenize("Tenant's rights and duties.") == ["Tenant's", "rights", "and", "duties"]


def test_preprocess_document_stats():
    processed = preprocess_document("This is a policy. Read it carefully.")
    assert processed.stats.word_count == 7
    assert processed.stats.sentence_count == 2
