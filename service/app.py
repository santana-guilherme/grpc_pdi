import grpc
import signal
import logging
import sqlite3
from concurrent import futures

import api_pb2_grpc
from service import APIServer
from database import Database

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def serve():
    port = "50051"
    conn = sqlite3.connect("scrap.db", check_same_thread=False)
    database = Database(conn)
    database.init_database()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_pb2_grpc.add_ScrapAPIServicer_to_server(APIServer(db=database), server)

    def gracefully_stop(sig, frame):
        log.info("shutting down")
        conn.close()
        server.stop(10)

    signal.signal(signal.SIGINT, gracefully_stop)

    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
