#!/usr/bin/python3
# -*- coding: utf-8 -*-
from urllib import request
from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import xml.etree.ElementTree as eTree
import datetime
import re

url = "http://www.cbr.ru/scripts/XML_daily.asp"


def getrate(codeid, root_node):
    target = root_node.find("./Valute[CharCode='" + codeid + "']")
    rate = target.__getitem__(4).text
    return rate


def getcode():
    return "code"


def getdate(root_node):
    return datetime.datetime.strptime(root_node.attrib['Date'], '%d.%m.%Y').strftime('%Y-%m-%d')


class HttpSrv(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _set_headers_json(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if re.match(r"/currency/api/rate/[A-Z]{3}/([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))", self.path):
            self._set_headers_json()
            code = self.path.split("/")[4]
            urlDate = url + "?date_req=" + datetime.datetime.strptime(self.path.split("/")[5], '%Y-%m-%d').strftime('%d/%m/%Y')
            tree = eTree.parse(request.urlopen(urlDate))
            root_node = tree.getroot()
            body = '{"code": "' + code + '","rate": "' + getrate(code, root_node) + '","date": "' + getdate(root_node) + '"}'
            self.wfile.write(body.encode())
        elif re.match(r"/currency/api/rate/[A-Z]{3}", self.path):
            self._set_headers_json()
            code = self.path.split("/")[4]
            tree = eTree.parse(request.urlopen(url))
            root_node = tree.getroot()
            body = '{"code": "' + code + '","rate": "' + getrate(code, root_node) + '","date": "' + getdate(root_node) + '"}'
            self.wfile.write(body.encode())
        else:
            self.send_response(502)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self.send_response(501)
        self.send_header("Content-type", "text/html")
        self.end_headers()


def run(server_class=HTTPServer, handler_class=HttpSrv, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print("Starting httpd server on " + str(addr) + ":" + str(port))
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="0.0.0.0",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=50001,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
