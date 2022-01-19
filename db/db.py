from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, Sequence


class DB(ABC):
    @abstractmethod
    def insert(self, data: Dict, id: Optional[str]):
        pass

    @abstractmethod
    def insert_many(self, data_sequence: Sequence[Dict[Any, Any]]):
        pass


# Those methods should be in this abstract class, but I won't implement them
# due the small scope of this assignment

# @abstractmethod
# def find(self):
#     pass

# @abstractmethod
# def update(self):
#     pass

# @abstractmethod
# def delete(self):
#     pass
