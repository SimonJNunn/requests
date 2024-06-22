#!/usr/bin/env python3
from requests import Session
from threading import Thread, Lock
from time import sleep
from os import _exit
from argparse import ArgumentParser
from random import randint
import atexit

packet_mutex = Lock()
reset_mutex = Lock()
session_mutex = Lock()

global session
session = Session()

global packet_number
packet_number=0

global reset_counter
reset_counter=0


def increment_reset_counter():
    global reset_counter
    with reset_mutex:
        reset_counter = reset_counter + 1
    return reset_counter


def get_session():
    global session
    with session_mutex:
        if session is None:
            print("Session Started")
            session = Session()
    return session


def reset_session():
    global session
    with session_mutex:
        if session is not None:
            reset_number = increment_reset_counter()
            print(f"Session Reset #{reset_number}")
            session.close()


def get_packet_number():
    global packet_number
    with packet_mutex:
        packet_number = packet_number + 1
    return packet_number


def exec(timeout=3):
    try:
        response = get_session().get("http://127.0.0.1:8080",
                               data=str(get_packet_number()),
                               timeout=timeout)
        print(response.text)
    except Exception as ex:
        print(ex)
        reset_session()


def proc(timeout=3):
    while True:
        # sleep(1)
        t = Thread(target=exec,
                   args=[timeout])
        t.start()


def exit_handler():
    global reset_counter
    print (f"==================")
    print (f"|| resets: {reset_counter} ||")
    print (f"==================")


if __name__=="__main__":
    atexit.register(exit_handler)

    parser = ArgumentParser()
    parser.add_argument("--timeout", type=int)
    args = parser.parse_args()

    proc1 = Thread(target=proc, args=[args.timeout])
    proc1.start()

    proc2 = Thread(target=proc, args=[args.timeout])
    proc2.start()

    sleep(10)
    _exit(0)
