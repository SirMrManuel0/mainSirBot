# Function to encrypt text using a key
def encrypt(text, key):
    """
    Encrypts the given text using the provided key.

    Args:
    text (str): The text to be encrypted.
    key (str): The key used for encryption.

    Returns:
    str: The encrypted text.
    """
    # Convert the text into a list of numbers
    arr_text = text_in_numbers(text)
    ii = 0
    for i in range(0, len(arr_text)):
        # Add the key value to the corresponding element in the list
        if ii < (len(key) - 1):
            arr_text[i] = int(arr_text[i]) + int(key[ii])
        else:
            ii = 0
            arr_text[i] = int(arr_text[i]) + int(key[ii])
        # Ensure the resulting number is within a valid range
        if int(arr_text[i]) >= 1114112:
            arr_text[i] = int(arr_text[i]) - 1114112
        ii += 1
    # Convert the list of numbers back to a string
    arr_text = numbers_in_text(arr_text)
    return str(arr_text)

# Function to convert a list of numbers to a text string
def numbers_in_text(numbers):
    """
    Converts a list of numbers to a text string.

    Args:
    numbers (list of int): List of numbers to be converted to text.

    Returns:
    str: The text string created from the list of numbers.
    """
    ret_numbers = ""
    for i in numbers:
        ret_numbers += chr(i)
    return ret_numbers

# Function to convert a text string to a list of numbers
def text_in_numbers(text):
    """
    Converts a text string to a list of numbers.

    Args:
    text (str): The text string to be converted to numbers.

    Returns:
    list of int: The list of numbers created from the text string.
    """
    text_in_number = ""
    for i in text:
        text_in_number += str(ord(i)) + '_'
    return text_in_number.split('_')[:-1]

# Function to decrypt text using a key
def decrypt(text, key):
    """
    Decrypts the given text using the provided key.

    Args:
    text (str): The text to be decrypted.
    key (str): The key used for decryption.

    Returns:
    str: The decrypted text.
    """
    # Convert the text into a list of numbers
    arr_text = text_in_numbers(text)
    ii = 0
    for i in range(0, len(arr_text)):
        # Subtract the key value from the corresponding element in the list
        if ii < (len(key) - 1):
            arr_text[i] = int(arr_text[i]) - int(key[ii])
        else:
            ii = 0
            arr_text[i] = int(arr_text[i]) - int(key[ii])
        # Ensure the resulting number is within a valid range
        if int(arr_text[i]) < 0:
            arr_text[i] = int(arr_text[i]) + 1114112
        ii += 1
    # Convert the list of numbers back to a string
    arr_text = numbers_in_text(arr_text)
    return str(arr_text)