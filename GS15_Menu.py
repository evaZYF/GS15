# coding: utf-8
import os
import sys
import random
import hashlib
from __builtin__ import pow as powmod

def print_menu():
    print ""
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

def genererCles(t0, t1, cleKString, tailleBlocs):
    C = "0001101111010001000110111101101010101001111111000001101000100010"
    tweaks = []
    t0 = t0
    t1 = t1
    t2 = ""
    cleKString = cleKString

    #CAS OU L'ON GENERE TOUT
    if (t0 == ""):
        for i in range(0, 64, 1):
            a = random.randint(0, 1)
            t0 = str(t0)+str(a)
            b = random.randint(0, 1)
            t1 = str(t1)+str(b)

    t2 = bin(int(t0, 2) ^ int(t1, 2))[2:].zfill(64)
    tweaks.append(bin(int(t0, 2))[2:].zfill(64))
    tweaks.append(bin(int(t1, 2))[2:].zfill(64))
    tweaks.append(t2)

    print("========================================================================================================================")
    print("ELEMENTS À CONSERVER : =================================================================================================")
    print("========================================================================================================================")
    for i in range(len(tweaks)):
        print "T" + str(i) + " = " + str(tweaks[i])

    #Génération cleK
    cleK = []
    if cleKString == "":
        for i in range(0, tailleBlocs/64, 1):
            a = random.randint(0, 1)
            cleK.append(str(a))
            for j in range(0, 63, 1):
                a = random.randint(0, 1)
                cleK[i] = str(cleK[i]) + str(a)
    else:
        for i in range(0, tailleBlocs/64, 1):
            cleK.append(cleKString[(63*i)+i])
            for j in range(1, 64, 1):
                cleK[i] = cleK[i]+cleKString[(63*i)+i+j]

    kN = "0"
    for i in range(len(cleK)):
        kN = int(str(kN), 10) ^ int(cleK[i], 2)
    kN = int(str(kN), 10) ^ int(C, 2)

    cleK.append(bin(kN)[2:].zfill(64))

    print("Clé finale : "),
    for i in range(len(cleK)):
        sys.stdout.write(cleK[i])
    print ""
    print "---"

    N = tailleBlocs/64
    tableauClesDeTournee = []

    for compteurI in range(0, 20, 1):
        cleDeTournee = []
        compteurN = 0

        #Pour le bloc n inclus entre {0, N-4}
        while compteurN <= N-4:
            cleDeTournee.append(str(cleK[(compteurI + compteurN) % (N + 1)]))
            compteurN += 1

        #Pour le bloc n  = N-3
        resultatTemporel = bin(int(tweaks[compteurI%3], 2) + int(cleK[(compteurI+compteurN) % (N+1)], 2))
        if(int(resultatTemporel, 2) >= 2**64):
            cleDeTournee.append(bin(int(resultatTemporel, 2) - 2**64)[2:].zfill(64))
        else:
            cleDeTournee.append(bin(int(resultatTemporel, 2))[2:].zfill(64))

        #Pour le bloc n = N-2
        resultatTemporel = bin(int(tweaks[(compteurI+1)%3], 2) + int(cleK[(compteurI+compteurN) % (N+1)], 2))
        if(int(resultatTemporel, 2) >= 2**64):
            cleDeTournee.append(bin(int(resultatTemporel, 2) - 2**64)[2:].zfill(64))
        else:
            cleDeTournee.append(bin(int(resultatTemporel, 2))[2:].zfill(64))

        #Pour le bloc n = N-1
        resultatTemporel = bin(int(str(compteurI), 10) + int(cleK[(compteurI+compteurN) % (N+1)], 2))
        if(int(resultatTemporel, 2) >= 2**64):
            cleDeTournee.append(bin(int(resultatTemporel, 2) - 2**64)[2:].zfill(64))
        else:
            cleDeTournee.append(bin(int(resultatTemporel, 2))[2:].zfill(64))

        tableauClesDeTournee.append(cleDeTournee)

    return tableauClesDeTournee

def chiffrementThreeFish(tableauClesDeTournee, tableauMotsFichier, tailleBlocs):

    tableauMotsFichierMixe = []
    tableauMotsFichierPermutation = []

    print("Taille dernier bloc = "+str(len(tableauMotsFichier[len(tableauMotsFichier)-1])))
    print("========================================================================================================================")
    print("========================================================================================================================")
    print("========================================================================================================================")

    for i in range(len(tableauMotsFichier)):
        tableauMotsFichierMixe.append(bin(int(tableauMotsFichier[i], 2) ^ int(tableauClesDeTournee[0][i%(tailleBlocs/64)], 2))[2:].zfill(64))
    for y in range(1, 20, 1):

        for z in range(0, 4, 1):

            #MIXAGE
            for i in range(0, len(tableauMotsFichier), 2):
                if i != len(tableauMotsFichier)-1:
                    resultatTemporel = bin(int(tableauMotsFichierMixe[i], 2) + int(tableauMotsFichierMixe[i+1], 2))
                    if(int(resultatTemporel, 2) >= 2**64):
                        m1primme = bin(int(resultatTemporel,2) - 2**64)
                        tableauMotsFichierPermutation.append(bin(int(m1primme, 2))[2:].zfill(64))
                    else:
                        m1primme = bin(int(resultatTemporel,2))
                        tableauMotsFichierPermutation.append(bin(int(m1primme, 2))[2:].zfill(64))

                    #TOURNÉE
                    m2R = tableauMotsFichierMixe[i+1]
                    for j in range(0, 48, 1):
                        m2Rchar = m2R[0]
                        m2R = m2R[1:] + m2Rchar

                    m2prime = bin(int(m1primme, 2) ^ int(m2R, 2))
                    tableauMotsFichierPermutation.append(bin(int(m2prime, 2))[2:].zfill(64))
                else:
                    tableauMotsFichierPermutation.append(bin(int(tableauMotsFichierMixe[i], 2))[2:].zfill(64))

            #PERMUTATION
            tableauMotsFichierMixe = tableauMotsFichierPermutation[::-1]

            tableauMotsFichierPermutation = []

        tableauMotsFichierMixe2 = []
        for k in range(len(tableauMotsFichier)):
            tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierMixe[k], 2) ^ int(tableauClesDeTournee[y][k%(tailleBlocs/64)], 2))[2:].zfill(64))

        tableauMotsFichierMixe = tableauMotsFichierMixe2

    print("Hash fichier chiffré : "+str(hashlib.sha224(str(tableauMotsFichierMixe)).hexdigest()))

    return tableauMotsFichierMixe

def dechiffrementThreeFish(tableauClesDeTournee, tableauMotsFichier, tailleBlocs, tailleDernierBloc):

    tableauMotsFichierMixe = []
    tableauMotsFichierPermutation = []

    #Première permutation
    for i in range(len(tableauMotsFichier)):
        tableauMotsFichierPermutation.append(bin(int(tableauMotsFichier[i], 2) ^ int(tableauClesDeTournee[19][i%(tailleBlocs/64)], 2))[2:].zfill(64))

    for y in range(18, -1, -1):

        for z in range(0, 4, 1):

            #PERMUTATION
            tableauMotsFichierMixe = tableauMotsFichierPermutation[::-1]

            tableauMotsFichierPermutation = []

            for i in range(0, len(tableauMotsFichier), 2):
                if i != len(tableauMotsFichier)-1:
                    m2R = bin(int(tableauMotsFichierMixe[i], 2) ^ int(tableauMotsFichierMixe[i+1], 2))[2:].zfill(64)

                    #TOURNÉE INVERSE
                    for j in range(0, 48, 1):
                        m2Rchar = m2R[63]
                        m2R = m2Rchar + m2R[:63]

                    m2 = m2R
                    temp = int(tableauMotsFichierMixe[i], 2) - int(m2, 2)
                    if temp < 0:
                        m1 = temp + 2**64
                    else:
                        m1 = temp

                    tableauMotsFichierPermutation.append(bin(m1)[2:].zfill(64))
                    tableauMotsFichierPermutation.append(m2)
                else:
                    tableauMotsFichierPermutation.append(tableauMotsFichierMixe[i])

        tableauMotsFichierMixe2 = []

        if y == 0:
            for i in range(len(tableauMotsFichier)):
                if i != len(tableauMotsFichier)-1:
                    tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierPermutation[i], 2) ^ int(tableauClesDeTournee[y][i%(tailleBlocs/64)], 2))[2:].zfill(64))

                else:
                    tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierPermutation[i], 2) ^ int(tableauClesDeTournee[y][i%(tailleBlocs/64)], 2))[2:].zfill(int(tailleDernierBloc)))

            tableauMotsFichierPermutation = tableauMotsFichierMixe2
        else:
            for i in range(len(tableauMotsFichier)):
                tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierPermutation[i], 2) ^ int(tableauClesDeTournee[y][i%(tailleBlocs/64)], 2))[2:].zfill(64))
            tableauMotsFichierPermutation = tableauMotsFichierMixe2

    tableauMotsFichierMixe2 = []
    '''
    for i in range(len(tableauMotsFichier)):
        tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierPermutation[i], 2) ^ int(tableauClesDeTournee[0][i%(tailleBlocs/64)], 2))[2:].zfill(64))
    print("Hash fichier mixe2 : "+str(hashlib.sha224(str(tableauMotsFichierMixe2)).hexdigest()))

    tableauMotsFichierPermutation = tableauMotsFichierMixe2
    
    tableauMotsFichierMixe2 = []

    for i in range(len(tableauMotsFichier)):
        if i != len(tableauMotsFichier)-1:
            print "wololo "+str(i)
            tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierPermutation[i], 2) ^ int(tableauClesDeTournee[0][i%(tailleBlocs/64)], 2))[2:].zfill(64))
            print("Hash fichier mixe2 : "+str(hashlib.sha224(str(tableauMotsFichierMixe2[i])).hexdigest()))

        else:
            print "WAHLLAH "+str(i)
            tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierPermutation[i], 2) ^ int(tableauClesDeTournee[0][i%(tailleBlocs/64)], 2))[2:])
            print("Hash fichier mixe2 : "+str(hashlib.sha224(str(tableauMotsFichierMixe2[i])).hexdigest()))

    tableauMotsFichierPermutation = tableauMotsFichierMixe2
    '''

    print("Hash fichier déchiffré : "+str(hashlib.sha224(str(tableauMotsFichierPermutation)).hexdigest()))

    return tableauMotsFichierPermutation

def lectureFichier(path):

    motsFichier = []
    with open(os.path.expanduser(str(path)), "rb") as file:
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

    print("Hash fichier ouvert : "+str(hashlib.sha224(str(motsFichier)).hexdigest()))

    return motsFichier

def ecritureFichier(motsFichier, path):

    f = open(os.path.expanduser(path), "wb")

    for i in range(len(motsFichier)):
        for j in range(0, 8, 1):

            if(motsFichier[i][j*8:(j*8)+8] != ""):
                byte = format(int(motsFichier[i][j*8:(j*8)+8], 2), 'x')

                if len(byte) % 2 != 0:
                    byte = byte.zfill(len(byte)+1)
                byte = byte.strip().decode('hex')

                f.write(byte)
            else:
                f.write("")
    f.close()

    '''
    motsFichier = []
    
    with open(os.path.expanduser(str(path)), "rb") as file2:
        compteur = 0
        while True:
            byte = file2.read(1)
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
    file2.close()

    #print("FICHIER GENERE")
    #print(len(motsFichier))
    #for i in range(len(motsFichier)):
        #sys.stdout.write(motsFichier[i])
    #    print(motsFichier[i])
    #print("")
    #print("Hash fichier chiffré généré : "+str(hashlib.sha224(str(motsFichier)).hexdigest()))
    '''

def mainThreeFishChiffrement():
    print " -> Chiffrement symétrique ThreeFish ><(((º> ..."
    print "Pour effectuer le chiffrement, il nous faut une taille de blocs pour effectuer ce chiffrement"
    taille = True
    while taille:
        tailleBlocs = input("Vous pouvez choisir entre 256, 512 ou 1024 bits : ")
        if tailleBlocs == 256:
            print "256 blocs choisis"
            taille = False
        elif tailleBlocs == 512:
            print "512 blocs choisis"
            taille = False
        elif tailleBlocs == 1024:
            print("1024 bits choisis")
            taille = False
        else:
            print "Il semblerait que le choix entre 256, 512 ou 1024 ait été trop compliqué, veuillez réessayer"

    reponse = True
    while reponse:
        path = str(raw_input("Path du fichier à chiffrer :  "))
        reponse = False

    reponse = True
    while reponse:
        path2 = str(raw_input("Path vers lequel le fichier chiffré doit être stocké :  "))
        reponse = False

    print "Vous avez choisi des blocs de " + str(tailleBlocs) + " bits"

    tableauChiffre = chiffrementThreeFish(genererCles("", "", "", tailleBlocs), lectureFichier(path), tailleBlocs)

    ecritureFichier(tableauChiffre, path2)

def mainThreeFishDechiffrement():
    print " -> Déchiffrement ThreeFish ><(((º> ..."
    print "Pour effectuer le dechiffrement, il nous faut plusieurs informations"
    reponse = True
    while reponse:
        tailleBlocs = input("Quelle était la taille des blocs utilisée pour chiffrer le fichier ?")
        if tailleBlocs == 256:
            print "256 blocs choisis"
            reponse = False
        elif tailleBlocs == 512:
            print "512 blocs choisis"
            reponse = False
        elif tailleBlocs == 1024:
            print("1024 bits choisis")
            reponse = False
        else:
            print "256, 512, ou 1024 seulement svp"

    reponse = True
    while reponse:
        t0 = str(raw_input("Indiquez t0 :  ").zfill(64))
        reponse = False

    reponse = True
    while reponse:
        t1 = str(raw_input("Indiquez t1 :  "))
        reponse = False

    reponse = True
    while reponse:
        cleString = str(raw_input("Indiquez la clé de chiffrement :"))
        reponse = False

    reponse = True
    while reponse:
        tailleDernierBloc = str(raw_input("Quelle est la taille du dernier bloc ?"))
        reponse = False

    reponse = True
    while reponse:
        path = str(raw_input("Nom du fichier a déchiffrer :"))
        reponse = False

    reponse = True
    while reponse:
        path2 = str(raw_input("Nom du fichier une fois déchiffré : "))
        reponse = False

    tableauDechiffre = dechiffrementThreeFish(genererCles(t0, t1, cleString, tailleBlocs), lectureFichier(path), tailleBlocs, tailleDernierBloc)
    ecritureFichier(tableauDechiffre, path2)

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

    with open(raw_input("Saisir le nom du fichier chiffré : "), 'w') as f:
        print "Écriture des informations du message à chiffrer en cours, veuillez patienter..."
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
    with open(raw_input("Saisir le nom du fichier final : "), 'w') as f:
        # f.write("==========DECRYPTED MESSAGE==========\n")
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
                if len(hex(m)[2:-1]) % 2 != 0:
                    m = hex(m)[2:-1].zfill(len(hex(m)[2:-1]) + 1)
                    m = m.decode("hex")
                    f.write(str(m))
                else:
                    m = hex(m)[2:-1].decode("hex")
                    f.write(str(m))
                ind_l += 3
        # f.write("\n==========END==========")
        f.close()
        priv.close()
        chiffre.close()
        print "Déchiffrement terminé, vous pouvez trouver le résultat dans le fichier 'message.dec'."

loop = True
while loop:
    print_menu()
    choix = input("\nSaisir le numéro de la fonction choisie [1-7] : ")

    if choix == 1:

        mainThreeFishChiffrement()

    elif choix == 2:
        print " -> Chiffrement de Cramer-Shoup choisi, ..."
        gen_keys()
        encrypt()

    elif choix == 3:
        print " -> Hash d'un message choisi, ..."
        tmp = raw_input("Saisir votre message : ")
        msg_h = sha_256(tmp)
        print "Le hash du message est : " + tmp

    elif choix == 4:

        mainThreeFishDechiffrement()

    elif choix == 5:
        print " -> Déchiffrement de Cramer-Shoup choisi, ..."
        decrypt()

    elif choix == 6:
        print " -> Vérification d'un hash choisi, ..."

    elif choix == 7:
        print " Vous avez choisi de partir, c'est bien dommage..."
        loop = False
    else:
        raw_input(
            "---ERROR--ERROR--ERROR---\nCette option n'existe pas, veuillez appuyer sur une touche pour continuer...")
