import math

def unary_code(q):
    return '1' * q + '0'

def golomb_old_encode(N,M):
    q = N // M
    r = N % M
    quo = unary_code(q)
    b = math.floor(math.log2(M))
    c = math.ceil(math.log2(M))
    rem = bin(r)[2:]
    l = len(rem)

    if b == c:
        rem = '0'*(b-l) + rem
        return quo + rem

    k = 2 ** c - M
    if r < k: # encode r in b bits
        rem = '0' * (b - l) + rem
        return quo + rem

    rem = bin(r + k)[2:]
    l = len(rem)
    rem = '0' * (c - l) + rem
    return quo + rem

def golomb_encode(N,M=4):
    q = N // M
    r = N % M
    quo = unary_code(q)
    b = math.floor(math.log2(M))
    rem = bin(r)[2:]
    l = len(rem)

    k = 2 ** (b+1) - M
    if r < k: # encode r in b bits
        rem = '0' * (b - l) + rem
        return quo + rem

    rem = bin(r + k)[2:] #encode r+k in b+1 bits
    l = len(rem)
    rem = '0' * (b+1 - l) + rem
    return quo + rem

def golomb_my_decode(code, M=4): #need fix
    b = math.floor(math.log2(M))
    k = 2 ** (b + 1) - M
    q = 0
    i = 0 # tracker
    while i < len(code) and code[i] == '1':
    # getting q value by count number of '1' stop when see 0 also we check i < len(code) to prevent
    # infinite loop like this -> 11111
        q += 1
        i += 1
    i += 1
    if i + b > len(code): # if we got something like 11110 -> invalid
        raise ValueError("Invalid code")
    n = M*q
    r_bits = code[i:i+b]
    r = int(r_bits, 2)
    return n+r

def golomb_decode(code, M=4):
    b = math.floor(math.log2(M))
    k = 2 ** (b + 1) - M
    q = 0
    i = 0 # tracker
    while i < len(code) and code[i] == '1':
    # getting q value by count number of '1' stop when see 0 also we check i < len(code) to prevent
    # infinite loop like this -> 11111
        q += 1
        i += 1
    i += 1
    if i + b > len(code): # if we got something like 11110 -> invalid
        raise ValueError("Invalid code")

    r_bits = code[i:i+b]
    r = int(r_bits, 2)

    if r < k:
        i += b
    else:
        if i + b + 1 > len(code):
            raise ValueError("Invalid code")
        r_bits = code[i:i + b + 1]
        r = int(r_bits, 2) - k
        i += (b + 1)

    return q * M + r
