#!/usr/bin/env python3
from requests import Session
from threading import Thread, Lock
from time import sleep
from os import _exit
from argparse import ArgumentParser
from random import randint

global session
session = Session()

mutex = Lock()

global packet_number
packet_number=0


def get_session():
    global session
    if session is None:
        print("Session Started")
        session = Session()
    return session


def reset_session():
    global session
    if session is not None:
        print("Session Reset")
        session.close()
        session = None


def get_packet_number():
    global packet_number
    with mutex:
        packet_number = packet_number + 1
    return packet_number


def exec(data, session, timeout=3):
    sleep(randint(1,5))
    try:
        response = session.get("http://127.0.0.1:8080",
                               data=str(data),
                               timeout=timeout)
        print(response.text)
    except Exception as ex:
        # print(ex)
        reset_session()


if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument("--timeout", type=int)
    args = parser.parse_args()

    while True:
        # sleep(1)
        t = Thread(target=exec,
                   args=[get_packet_number(),
                         get_session(),
                         args.timeout,])
        t.start()