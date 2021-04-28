def remove(string: str, *args):
    for each in args:
        if each in string:
            string = string.replace(each, "")

    return string
