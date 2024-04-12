import bit_utility
import base64



#Mersenne Twister MT 19937
class MersenneTwister:

    #    MT: a length n array to store the state of the generator
    #     w: word size (in number of bits)
    #     n: degree of recurrence
    #     m: middle word, an offset used in the recurrence relation defining the series x, 1 ≤ m < n
    #     r: separation point of one word, or the number of bits of the lower bitmask, 0 ≤ r ≤ w − 1
    #     a: coefficients of the rational normal form twist matrix
    #     b, c: TGFSR(R) tempering bitmasks
    #     s, t: TGFSR(R) tempering bit shifts
    #     u, d, l: additional Mersenne Twister tempering bit shifts/masks

    def __init__(self, seed):
        self.index = 0
        self.MT = [0] * 624
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908B0DF
        self.u = 11
        self.d = 0xFFFFFFFF
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (1 << self.w) - self.lower_mask

        self.index = self.n
        self.MT[0] = bit_utility.bytes_to_int(seed)
        for i in range(1, self.n):
            self.MT[i] = (1812433253 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i) & 0xFFFFFFFF

    # Extract a tempered value based on MT[index]
    # calling twist() every n numbers
    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
                raise Exception("Generator was never seeded")
            self.twist()

        y = self.MT[self.index]
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= y >> self.l

        self.index += 1
        return y & 0xFFFFFFFF

    # Generate the next n values from the series x_i
    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0


# Testing the implementation
def MersenneGenerate():
    mt = MersenneTwister(bit_utility.int_to_bytes(5))
    output = bit_utility.int_to_bytes(mt.extract_number())
    encoded_output = base64.b64encode(output)
    print(encoded_output)


# MersenneGenerate()
