from typing import Callable


class BaseService:
    """Base Service layer to manage business logic of multiple models by inheritance."""

    def __init__(self, repo_class: Callable):
        self.repo = repo_class()
