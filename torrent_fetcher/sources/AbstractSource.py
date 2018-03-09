from abc import ABC, abstractmethod
 
class AbstractSource(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def getTorrentsUrls(self, requestedPatterns):
        """
        Get a list of torrents urls associated to items matching the given
        patterns in the source.

        :param requestedPatterns:
            A collection of pattern matching described filtering on requested items.

        :return:
            A list of torrents urls matching the given pattern in the source.
        """
        pass
