#! /usr/bin/python

import argparse
import re
import time
from urllib.parse import urlparse

import requests

# Color Codes
###############################################################################

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
statusCodeDict = {"200": "Valid", "400": "Bad Request", "401": "Un-Authorized", "404": "Not Found",
                  "500": "Server Error", "502": "Bad Gateway", "504": "Gateway Timeout", "DOWN": "DOWN",
                  "403": "Forbidden"}


def main():
    parser = argparse.ArgumentParser(description="Checking if URL is up / down")
    parser.add_argument("-f", help=("Input the filename / Drop the file after URLChecker.py"), dest="input", type=str,
                        required=True)
    parser.add_argument("-o", help="Output filename : ", dest="output", type=str, required=False)
    args = parser.parse_args()
    print("\nTesting URLs.", time.ctime())
    checkUrls(args)


def parseURLDomainOnly(lines):
    parsed_url = urlparse(lines)
    result = ("{url.scheme}://{url.netloc}/".format(url=parsed_url))
    return result


def checkUrls(args):
    URLS = []

    def parseFile():
        f = open(args.input, "r")
        for lines in f:
            lines = parseURLDomainOnly(lines)  # Parser for Domain Only.
            if not lines.find("https"):
                URLS.append(lines)
            lines = re.sub("https", "http", lines)
            URLS.append(lines)

    parseFile()
    for url in URLS:
        status = "N/A"
        try:
            status = checkUrl(url)
        except requests.exceptions.ConnectionError as e:
            status = "DOWN"
        printStatus(url, status)


def checkUrl(url):
    r = requests.get(url, timeout=5)  # Set the timeout here.
    # print r.status_code
    return str(r.status_code)


def printStatus(url, status):
    color = GREEN

    if status != "200":
        color = RED
    if status not in statusCodeDict:
        statusCodeDict[status] = "Unknown Code"
        print(color + "[" + statusCodeDict[status] + "]" + ENDC + ' ' + url)

if __name__ == '__main__':
    main()
