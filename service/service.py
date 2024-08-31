import logging
import api_pb2
import api_pb2_grpc
from database import Database
import sqlite3

import requests

logger = logging.getLogger(__name__)


class APIServer(api_pb2_grpc.ScrapAPI):

    def __init__(self, db: Database) -> None:
        self.db = db

    def ScrapURL(self, request, context):
        response = api_pb2.ScrapResponse()
        try:
            resp = requests.get(request.url)
            resp.raise_for_status()

            self.db.insert_website(request.url, resp.text)
            response.status = 200
            response.message = f"{request.url} successfully scraped and stored"
        except Exception as ex:
            logger.exception(f"Error getting response from {request.url}. Ex: {ex}")
            response.status = 500
            response.message = f"Error getting response from {request.url}. Ex: {ex}"
        logger.info("returning response ")
        return response

    def GetScrapedURLS(self, request, context):
        response = api_pb2.ScrapedUrlList(scrapedurl=[])
        for row in self.db.fetch_all_websites():
            response.scrapedurl.append(api_pb2.ScrapedUrl(url=row[0], html=row[1]))

        return response
