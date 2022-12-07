import os
from typing import List

from util import service_requests


def request_most_similar_record_ids(
    project_id: str, embedding_id: str, record_id: str, limit: int
) -> List[str]:
    url = f"{os.getenv('NEURAL_SEARCH')}/most_similar"
    params = {
        "project_id": project_id,
        "embedding_id": embedding_id,
        "record_id": record_id,
        "limit": limit,
    }
    result = service_requests.get_call_or_raise(url, params)
    return result
