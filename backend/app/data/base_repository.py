from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    @abstractmethod
    def customers(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def churn_events(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def propensity_scores(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def customer_interactions(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def offers(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def contract_episodes(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def source_version(self) -> str:
        raise NotImplementedError
