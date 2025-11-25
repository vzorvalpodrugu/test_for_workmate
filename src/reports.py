from typing import List, Dict, Any
from abc import ABC, abstractmethod

class Report(ABC):
    @abstractmethod
    def generate_report(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_name(self):
        pass

