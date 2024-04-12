import bit_utility


# Mersenne Twister prg initalized with a seed
class MT19937:

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

        self.MT[0] = bit_utility.bytes_to_int(seed)
        for i in range(1, self.n):
            self.MT[i] = (1812433253 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i) & 0xFFFFFFFF
        #for i in range(1, self.n):
        #    print(self.MT[i -1])

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


# Mersenne Twister prg initalized with a state array
class MTClone:

    #    MT: a length n array to store the state of the generator
    #     w: word size (in number of bits)
    #     n: degree of recurrence
    #     m: middle word, an offset used in the recurrence relation defining the series x, 1 ≤ m < n
    #     r: separation point of one word, or the number of bits of the lower bitmask, 0 ≤ r ≤ w − 1
    #     a: coefficients of the rational normal form twist matrix
    #     b, c: TGFSR(R) tempering bitmasks
    #     s, t: TGFSR(R) tempering bit shifts
    #     u, d, l: additional Mersenne Twister tempering bit shifts/masks

    def __init__(self, state):
        self.index = 0
        self.MT = state
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


# reverses the left shift transformation by recovering chunks
def left_unmix(value, shift, mask):
    result = value
    w = 32

    for i in range(0, w, shift):
        # Work on the next shift sized portion at a time by generating a mask for it.
        partial_mask = '0' * (w - shift - i) + '1' * shift + '0' * i
        partial_mask = int(partial_mask, 2)
        portion = result & partial_mask

        result ^= ((portion << shift) & mask)

    return int(result)


# reverses the right shift transformation by recovering chunks
def right_unmix(value, shift):
    result = value
    w = 32

    for i in range(0, w, shift):
        # Work on the next shift sized portion at a time by generating a mask for it.
        partial_mask = '0' * i + '1' * shift + '0' * (w - shift - i)
        partial_mask = int(partial_mask[:w], 2)
        portion = result & partial_mask

        result ^= portion >> shift

    return int(result)


# reverse the mixing transformation of Mersenne Twister
def unmix_value(value):
    # Constants for MT19937, from the table above
    u = 11
    s = 7
    b = 0x9D2C5680
    t = 15
    c = 0xEFC60000
    l = 18

    y = right_unmix(value, l)
    y = left_unmix(y, t, c)
    y = left_unmix(y, s, b)
    y = right_unmix(y, u)

    return y

# applies the mixing transformation of Mersenne Twister
# simply for testing - not used in implementation
def mix_value(value):
    u = 11
    d = 0xFFFFFFFF
    s = 7
    b = 0x9D2C5680
    t = 15
    c = 0xEFC60000
    l = 18

    # Apply the transformations
    y1 = value ^ ((value >> u) & d)
    y2 = y1 ^ ((y1 << s) & b)
    y3 = y2 ^ ((y2 << t) & c)
    y4 = y3 ^ (y3 >> l)

    return y4 & 0xFFFFFFFF


def testing():
    # sample extractions to compare to clone
    mt_sample = MT19937(bit_utility.int_to_bytes(5))
    print("\n\n")
    print(mt_sample.extract_number())
    print(mt_sample.extract_number())

    # get the mixed state
    mt = MT19937(bit_utility.int_to_bytes(5))
    s = []
    for i in range(1, 625):
        s.append(mt.extract_number())

    # unmix the state to get initial state
    initial_state = []
    for t in s:
        initial_state.append(unmix_value(t))

    # clone and predict numbers
    clone = MTClone(initial_state)
    print(clone.extract_number())
    print(clone.extract_number())

# testing()

