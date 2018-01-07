# coding: utf-8
import os
import sys
import random
import hashlib
import math

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

loop = True
while loop:
    print_menu()
    choix = input("\nSaisir le numéro de la fonction choisie [1-7] : ")

    if choix == 1:

        mainThreeFishChiffrement()

    elif choix == 2:
        print " -> Chiffrement de Cramer-Shoup choisi, ..."
        ## fonction Cramer-Shoup en mode chiffrement
    elif choix == 3:
        print " -> Hash d'un message choisi, ..."
        ## fonction da hashage
    elif choix == 4:

        mainThreeFishDechiffrement()

    elif choix == 5:
        print " -> Déchiffrement de Cramer-Shoup choisi, ..."
        ## fonction Cramer-Shoup en mode déchiffrement
    elif choix == 6:
        print " -> Vérification d'un hash choisi, ..."
        ## fonction de hashage
    elif choix == 7:
        print " Vous avez choisi de partir, c'est bien dommage..."
        loop = False
    else:
        raw_input(
            "---ERROR--ERROR--ERROR---\nCette option n'existe pas, veuillez appuyer sur une touche pour continuer...")
