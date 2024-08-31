import logging

import grpc
import api_pb2
import api_pb2_grpc
from argparse import ArgumentParser


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

parser = ArgumentParser()
parser.add_argument('-url', dest='url')
parser.add_argument('-ret', dest='ret')
args = parser.parse_args()

if args.url:
    log.info('Sending request')
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = api_pb2_grpc.ScrapAPIStub(channel)
        response = stub.ScrapURL(api_pb2.ScrapRequest(url=args.url))
        log.info("Api response received: " + response.message)

if args.ret:
    log.info('Retrieving scraped urls')
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = api_pb2_grpc.ScrapAPIStub(channel)
        response = stub.GetScrapedURLS(api_pb2.google_dot_protobuf_dot_empty__pb2.Empty())
        for i in response.scrapedurl:
            print(f"{i.url} -- {i.html[:50]}")
