class PeopleRepository:

    def __init__(self):
        self._store = {}

    async def save_selected(self, cust_id, event_id, embeddings):
        self._store[(cust_id, event_id)] = embeddings

    async def get_selected(self, cust_id, event_id):
        return self._store.get((cust_id, event_id), [])


people_repository = PeopleRepository()