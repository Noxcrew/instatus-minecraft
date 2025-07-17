#!/usr/bin/env python3
import json
import os
import sys
import time

import requests
from loguru import logger
from mcstatus import JavaServer

INSTATUS_API = os.getenv("INSTATUS_API", "https://api.instatus.com")
INSTATUS_PAGE_ID = os.getenv("INSTATUS_PAGE_ID")
INSTATUS_METRIC_ID = os.getenv("INSTATUS_METRIC_ID")
INSTATUS_TOKEN = os.getenv("INSTATUS_TOKEN")
MC_SERVER_IP = os.getenv("MC_SERVER_IP", "play.mccisland.net")
QUERY_INTERVAL = os.getenv("QUERY_INTERVAL", "30")

headers = {
    "Authorization": f"Bearer {INSTATUS_TOKEN}",
    "Content-Type": "application/json",
}


def query_server(address):
    """
    Query the Minecraft server for status and return playercount if online.
    """

    try:
        server = JavaServer.lookup(address)
        playercount = server.status().players.online
        logger.debug(f"Playercount: {playercount}")
        return playercount
    except Exception as e:
        logger.error(f"Exception while trying to query {MC_SERVER_IP}: {e}")
        return None


def push_metrics(timestamp, playercount):
    """
    Push metrics to Instatus.
    """

    data = {"data": [{"timestamp": timestamp, "value": playercount}]}

    try:
        logger.debug(f"Pushing metrics to Instatus: {timestamp}, {playercount}")
        r = requests.post(
            f"{INSTATUS_API}/v1/{INSTATUS_PAGE_ID}/metrics/{INSTATUS_METRIC_ID}/data",
            headers=headers,
            data=json.dumps(data),
        )
        r.raise_for_status()
        logger.info(
            f"Successfully pushed metrics to Instatus ({timestamp}, {playercount})"
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            logger.error(
                "Unauthorized (401) when pushing metrics to Instatus. Likely an invalid Instatus token."
            )
            sys.exit(1)
        logger.error("Error pushing metrics to Instatus: {}".format(e))


def main(log_level):
    logger.remove()
    logger.add(
        sys.stderr,
        colorize=True,
        level=log_level.upper(),
        backtrace=True,
        diagnose=True,
    )

    logger.info("instatus-minecraft")

    while True:
        playercount = query_server(MC_SERVER_IP)
        timestamp = int(time.time())

        if playercount == None:
            playercount = 0

        push_metrics(timestamp, playercount)

        time.sleep(int(QUERY_INTERVAL))


if __name__ == "__main__":
    log_level = os.getenv("LOG_LEVEL", "INFO")
    main(log_level)
