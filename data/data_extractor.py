import pickle
from typing import List, Union
from urlextract import URLExtract


class DataExtractor:
    @staticmethod
    def get_urls_from_file(file_path: str) -> Union[List[str], None]:
        file_content = None

        with open(file_path, "rb") as file:
            data = pickle.load(file)
            file_content = "".join(data).replace(",", "")

        if not file_content:
            return None

        extractor = URLExtract()
        urls = extractor.find_urls(file_content)

        return urls
