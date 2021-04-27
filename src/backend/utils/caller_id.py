from PIL import Image
from run import run
import pytesseract
import tempfile


'''
This module extracts the text with the largest font in an image,
which in our case would be the caller's id.

Some assumptions made with this method:
    - The caller's id is the largest font on your call screen.
    - Caller's id is present in the top 70% area of your call screen which is true for most devices.
    - Caller's id is present on a single line.

This method was used since I could not find any 
inbuilt functionality in adb to get caller's id.
'''


def get_text_groups(img_path):
    img = Image.open(img_path)
    img_w, img_h = img.size

    # crop image to get 7/10 part of the image
    img = img.crop((0, 0, img_w, 7 * (img_h / 10)))

    # get image's text using pytesseract
    text = pytesseract.image_to_string(img)

    # remove form feed characters and split by newline then filter out blank elements
    text = text.replace("\x0c", "").split("\n")
    text = [word for word in text if word != ""]
    if " " in text:
        text.remove(" ")

    return text


def get_area_data(img_path, grp_data):
    img = Image.open(img_path)
    img_w, img_h = img.size

    # crop image to get 7/10 part of the image
    img = img.crop((0, 0, img_w, 7 * (img_h / 10)))

    # get image's box data using pytesseract
    box_data = pytesseract.image_to_boxes(img)

    # initialize dict which stores each character + it's index number as key
    # and the character's bounding box's area as the value.
    area_dict = {}

    main_str = "".join(grp_data).replace(" ", "")

    i = 0
    # loops over each character and calculates each letter's area and updates area_dict
    for box in box_data.splitlines():
        box = box.split(' ')
        char, x1, y1, x2, y2 = box[0], int(box[1]), int(box[2]), int(box[3]), int(box[4])
        try:
            if char != main_str[i]:
                continue
        except IndexError:
            continue
        width, height = x2 - x1, y2 - y1
        area_dict[f"{char}{i}"] = width * height
        i += 1

    return area_dict


def get_biggest_text(img_path):
    text_groups = get_text_groups(img_path)
    area_table = get_area_data(img_path, text_groups)
    sum_dict = {}
    i = 0
    for word_index, group in enumerate(text_groups):
        sum_buffer = 0
        for letter in group:
            if letter != " ":
                sum_buffer += area_table[f"{letter}{i}"]
                i += 1
        sum_dict[sum_buffer] = word_index

    largest_area = max(sum_dict.keys())
    largest_word_key = sum_dict[largest_area]

    return text_groups[largest_word_key]


def get_caller_id():
    tmp_dir = tempfile.gettempdir()
    file_path = f"{tmp_dir}/call_screenshot.png"
    run(f"adb exec-out screencap -p > {file_path}")
    print(get_biggest_text(file_path))
