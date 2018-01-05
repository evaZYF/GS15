# coding: utf-8

# coding: utf-8

from __builtin__ import pow as powmod
import random


def lectureFichier():
    motsFichier = []
    with open(raw_input("Saisir le nom du fichier à chiffrer (ou le chemin direct) : "), "rb") as file:
        compteur = 0
        while True:
            byte = file.read(1)
            if byte.encode('hex') == '':
                break
            if byte.encode('hex') != '':
                binaire = bin(int(byte.encode('hex'), 16))[2:].zfill(8)

                if compteur != 0:
                    if len(str(motsFichier[compteur - 1])) == 64:
                        motsFichier.append(str(binaire))
                        compteur += 1
                    else:
                        motsFichier[compteur - 1] = str(motsFichier[compteur - 1]) + str(binaire)
                else:
                    motsFichier.insert(compteur, binaire)
                    compteur += 1
    file.close()
    return motsFichier


# Constants

init_hash_values = [
    '6a09e667', 'bb67ae85', '3c6ef372', 'a54ff53a',
    '510e527f', '9b05688c', '1f83d9ab', '5be0cd19'
]

sha256_const = [
    '428a2f98', '71374491', 'b5c0fbcf', 'e9b5dba5',
    '3956c25b', '59f111f1', '923f82a4', 'ab1c5ed5',
    'd807aa98', '12835b01', '243185be', '550c7dc3',
    '72be5d74', '80deb1fe', '9bdc06a7', 'c19bf174',
    'e49b69c1', 'efbe4786', '0fc19dc6', '240ca1cc',
    '2de92c6f', '4a7484aa', '5cb0a9dc', '76f988da',
    '983e5152', 'a831c66d', 'b00327c8', 'bf597fc7',
    'c6e00bf3', 'd5a79147', '06ca6351', '14292967',
    '27b70a85', '2e1b2138', '4d2c6dfc', '53380d13',
    '650a7354', '766a0abb', '81c2c92e', '92722c85',
    'a2bfe8a1', 'a81a664b', 'c24b8b70', 'c76c51a3',
    'd192e819', 'd6990624', 'f40e3585', '106aa070',
    '19a4c116', '1e376c08', '2748774c', '34b0bcb5',
    '391c0cb3', '4ed8aa4a', '5b9cca4f', '682e6ff3',
    '748f82ee', '78a5636f', '84c87814', '8cc70208',
    '90befffa', 'a4506ceb', 'bef9a3f7', 'c67178f2'
]


# Tools

def rabin_miller(n):
    s = n - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1
    for test in range(10):
        rand = random.randrange(2, n - 1)
        v = pow(rand, s, n)
        if v != 1:
            i = 0
            while v != n - 1:
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = (v ** 2) % n
    return True


def isPrime(n):
    if n == 2:
        return True
    if n % 2 == 0 or n < 2:
        return False
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                 991, 997]
    if n in lowPrimes:
        return True
    for p in lowPrimes:
        if n % p == 0:
            return False
    return rabin_miller(n)


def largePrime(size):
    while True:
        lp = random.randrange(2 ** (size - 1), 2 ** size)
        if isPrime(lp):
            return lp


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def toBin(dec):
    return str(format(dec, 'b'))


def bin_8bit(dec):
    return str(format(dec, '08b'))


def bin_32bit(dec):
    return str(format(dec, '032b'))


def bin_64bit(dec):
    return str(format(dec, '064b'))


def toHex(dec):
    return str(format(dec, 'x'))


def bin2dec(bin_str):
    return int(bin_str, 2)


def hex2dec(hex_str):
    return int(hex_str, 16)


def L_P(set, n):
    result = []
    j = 0
    k = n
    while k < len(set) + 1:
        result.append(set[j:k])
        j = k
        k += n
    return result


def str2list(bit_str):
    bit_list = []
    for i in range(len(bit_str)):
        bit_list.append(bit_str[i])
    return bit_list


def list2str(bit_list):
    bit_str = ''
    for i in range(len(bit_list)):
        bit_str += bit_list[i]
    return bit_str


def ror(bit_str, n):
    bit_list = str2list(bit_str)
    ctr = 0
    while ctr <= n - 1:
        list_final = list(bit_list)
        tmp = list_final.pop(-1)
        list_final = list([tmp] + list_final)
        bit_list = list(list_final)
        ctr += 1
    return list2str(list_final)


def shift_right(bit_str, n):
    bit_list = str2list(bit_str)
    ctr = 0
    while ctr <= n - 1:
        bit_list.pop(-1)
        ctr += 1
    beg = ['0'] * n
    return list2str(beg + bit_list)


def add_mod_32(input_set):
    value = 0
    for i in range(len(input_set)):
        value += input_set[i]
    mod_32 = 4294967296
    return value % mod_32


def xor_2str(bit_str_1, bit_str_2):
    xor_list = []
    for i in range(len(bit_str_1)):
        if bit_str_1[i] == '0' and bit_str_2[i] == '0':
            xor_list.append('0')
        if bit_str_1[i] == '1' and bit_str_2[i] == '1':
            xor_list.append('0')
        if bit_str_1[i] == '0' and bit_str_2[i] == '1':
            xor_list.append('1')
        if bit_str_1[i] == '1' and bit_str_2[i] == '0':
            xor_list.append('1')
    return list2str(xor_list)


def and_2str(bit_str_1, bit_str_2):
    and_list = []
    for i in range(len(bit_str_1)):
        if bit_str_1[i] == '1' and bit_str_2[i] == '1':
            and_list.append('1')
        else:
            and_list.append('0')

    return list2str(and_list)


def or_2str(bit_str_1, bit_str_2):
    or_list = []
    for i in range(len(bit_str_1)):
        if bit_str_1[i] == '0' and bit_str_2[i] == '0':
            or_list.append('0')
        else:
            or_list.append('1')
    return list2str(or_list)


def not_str(bit_str):
    not_list = []
    for i in range(len(bit_str)):
        if bit_str[i] == '0':
            not_list.append('1')
        else:
            not_list.append('0')
    return list2str(not_list)


# SHA-256 Functions

# Compression
def ch(x, y, z):
    return xor_2str(and_2str(x, y), and_2str(not_str(x), z))


def maj(x, y, z):
    return xor_2str(xor_2str(and_2str(x, y), and_2str(x, z)), and_2str(y, z))


def S0(x):
    return xor_2str(xor_2str(ror(x, 2), ror(x, 13)), ror(x, 22))


def S1(x):
    return xor_2str(xor_2str(ror(x, 6), ror(x, 11)), ror(x, 25))


def s0(x):
    return xor_2str(xor_2str(ror(x, 7), ror(x, 18)), shift_right(x, 3))


def s1(x):
    return xor_2str(xor_2str(ror(x, 17), ror(x, 19)), shift_right(x, 10))


# Pre processing
def padding(bit_list):
    pad_one = bit_list + '1'
    pad_len = len(pad_one)
    k = 0
    while ((pad_len + k) - 448) % 512 != 0:
        k += 1
    temp0 = '0' * k
    temp1 = bin_64bit(len(bit_list))
    return pad_one + temp0 + temp1


def bit_return(str):
    bit_list = []
    for i in range(len(str)):
        bit_list.append(bin_8bit(ord(str[i])))
    return (list2str(bit_list))


def pre_pro(str):
    bit_main = bit_return(str)
    return padding(bit_main)


def parsing(str):
    return L_P(pre_pro(str), 32)


def schedule(ind, msg):
    new_msg = bin_32bit(add_mod_32(
        [int(s1(msg[ind - 2]), 2), int(msg[ind - 7], 2), int(s0(msg[ind - 15]), 2), int(msg[ind - 16], 2)]))
    return new_msg


# sha-256 function

def sha_256(str):
    msg = parsing(str)
    a = bin_32bit(hex2dec(init_hash_values[0]))
    b = bin_32bit(hex2dec(init_hash_values[1]))
    c = bin_32bit(hex2dec(init_hash_values[2]))
    d = bin_32bit(hex2dec(init_hash_values[3]))
    e = bin_32bit(hex2dec(init_hash_values[4]))
    f = bin_32bit(hex2dec(init_hash_values[5]))
    g = bin_32bit(hex2dec(init_hash_values[6]))
    h = bin_32bit(hex2dec(init_hash_values[7]))
    for i in range(0, 64):
        if i <= 15:
            tmp1 = add_mod_32(
                [int(h, 2), int(S1(e), 2), int(ch(e, f, g), 2), int(sha256_const[i], 16), int(msg[i], 2)])
            tmp2 = add_mod_32([int(S0(a), 2), int(maj(a, b, c), 2)])
            h = g
            g = f
            f = e
            e = add_mod_32([int(d, 2), tmp1])
            d = c
            c = b
            b = a
            a = add_mod_32([tmp1, tmp2])
            a = bin_32bit(a)
            e = bin_32bit(e)
        if i > 15:
            msg.append(schedule(i, msg))
            tmp1 = add_mod_32(
                [int(h, 2), int(S1(e), 2), int(ch(e, f, g), 2), int(sha256_const[i], 16), int(msg[i], 2)])
            tmp2 = add_mod_32([int(S0(a), 2), int(maj(a, b, c), 2)])
            h = g
            g = f
            f = e
            e = add_mod_32([int(d, 2), tmp1])
            d = c
            c = b
            b = a
            a = add_mod_32([tmp1, tmp2])
            a = bin_32bit(a)
            e = bin_32bit(e)

    hash_0 = add_mod_32([hex2dec(init_hash_values[0]), int(a, 2)])
    hash_1 = add_mod_32([hex2dec(init_hash_values[1]), int(b, 2)])
    hash_2 = add_mod_32([hex2dec(init_hash_values[2]), int(c, 2)])
    hash_3 = add_mod_32([hex2dec(init_hash_values[3]), int(d, 2)])
    hash_4 = add_mod_32([hex2dec(init_hash_values[4]), int(e, 2)])
    hash_5 = add_mod_32([hex2dec(init_hash_values[5]), int(f, 2)])
    hash_6 = add_mod_32([hex2dec(init_hash_values[6]), int(g, 2)])
    hash_7 = add_mod_32([hex2dec(init_hash_values[7]), int(h, 2)])
    hash_tab = (toHex(hash_0),
                toHex(hash_1),
                toHex(hash_2),
                toHex(hash_3),
                toHex(hash_4),
                toHex(hash_5),
                toHex(hash_6),
                toHex(hash_7))
    final_hash = ""
    for i in range(0, 7):
        final_hash += hash_tab[i]
    return final_hash


''' Blake2b hash implementation test (not working)

# IV for hash computation
IV = [0x6A09E667F3BCC908, 0xBB67AE8584CAA73B, 0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1, 0x510E527FADE682D1, 0x9B05688C2B3E6C1F, 0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179]

def ror64(x, y):
    return (x >> y) ^ (x << (64 - y))

def blake2b_mix(V, a, b, c, d, x, y):
    V[a] = V[a] + V[b] + x
    V[d] = ror64(V[d] ^ V[a], 32)
    V[c] += V[d]
    V[b] = ror64(V[b] ^ V[c], 24)
    V[a] = V[a] + V[b] + y
    V[d] = ror64(V[d] ^ V[a], 16)
    V[c] += V[d]
    V[b] = ror64(V[b] ^ V[c], 63)
    return V

def blake2b_compress(h, chunk, t, isLastBlock):
    sigma = [[ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ],
           [ 14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3 ],
           [ 11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4 ],
           [ 7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8 ],
           [ 9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13 ],
           [ 2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9 ],
           [ 12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11 ],
           [ 13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10 ],
           [ 6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5 ],
           [ 10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0 ],
           [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ],
           [ 14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3 ]]
    V = []
    s = []
    for i in range(0, 7):
        V[i] = h[i]
    for i in range(8, 15):
        V[i] = IV[i]

    V[12] ^= t % 2**64
    V[13] ^= t >> 64

    if isLastBlock:
        V[14] ^= 0xFFFFFFFFFFFFFFFF
    for i in range(0, 11):
        for j in range(0, 15):
            s[j] = sigma[i % 10][j]

        V = blake2b_mix(V, 0, 4,  8, 12, chunk[s[0]], chunk[s[1]])
        V = blake2b_mix(V, 1, 5,  9, 13, chunk[s[2]], chunk[s[3]])
        V = blake2b_mix(V, 2, 6, 10, 14, chunk[s[4]], chunk[s[5]])
        V = blake2b_mix(V, 3, 7, 11, 15, chunk[s[6]], chunk[s[7]])
        V = blake2b_mix(V, 0, 5, 10, 15, chunk[s[8]], chunk[s[9]])
        V = blake2b_mix(V, 1, 6, 11, 12, chunk[s[10]], chunk[s[11]])
        V = blake2b_mix(V, 2, 7,  8, 13, chunk[s[12]], chunk[s[13]])
        V = blake2b_mix(V, 3, 4,  9, 14, chunk[s[14]], chunk[s[15]])

    for i in range(0, 7):
        h[i] = h[i] ^ V[i] ^ V[i+8]

    return h

def blake2b_hash(m, input_size, key_size, hash_size):
    h = IV[:]
    final_hash = []
    m_block = []
    nb_block = int(math.ceil(key_size / 128) + math.ceil(input_size / 128))
    for i in range(0, nb_block - 2, 16):
        m_block = m[i:i + 15]

        if nb_block > 1:
            for i in range(0, nb_block - 2):
                h = blake2b_compress(h, m_block, (i + 1) * 128, False)
    m_block = m[len(m_block):len(m_block) + 15]
    if key_size == 0:
        h = blake2b_compress(h, m_block, 11, True)
    else:
        h = blake2b_compress(h, m_block, 11 + input_size, True)

    for i in range(0, hash_size - 1):
        final_hash[i] = (h[i >> 3] >> (8 * (i & 7))) & 0xFF

    return final_hash
'''


# Generate keys (public/private)
def gen_keys():
    print "Début de la génération des clés..."
    print "Traitement en cours..."
    # find large Sophie Germain prime (safe prime)
    loop = True
    while loop:
        q = largePrime(512)
        if isPrime(q):
            p = 2 * q + 1
            if isPrime(p):
                loop = False

    # find g1 and g2
    loop = True
    while loop:
        g1, g2 = random.randint(2, p - 1), random.randint(2, p - 1)
        if pow(g1, (p - 1) / q) % p != 1:
            g1 = pow(g1, (p - 1) / q) % p
        if pow(g1, (p - 1) / q) % p != 1:
            g2 = pow(g2, (p - 1) / q) % p
        if g1 != g2:
            loop = False

    # generate x1, x2, y1, y2 and w (public key)
    x1, x2, y1, y2, w = random.randint(2, p - 1), random.randint(2, p - 1), random.randint(2, p - 1), random.randint(2,
                                                                                                                     p - 1), random.randint(
        2, p - 1)

    # compute X, Y and W (private key)
    X = (powmod(g1, x1, p) * powmod(g2, x2, p)) % p
    Y = (powmod(g1, y1, p) * powmod(g2, y2, p)) % p
    W = powmod(g1, w, p)

    # writing public and private keys into files
    print "Écriture de la clé publique dans le fichier 'key.pub'..."
    f = open("key.pub", "w")
    f.write("==========PUBLIC KEY==========\n")
    f.write("p:" + str(p) + "\n")
    f.write("g1:" + str(g1) + "\n")
    f.write("g2:" + str(g2) + "\n")
    f.write("X:" + str(X) + "\n")
    f.write("Y:" + str(Y) + "\n")
    f.write("W:" + str(W) + "\n")
    f.write("==========END==========")
    print "Écriture terminée."
    f.close()
    print "Écriture de la clé privée dans le fichier 'key.priv'"
    f = open("key.priv", "w")
    f.write("==========PRIVATE KEY==========\n")
    f.write("x1:" + str(x1) + "\n")
    f.write("x2:" + str(x2) + "\n")
    f.write("y1:" + str(y1) + "\n")
    f.write("y2:" + str(y2) + "\n")
    f.write("w:" + str(w) + "\n")
    f.write("p:" + str(p) + "\n")
    f.write("==========END==========")
    print "Écriture terminée."
    f.close()
    print "Génération des clés terminées (enfin !), passage aux choses sérieuses ^_^"


# Encryption
def encrypt():
    with open(raw_input("Saisir le nom du fichier de la clé publique (ou le chemin direct) : "), 'rU') as pub:
        temp = pub.readlines()
        p = int(temp[1].split(":")[1])
        g1 = int(temp[2].split(":")[1])
        g2 = int(temp[3].split(":")[1])
        X = int(temp[4].split(":")[1])
        Y = int(temp[5].split(":")[1])
        W = int(temp[6].split(":")[1])

        m = lectureFichier()
        n = len(m)

        print "Écriture des informations du message chiffré dans le fichier 'message.enc'"
        f = open("message.enc", "w")
        f.write("==========ENCRYPTED MESSAGE==========\n")
        f.write("n:" + str(n) + "\n")
        for i in range(0, n):
            b = random.randint(2, p - 1)
            b1 = powmod(g1, b, p)
            b2 = powmod(g2, b, p)
            c = (powmod(W, b, p) * int(m[i], 2)) % p

            # blake2b hash computation
            # b1_hash = blake2b_hash(b1, sys.getsizeof(b1), 0, 512)
            # b2_hash = blake2b_hash(b2, sys.getsizeof(b2), 0, 512)
            # c_hash = blake2b_hash(c, sys.getsizeof(c), 0, 512)
            # beta = b1_hash + b2_hash + c_hash

            # sha_256 hashlib version
            # b1_hash = hashlib.sha_256(str(b1)).hexdigest()
            # b2_hash = hashlib.sha_256(str(b2)).hexdigest()
            # c_hash = hashlib.sha_256(str(c)).hexdigest()
            # beta = b1_hash + b2_hash + c_hash
            # beta2 = int(beta, 16)

            # sha256 hash computation
            b1_hash = sha_256(str(b1))
            b2_hash = sha_256(str(b2))
            c_hash = sha_256(str(c))
            beta = b1_hash + b2_hash + c_hash
            v = (powmod(X, b, p) * powmod(Y, b * int(beta, 16), p)) % p

            f.write("=====BLOCK " + str(i + 1) + "=====\n")
            f.write("b1:" + str(b1) + "\n")
            f.write("b2:" + str(b2) + "\n")
            f.write("c:" + str(c) + "\n")
            f.write("v:" + str(v) + "\n")
            f.write("=====END BLOCK=====\n")
        f.write("==========END FILE==========\n")
        f.close()
        pub.close()
        print "Écriture terminée, gardez bien ce fichier au chaud pour pouvoir le déchiffrer..."


# Decryption
def decrypt():
    with open(raw_input("Saisir le nom du fichier de la clé privée (ou le chemin direct) : "), 'rU') as priv:
        temp = priv.readlines()
        x1 = int(temp[1].split(":")[1])
        x2 = int(temp[2].split(":")[1])
        y1 = int(temp[3].split(":")[1])
        y2 = int(temp[4].split(":")[1])
        w = int(temp[5].split(":")[1])
        p = int(temp[6].split(":")[1])
    with open(raw_input("Saisir le nom du fichier à déchiffrer (ou le chemin direct) : "), 'rU') as chiffre:
        temp = chiffre.readlines()
        n = int(temp[1].split(":")[1])
        ind_l = 3
        f = open("message.dec", "w")
        f.write("==========DECRYPTED MESSAGE==========\n")
        for i in range(0, n):
            b1 = int(temp[ind_l].split(":")[1])
            ind_l += 1
            b2 = int(temp[ind_l].split(":")[1])
            ind_l += 1
            c = int(temp[ind_l].split(":")[1])
            ind_l += 1
            v = int(temp[ind_l].split(":")[1])

            # compute hash
            b1_hash = sha_256(str(b1))
            b2_hash = sha_256(str(b2))
            c_hash = sha_256(str(c))
            beta = b1_hash + b2_hash + c_hash

            v2 = (powmod(b1, x1, p) * powmod(b2, x2, p) * powmod(powmod(b1, y1, p) * powmod(b2, y2, p), int(beta, 16),
                                                                 p)) % p

            # check v and v2
            if v == v2:
                print "Vérification réussie, déchiffrement du bloc " + str(i + 1) + " en cours..."
                m = (modinv(powmod(b1, w, p), p) * c) % p
                m = hex(m)[2:-1].decode("hex")
                f.write(str(m))
            ind_l += 3
        f.write("\n==========END==========")
        f.close()
        priv.close()
        chiffre.close()
        print "Déchiffrement terminé, vous pouvez trouver le résultat dans le fichier 'message.dec'."


# Project main menu
def print_menu():
    print "Bienvenue ! Vous venez d'entrer dans un nouveau monde, celui de la cryptographie ! 'whouaaa'"
    print "Ce petit script vous permettra d'utiliser 2 chiffrements et une fonction de hashage."
    print "Son fonctionnement est très simple... Dans le menu suivant, il vous suffit de choisir la fonction désirée et de se laisser guider... Bon voyage !\n"
    print "<" + 5 * "-=" + "GS15 PROJECT / MENU" + 5 * "=-" + ">"
    print "->1<- Chiffrement symétrique ThreeFish"
    print "->2<- Chiffrement de Cramer-Shoup"
    print "->3<- Hash d'un message"
    print "->4<- Déchiffrement symétrique ThreeFish"
    print "->5<- Déchiffrement de Cramer-Shoup"
    print "->6<- Vérification d'un hash"
    print "->7<- Exit..."
    print "<-=" + 9 * "-=" + 9 * "=-" + "=->"


loop = True
while loop:
    print_menu()
    choix = input("\nSaisir le numéro de la fonction choisie [1-7] : ")

    if choix == 1:
        print " -> Chiffrement symétrique ThreeFish choisi, suivez le guide ><(((> ..."
        # fonction ThreeFish en mode chiffrement
    elif choix == 2:
        print " -> Chiffrement de Cramer-Shoup choisi, ..."
        gen_keys()
        encrypt()
    elif choix == 3:
        print " -> Hash d'un message (ou d'un fichier) choisi, ..."
        tmp = raw_input("Saisir votre message : ")
        msg_h = sha_256(tmp)
        print "Le hash du message est : " + tmp
    elif choix == 4:
        " -> Déchiffrement symétrique ThreeFish choisi, le guide revient sur ses pas <(((>< ..."
        # fonction ThreeFish en mode déchiffrement
    elif choix == 5:
        print " -> Déchiffrement de Cramer-Shoup choisi, ..."
        decrypt()
    elif choix == 6:
        print " -> Vérification d'un hash choisi, ..."
        # fonction de hashage
    elif choix == 7:
        print " Vous avez choisi de partir, c'est bien dommage..."
        loop = False
    else:
        raw_input(
            "---ERROR--ERROR--ERROR---\nCette option n'existe pas, veuillez appuyer sur une touche pour continuer...")
