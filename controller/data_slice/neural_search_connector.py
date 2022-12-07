import os
from util import service_requests


def request_outlier_detection(project_id: str, embedding_id: str, limit: int):
    url = f"{os.getenv('NEURAL_SEARCH')}/detect_outliers"
    params = {
        "project_id": project_id,
        "embedding_id": embedding_id,
        "limit": limit,
    }
    result = service_requests.get_call_or_raise(url, params)
    return result
