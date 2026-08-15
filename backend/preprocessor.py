import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def preprocess(sentence: str) -> tuple[str, list[str]]:
    sentence = sentence.lower()
    tokens = word_tokenize(sentence)
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens), tokens


def get_token_overlap(tokens_a: list[str], tokens_b: list[str]) -> tuple[float, list[str]]:
    set_a, set_b = set(tokens_a), set(tokens_b)
    common = set_a.intersection(set_b)
    if not set_a and not set_b:
        return 0.0, []
    overlap = len(common) / max(len(set_a), len(set_b))
    return round(overlap, 4), list(common)


def get_antonyms(word: str) -> list[str]:
    antonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            for antonym in lemma.antonyms():
                antonyms.append(antonym.name())
    return list(set(antonyms))


def find_antonym_pairs(tokens_a: list[str], tokens_b: list[str]) -> list[str]:
    pairs = []
    for token_a in tokens_a:
        antonyms_of_a = get_antonyms(token_a)
        for token_b in tokens_b:
            if token_b in antonyms_of_a:
                pairs.append(f"{token_a} <-> {token_b}")
    return pairs


def get_wordnet_similarity(tokens_a: list[str], tokens_b: list[str]) -> float:
    scores = []
    for word_a in tokens_a:
        synsets_a = wordnet.synsets(word_a)
        if not synsets_a:
            continue
        for word_b in tokens_b:
            synsets_b = wordnet.synsets(word_b)
            if not synsets_b:
                continue
            sim = synsets_a[0].path_similarity(synsets_b[0])
            if sim is not None:
                scores.append(sim)
    return round(sum(scores) / len(scores), 4) if scores else 0.0


def analyze(sentence_a: str, sentence_b: str) -> dict:
    cleaned_a, tokens_a = preprocess(sentence_a)
    cleaned_b, tokens_b = preprocess(sentence_b)
    overlap, common_tokens = get_token_overlap(tokens_a, tokens_b)
    antonyms = find_antonym_pairs(tokens_a, tokens_b)
    wn_similarity = get_wordnet_similarity(tokens_a, tokens_b)
    return {
        "cleaned_a": cleaned_a,
        "cleaned_b": cleaned_b,
        "token_overlap": overlap,
        "common_tokens": common_tokens,
        "antonyms_found": antonyms,
        "wordnet_similarity": wn_similarity,
        "tokens_a": tokens_a,
        "tokens_b": tokens_b,
    }
