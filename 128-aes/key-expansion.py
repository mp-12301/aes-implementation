# AES Key Expansion

def KeyExpansion(cipher_key):

    # S-box
    ssbox = initializeAESSBOX()
    # Number of 32 bits words that comprise the cipher key
    nk = (len(cipher_key) * 8) / 32
    # Number of 32 bits columns that comprise the state
    nb = 4
    # Number of rounds that is a function of nk and nb (=4)
    nr = {
        4: 10,
        6: 12,
        8: 14
    }[nk]

    w = []

    for i in range(0, len(cipher_key), nb):
        w.append(cipher_key[i:i + nb])

    for i in range(nk, nb * (nr + 1)):
        temp = w[i-1]
        if (i % nk == 0):
            temp = wxor(subWord(ssbox, rotWord(temp)), rcon(i / nk))
        elif (nk > 6 and i % nk == 4):
            temp = subWord(ssbox, temp)
        w.append(wxor(w[i - nk], temp))
    print len(w)

    return


def rotWord(word):
    return word[1:] + word[0]


def subWord(ssbox, word):
    subword = []
    for b in word:
        subword.append(chr(ssbox[ord(b)]))
    return ''.join(subword)


def wxor(w1, w2):
    return ''.join([chr(ord(b1) ^ ord(b2)) for b1, b2 in zip(w1, w2)])


def rcon(i):
    # TODO Function to calculate first byte x**(i-1) in GF(2^8)
    fb = {
        1: '\x01',
        2: '\x02',
        3: '\x04',
        4: '\x08',
        5: '\x10',
        6: '\x20',
        7: '\x40',
        8: '\x80',
        9: '\x1b',
        10: '\x36'
    }
    return [fb[i], '\x00', '\x00', '\x00', '\x00', '\x00', '\x00']


def ROTL8(x, shift):
    return 0xff & (((x) << (shift)) | ((x) >> (8 - (shift))))


def initializeAESSBOX():
    sbox = [None] * 256
    p = q = 1
    firstTime = True

    # loop invariant: p * q == 1 in the Galois field
    # To simulate a do/while loop
    while p != 1 or firstTime:
            # multiply p by 3
            p = p ^ (p << 1) ^ (0x1B if p & 0x80 else 0)
            p = p & 0xff

            # divide q by 3
            q ^= q << 1
            q ^= q << 2
            q ^= q << 4
            q ^= 0x09 if q & 0x80 else 0
            q = q & 0xff

            # compute the affine transformation
            xformed = q ^ ROTL8(q, 1) ^ ROTL8(q, 2) ^ ROTL8(q, 3) ^ ROTL8(q, 4)

            sbox[p] = xformed ^ 0x63
            firstTime = False

    # 0 is a special case since it has no inverse
    sbox[0] = 0x63

    return sbox


import binascii

KeyExpansion(binascii.a2b_hex('2b7e151628aed2a6abf7158809cf4f3c'))
