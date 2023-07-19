def encrypt(text, key):
    arr_text = text_in_numbers(text)
    ii = 0
    for i in range(0, len(arr_text)):
        if ii < (len(key) - 1):
            arr_text[i] = int(arr_text[i]) + int(key[ii])
        else:
            ii = 0
            arr_text[i] = int(arr_text[i]) + int(key[ii])
        if int(arr_text[i]) >= 1114112:
            arr_text[i] = int(arr_text[i]) - 1114112
        ii += 1
    arr_text = numbers_in_text(arr_text)
    return str(arr_text)

def numbers_in_text(numbers):
    ret_numbers = ""
    for i in numbers:
        ret_numbers += chr(i)
    return ret_numbers

def text_in_numbers(text):
    text_in_number = ""
    for i in text:
        text_in_number += str(ord(i)) + '_'
    return text_in_number.split('_')[:-1]


def decrypt(text, key):
    arr_text = text_in_numbers(text)
    ii = 0
    for i in range(0, len(arr_text)):
        if ii < (len(key) - 1):
            arr_text[i] = int(arr_text[i]) - int(key[ii])
        else:
            ii = 0
            arr_text[i] = int(arr_text[i]) - int(key[ii])
        if int(arr_text[i]) < 0:
            arr_text[i] = int(arr_text[i]) + 1114112
        ii += 1
    arr_text = numbers_in_text(arr_text)
    return str(arr_text)