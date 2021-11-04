from abc import ABC, abstractmethod


class ECLATEntity(ABC):

    def __init__(self, data: list, minSupport: int):
        self.data = data
        self.frequentItemSet = []
        self.minSupport = minSupport

    @abstractmethod
    def run(self,):
        """
        run eclat algorithms and the return all frequent k-item sets
        """

    @abstractmethod
    def saveAllFrequentItemSet(self, fileName: str):
        """
        save all frequent item set into a .txt file
        Args:
            fileName (str): saved .txt file name
        """
