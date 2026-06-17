from services.selected_people import get_face_embedding
from repository.people_repository import save_embeddings


def save_selected_people(dto):
    embeddings = []

    for path in dto.image_paths:
        emb = get_face_embedding(path)

        if emb is not None:
            embeddings.append(emb)

    save_embeddings(dto.cust_id, dto.event_id, embeddings)