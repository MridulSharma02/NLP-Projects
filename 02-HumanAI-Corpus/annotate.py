import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

print("Loading corpus...")
df = pd.read_csv("corpus_raw.csv")
df = df.dropna(subset=["text"])

def get_sentence_count(text):
    return len(nltk.sent_tokenize(str(text)))

def get_word_count(text):
    return len(nltk.word_tokenize(str(text)))

def get_avg_word_length(text):
    words = nltk.word_tokenize(str(text))
    if len(words) == 0:
        return 0
    return round(sum(len(w) for w in words) / len(words), 2)

def get_pos_tags(text):
    words = nltk.word_tokenize(str(text))
    tags = nltk.pos_tag(words)
    return str(tags[:5])

print("Annotating...")
df["sentence_count"] = df["text"].apply(get_sentence_count)
df["word_count"] = df["text"].apply(get_word_count)
df["avg_word_length"] = df["text"].apply(get_avg_word_length)
df["pos_tags_sample"] = df["text"].apply(get_pos_tags)

df.to_csv("corpus_annotated.csv", index=False)
print(f"Done! Saved annotated corpus to corpus_annotated.csv")