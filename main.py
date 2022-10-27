import time
from loguru import logger

from data_extractor import DataExtractor
from url_availability_checker import UrlAvailabilityChecker

FILE_DATA_PATH = "data/messages_to_parse.dat"
LOGER_PATH = "loger/file_{time}.log"


def timer(func):
    def wrap_func(*args, **kwargs):
        print("Start")

        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()

        with open("README.md", "w") as readme_f:
            readme_f.write(f"Spent: {end - start} time\n")
            readme_f.write(f"quantity of all links: {len(result[0])}\n")
            readme_f.write(f"quantity of unshorten links: {len(result[1])}\n")

        print(f"Finished: Spent:{end - start}")

        return result

    return wrap_func


@timer
def main():
    logger.add(LOGER_PATH, rotation="5 min", retention="20 min", enqueue=True)
    logger.info("The program has been started")

    urls = DataExtractor.get_urls_from_file(FILE_DATA_PATH)
    url_checker = UrlAvailabilityChecker(urls)
    url_checker.main_threads()
    all_urls = url_checker.result_status_codes
    unshorten_urls = url_checker.result_unshorten_urls

    logger.info("The program has been completed")

    return all_urls, unshorten_urls


if __name__ == '__main__':
    main()
