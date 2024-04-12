import bit_utility
import Mersenne
import time
import random


import base64

# Returns a single output of Mersenne Twister seeded using current time
def oracle():
    # Wait between 5 and 60 seconds
    wait_time = random.randint(5, 60)
    time.sleep(wait_time)

    # Seed MT19937 using the current UNIX timestamp
    seed = int(time.time())
    mt = Mersenne.MersenneTwister(bit_utility.int_to_bytes(seed))
    print("The seed we are looking for is : " + repr(seed))

    # Wait another randomly chosen number of seconds between 5 and 60
    wait_time = random.randint(5, 60)
    time.sleep(wait_time)

    # Return the first 32 bit output as a base64 encoded value
    output = bit_utility.int_to_bytes(mt.extract_number())
    encoded_output = base64.b64encode(output)
    return encoded_output


# Returns seed of Mersenne Twister instance
# Uses timeframe of possible seeds and compares first output
def break_it(output):
    current_time = int(time.time())
    for i in range(current_time - 60, current_time - 5):
        prg = Mersenne.MersenneTwister(bit_utility.int_to_bytes(i))
        prg_output = bit_utility.int_to_bytes(prg.extract_number())
        encoded_prg_output = base64.b64encode(prg_output)
        if output == encoded_prg_output:
            print("Match found - Seed is : " + repr(i))
            break
    else:
        print("No match found")


# Test the oracle
testing = oracle()
# print(oracle())

# Find the seed
break_it(testing)

