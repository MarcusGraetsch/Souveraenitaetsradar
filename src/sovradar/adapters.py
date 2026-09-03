from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from .models import GenericFact


class ProviderAdapter(ABC):
    """Translation boundary for customer-provided provider exports.

    Adapters parse files only. They do not authenticate to provider APIs and do not
    implement risk thresholds or final gate decisions.
    """

    provider_name: str

    @abstractmethod
    def can_parse(self, path: Path) -> bool:
        raise NotImplementedError

    @abstractmethod
    def parse(self, path: Path) -> list[GenericFact]:
        raise NotImplementedError
