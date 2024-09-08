import sys
import random
import math

def string_to_ascii(data):
    return [ord(i)
            for i in data]

def ascii_to_string(num):
    return [chr(i)
            for i in num]

def is_prime(num):
    if num == 2:
        return True
    elif num < 2:
        return False
    elif num % 2 == 0:
        return False
    else:
        for i in range(3, int(math.sqrt(num)), 2):
            if num%i == 0:
                return False
    return True


def modular_inverse(a, m):
    m0 = m
    y = 0
    x = 1
    if (m == 1):
        return 0
        
    while (a > 1):
        q = a // m
        t = m

        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t

    if (x < 0):
        x = x + m0
    return x

def int_to_bin(data, b):
    return ''.join(str(bin(i))[2:].zfill(b)
                    for i in data)

def bin_to_int(data, b):
    return [int(data[i:i+b], 2)
            for i in range(0, len(data), b)]

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def generate_keys():
    p = random.randint(1e12, 1e13-1)
    while not is_prime(p):
        p = random.randint(1e12, 1e13-1)
    q = random.randint(1e12, 1e13-1)
    while not is_prime(q):
        q = random.randint(1e12, 1e13-1)
    n = p*q
    phi = (p-1)*(q-1)
    e = random.randint(1, phi)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi)
    d = modular_inverse(e, phi)
    return n, e, d


def encrypt(pub, n, plain):
    cipher = []
    size=5;
    plainBlock = []
    s = plain
    while len(s) > 0:
        plainBlock.append(s[:size])
        s = s[size:].strip()
            
    numBlock = []
    for Iblock in plainBlock:
        numBlock.append(string_to_ascii(Iblock))

    binBlock = []
    for IbinBlock in numBlock:
        binBlock.append(int_to_bin(IbinBlock, 12))

    intBlock = []
    for IintBlock in binBlock:
        intBlock.append(int(IintBlock, 2))

    finalmessage=[]
    for Iecipher in intBlock:
        finalmessage.append(pow(int(Iecipher), int(pub), int(n)))
    str1 = " ".join(map(str,finalmessage))
    return str1


def decrypt(priv, n, cipher):
    finalDecrypt=''
    cipher_arr=[]
    cipher_text=''
    for i in range(len(cipher)):
        if(cipher[i]!=" "):
            cipher_text = cipher_text+cipher[i]
        else:
            cipher_arr.append(cipher_text)
            cipher_text=''        
    cipher_arr.append(cipher_text)
    intBlock2=[]
    cipher_arr= ' '.join(cipher_arr).split()
    for Icipher in cipher_arr:
        intBlock2.append(pow(int(Icipher), int(priv), int(n)))
    binBlock2= int_to_bin(intBlock2, 60)
    asciiBlock2 = bin_to_int(binBlock2, 12)
    finalDecrypt = ascii_to_string(asciiBlock2)
    space='\x00'
    while space in finalDecrypt:
        finalDecrypt.remove(space)
    str1 = "".join(map(str,finalDecrypt))
    return str1

