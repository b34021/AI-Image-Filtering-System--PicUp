import math


def cosine_similarity(vec1, vec2):
    dot = 0.0
    norm1 = 0.0
    norm2 = 0.0

    for a, b in zip(vec1, vec2):
        dot += a * b
        norm1 += a * a
        norm2 += b * b

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot / (math.sqrt(norm1) * math.sqrt(norm2))


def match_selected_people(face_embedding, selected_embeddings, threshold=0.5):

    for emb in selected_embeddings:

        similarity = cosine_similarity(face_embedding, emb)

        if similarity > threshold:
            return True

    return False