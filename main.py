from crawlers.pastebin_crawler import PastebinCrawler
from db.local_storage_db import LocalStorageDB


def main():
    pastebin = PastebinCrawler(db=LocalStorageDB(directory="pastebin"))
    pastebin.process()


main()
