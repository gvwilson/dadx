# start snippet imports
import math
import string
from collections import Counter

import polars as pl
# end snippet imports


# start snippet tokenize
DESCRIPTIONS = {
    "d1": "flood water basement",
    "d2": "storm downed power line",
    "d3": "flood road closed",
    "d4": "storm power outage reported",
    "d5": "flood water rising",
}


def tokenize(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.split()


tokenized = {doc_id: tokenize(text) for doc_id, text in DESCRIPTIONS.items()}
for doc_id, toks in tokenized.items():
    print(doc_id, toks)
# end snippet tokenize


# start snippet term_frequency
def term_frequencies(tokens):
    counts = Counter(tokens)
    total = len(tokens)
    return {term: count / total for term, count in counts.items()}


for doc_id, toks in tokenized.items():
    tf = term_frequencies(toks)
    print(doc_id, {t: round(f, 3) for t, f in tf.items()})
# end snippet term_frequency


# start snippet document_frequency
def document_frequencies(docs):
    df = Counter()
    for toks in docs.values():
        for term in set(toks):
            df[term] += 1
    return df


doc_freq = document_frequencies(tokenized)
print(doc_freq)
# end snippet document_frequency


# start snippet idf_weights
n_docs = len(DESCRIPTIONS)


def idf_weights(df, n):
    return {term: math.log(n / count) for term, count in df.items()}


idf = idf_weights(doc_freq, n_docs)
print({t: round(w, 3) for t, w in idf.items()})
# end snippet idf_weights


# start snippet tfidf
def tfidf(tf, idf):
    return {term: freq * idf[term] for term, freq in tf.items()}


scores = {
    doc_id: tfidf(term_frequencies(toks), idf)
    for doc_id, toks in tokenized.items()
}
for doc_id, w in scores.items():
    print(doc_id, {t: round(x, 3) for t, x in w.items()})
# end snippet tfidf


# start snippet vectors
rows = []
for doc_id, weights in scores.items():
    for term, weight in weights.items():
        rows.append({"doc": doc_id, "term": term, "weight": round(weight, 3)})
weights_df = pl.DataFrame(rows)
print(weights_df.sort("weight", descending=True))
# end snippet vectors


# start snippet matrix
matrix = weights_df.pivot(on="term", index="doc", values="weight")
matrix = matrix.fill_null(0.0)
print(matrix)
# end snippet matrix


# start snippet top_terms
top_terms = weights_df.group_by("doc").agg(
    pl.col("term").sort_by("weight", descending=True).first().alias("top_term"),
    pl.col("weight").sort_by("weight", descending=True).first().alias("top_weight"),
)
print(top_terms.sort("doc"))
# end snippet top_terms
