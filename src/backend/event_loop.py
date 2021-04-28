from utils.caller_id import get_call_status, get_incoming_call_num
from utils.call_handler import *
from time import sleep


while True:
    sleep(2)
    call_status = get_call_status()["mCallState"].values()
    if 1 in call_status:
        handle_incoming_call()
    elif 2 in call_status:
        handle_call_pickup()
    else:
        print("no incoming calls")
