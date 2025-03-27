"""
модуль для утилит, использующихся в других модулях
"""

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def jaccard_similarity(text1: str, text2: str) -> float:
    """Jaccard similarity score"""
    intersection = set(text1.split()) & set(text2.split())
    union = set(text1.split()).union(set(text2.split()))
    if len(union) != 0:
        return float(len(intersection) / len(union))
    return 0.0