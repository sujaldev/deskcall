import os


def run(command):
    stream = os.popen(command)
    return stream.readlines()
