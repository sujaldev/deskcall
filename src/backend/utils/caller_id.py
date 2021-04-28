from src.backend.utils.string_funcs import remove
from src.backend.utils.run import run


def get_call_status():
    output = run(r'adb shell dumpsys telephony.registry | grep "mCallState\|mCallIncomingNumber"')
    parsed_output = {
        "mCallState": {},
        "mCallIncomingNumber": {}
    }

    i = 0
    for current_line in output:
        if "    mCallState=" in current_line:
            parsed_output["mCallState"][i] = int(remove(current_line, "    mCallState=", "\n"))
        elif "    mCallIncomingNumber=" in current_line:
            parsed_output["mCallIncomingNumber"][i] = remove(current_line, "    mCallIncomingNumber=", "\n")
            i += 1
        else:
            raise Exception("Output from adb command not what was expected.")

    return parsed_output


def get_incoming_call_num():
    parsed_output = get_call_status()
    for key in parsed_output["mCallIncomingNumber"].keys():
        number = parsed_output["mCallIncomingNumber"][key]
        if number != "":
            return number

    return 0
