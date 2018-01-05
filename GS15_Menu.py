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
            a = random.randint(0,1)
            t0 = str(t0)+str(a)
            b = random.randint(0,1)
            t1 = str(t1)+str(b)

    t2 = int(t0, 2) ^ int(t1, 2)
    tweaks.append(t0)
    tweaks.append(t1)
    tweaks.append(bin(t2)[2:].zfill(64))
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
        print len(cleK)

        print("--")
        for i in range(len(cleK)):
            print(cleK[i])

    kN = "0"
    for i in range(len(cleK)):
        kN = int(str(kN), 10) ^ int(cleK[i], 2)
    kN = int(str(kN), 10) ^ int(C, 2)
    print("k"+str(tailleBlocs/64)+" = " + str(bin(kN)[2:].zfill(64)))

    cleK.append(bin(kN)[2:].zfill(64))

    print("Clé finale (A CONSERVER) : "),
    for i in range(len(cleK)):
        #print cleK[i]
        sys.stdout.write(cleK[i])
    print ""

    N = tailleBlocs/64
    tableauClesDeTournee = []
    for compteurI in range(0, 20, 1):
        cleDeTournee = []
        #print compteurI
        compteurN = 0
        #Pour le bloc n inclus entre {0, N-4}
        while compteurN <= N-4:
            cleDeTournee.append(str(cleK[(compteurI + compteurN) % (N + 1)]))
            compteurN += 1
        #Pour le bloc n  = N-3
        resultatTemporel = bin(int(tweaks[compteurI%3], 2) + int(cleK[(compteurI+compteurN) % (N+1)], 2))
        if len(resultatTemporel) <= 66:
            cleDeTournee.append(bin(int(resultatTemporel,2))[2:].zfill(64))
        elif len(resultatTemporel) > 66:
            cleDeTournee.append(bin(int(resultatTemporel,2))[len(resultatTemporel)-64:].zfill(64))

        #Pour le bloc n = N-2
        resultatTemporel = bin(int(tweaks[(compteurI+1)%3], 2) + int(cleK[(compteurI+compteurN) % (N+1)], 2))
        if len(resultatTemporel) <= 66:
            cleDeTournee.append(bin(int(resultatTemporel,2))[2:].zfill(64))
        elif len(resultatTemporel) > 66:
            cleDeTournee.append(bin(int(resultatTemporel,2))[len(resultatTemporel)-64:].zfill(64))

        #Pour le bloc n = N-1
        resultatTemporel = bin(int(str(compteurI), 10) + int(cleK[(compteurI+compteurN) % (N+1)], 2))
        if len(resultatTemporel) <= 66:
            cleDeTournee.append(bin(int(resultatTemporel,2))[2:].zfill(64))
        elif len(resultatTemporel) > 66:
            cleDeTournee.append(bin(int(resultatTemporel,2))[len(resultatTemporel)-64:].zfill(64))

        tableauClesDeTournee.append(cleDeTournee)

    #for i in range(len(tableauClesDeTournee)):
    #    print("CLE " + str(i) + " : ")
    #    for j in range(len(tableauClesDeTournee[i])):
    #        print tableauClesDeTournee[i][j]

    print("Hash clés de tournée :"),
    print(hashlib.sha224(str(tableauClesDeTournee)).hexdigest())

    return tableauClesDeTournee

def chiffrementThreeFish(tableauClesDeTournee, tableauMotsFichier, tailleBlocs):
    #print("===================================CLEFS DE TOURNEE==================================")
    #for i in range(len(tableauClesDeTournee)):
    #    print("CLE " + str(i) + " : ")
    #    for j in range(len(tableauClesDeTournee[i])):
    #        print tableauClesDeTournee[i][j]
    #print("=====================================MOTS FICHIER====================================")
    #for i in range(len(tableauMotsFichier)):
    #    print tableauMotsFichier[i]

    tableauMotsFichierMixe = []
    tableauMotsFichierPermutation = []

    # Mise en place de blocs de taille adécuate
    '''
    for i in range(0, 20, 1):
        cledeTournee = ""
        for j in range(0, tailleBlocs/64, 1):
            cledeTournee = cledeTournee + tableauClesDeTournee[i][j]
        tableauClesDeTourneeTailleBloc.append(cledeTournee)
        print("Appended"+str(i))
    
    print("=========TABLEAU CLES DE TOURNEE==========")
    for i in range(len(tableauClesDeTourneeTailleBloc)):
        print(tableauClesDeTourneeTailleBloc[i])

    compteurPosition = 0
    print(len(tableauMotsFichier))
    for j in range(0, int((float(len(tableauMotsFichier))*64)/float(tailleBlocs))):
        motTailleBloc = ""
        for i in range(0, tailleBlocs/64, 1):
            motTailleBloc += tableauMotsFichier[compteurPosition]
            compteurPosition += 1
            print("CompteurPosition : "+ str(compteurPosition))
        tableauMotsFichiertailleBloc.append(motTailleBloc)
        print "J : "+str(j)
    '''
    #print("=========TABLEAU FICHIER==========")
    #for i in range(len(tableauMotsFichiertailleBloc)):
    #    print(tableauMotsFichiertailleBloc[i])

    #print("=========Tableau premiere tournée==========")
    for i in range(len(tableauMotsFichier)):
        tableauMotsFichierMixe.append(bin(int(tableauMotsFichier[i], 2) ^ int(tableauClesDeTournee[0][i%(tailleBlocs/64)], 2))[2:].zfill(64))
    #print("LENGTH ORIGINAL: "+str(len(tableauMotsFichier)))
    #for i in range(len(tableauMotsFichierMixe)):
    #    print(tableauMotsFichierMixe[i])

    #print len(tableauMotsFichier)
    #print len(tableauMotsFichierMixe)
    for y in range(0, 20, 1):
        for z in range(0, 4, 1):
            #MIXAGE

            for i in range(0, len(tableauMotsFichier), 2):
                if i != len(tableauMotsFichier)-1:
                    resultatTemporel = bin(int(tableauMotsFichierMixe[i], 2) + int(tableauMotsFichierMixe[i+1], 2))[2:]
                    #print(len(resultatTemporel))
                    if len(resultatTemporel) <= 64:
                        m1primme = bin(int(resultatTemporel, 2))[2:].zfill(64)
                        tableauMotsFichierPermutation.append(m1primme)
                    elif len(resultatTemporel) > 64:
                        m1primme = bin(int(resultatTemporel, 2))[3:].zfill(64)
                        tableauMotsFichierPermutation.append(m1primme)
                    #print(i)

                    #TOURNÉE
                    m2R = tableauMotsFichierMixe[i+1]
                    for j in range(0, 48, 1):
                        m2Rchar = m2R[0]
                        m2R = m2R[1:] + m2Rchar

                    m2prime = bin(int(m1primme, 2) ^ int(m2R, 2))[2:].zfill(64)
                    tableauMotsFichierPermutation.append(m2prime)
                else:
                    tableauMotsFichierPermutation.append(bin(int(tableauMotsFichierMixe[i], 2))[2:].zfill(64))
                #print(tableauMotsFichierPermutation[i])
                #print(tableauMotsFichierPermutation[i+1])

            #PERMUTATION
            tableauMotsFichierMixe = tableauMotsFichierPermutation[::-1]
            tableauMotsFichierPermutation = []

        tableauMotsFichierMixe2 = []
        for i in range(len(tableauMotsFichier)):
            tableauMotsFichierMixe2.append(bin(int(tableauMotsFichierMixe[i], 2) ^ int(tableauClesDeTournee[y][i%(tailleBlocs/64)], 2))[2:].zfill(64))

        #print("USED KEY Nº"+str(y)+": ")
        #for i in range(len(tableauClesDeTournee[y])):
        #    print tableauClesDeTournee[y][i]

        tableauMotsFichierMixe = tableauMotsFichierMixe2
    print("Hash fichier chiffré : "+str(hashlib.sha224(str(tableauMotsFichierMixe)).hexdigest()))
    #print("LENGTH MIXE: "+str(len(tableauMotsFichierMixe)))

    return tableauMotsFichierMixe
    #print("=========Tableau dernière tournée==========")
    #print("LENGTH initiale: "+str(len(tableauMotsFichier)) + " LENGTH finale: "+str(len(tableauMotsFichier)))
    #for i in range(len(tableauMotsFichierMixe)):
    #    print tableauMotsFichierMixe[i]

    # Addition clé de tournée par mot
    #for i in range(len(tableauMotsFichier)):
    #    for j in range(0, tailleBlocs/64, 1):
    #        print str(bin(int(tableauMotsFichier[i], 2) ^ int(tableauClesDeTournee[i][j], 2))[2:].zfill(64))
    #        tableauMotsFichierMixe.append(bin(int(tableauMotsFichier[i], 2) ^ int(tableauClesDeTournee[i][j], 2))[2:].zfill(64))

    # Addition clé de tournée par bloc
    #for i in range(len(tableauMotsFichiertailleBloc)):
    #    tableauBlocsFichierMixe.append(bin(int(tableauMotsFichiertailleBloc[i], 2) ^ int(tableauClesDeTourneeTailleBloc[i], 2))[2:].zfill(tailleBlocs))
    #    print tableauBlocsFichierMixe[i]

def dechiffrementThreeFish(tableauClesDeTournee, tableauMotsFichier, tailleBlocs):
    print("hello")


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

    print("Hash fichier original : "+str(hashlib.sha224(str(motsFichier)).hexdigest()))

    return motsFichier

def ecritureFichier(path):
    f = open(os.path.expanduser(str(path)), "wb")
    print "WRITE OUT"

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

    print "Vous avez choisi des blocs de " + str(tailleBlocs) + " bits"

    tableaufichierChiffre = chiffrementThreeFish(genererCles("", "", "", tailleBlocs), lectureFichier("~/Desktop/myfile.rtf"), tailleBlocs)

    mainThreeFishDechiffrement(tableaufichierChiffre)

def mainThreeFishDechiffrement(tableaufichierChiffre):
    print " -> Déchiffrement ThreeFish ><(((º> ..."
    print "Pour effectuer le dechiffrement, il nous faut plusieurs informations"
    reponse = True
    while reponse:
        tailleBlocs = input("Quelle était la taille des blocs?")
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
        t0 = str(raw_input("Indiquez T0 :  ").zfill(64))
        reponse = False

    reponse = True
    while reponse:
        t1 = str(raw_input("Indiquez T1 :  "))
        reponse = False

    reponse = True
    while reponse:
        cleString = str(raw_input("Quelle est la clé de chiffrement ?"))
        reponse = False

    dechiffrementThreeFish(genererCles(t0, t1, cleString, tailleBlocs), tableaufichierChiffre, tailleBlocs)


loop = True

while loop:
    print_menu()
    choix = input("\nSaisir le numéro de la fonction choisie [1-7] : ")

    if choix == 1:
        '''
        a='0010001010101101010101011010101010110101010101101010101011010101'
        b='0101011101011010101001001010010110100010101010101101111101001010'
        print(len(a))
        10001010101101010101011010101010110101010101101010101011010101
        resultatTemporel = bin(int(a, 2) + int(b, 2))
        print(len(resultatTemporel))
        print str(resultatTemporel)
        resultatTemporel = str(resultatTemporel[3:].zfill(64))
        print resultatTemporel
        print "=========="
        
        m2R = "00001111"
        for j in range(0, 6, 1):
            m2Rchar = m2R[0]
            m2R = m2R[1:] + m2Rchar

        print(m2R)
        
        testarray =[1, 2]
        print(hashlib.sha224(str(testarray)).hexdigest())
        '''
        mainThreeFishChiffrement()
        #genererCles("0101001111010010001111110001100110000001010111111000001101001111", "0100011101001110001011010010000100110011101000000011000101100110", "10010111100101000111110111110001011111100011110000101000101010100001100110101110101000100101001011111100101011011110010010100001110010011011010111001001100000010011010110010011001001001001010110111101011101001001101010110110101101011000011010001011111001011110000100101010100101110100111010101011011110000111100101011001", 256)

    elif choix == 2:
        print " -> Chiffrement de Cramer-Shoup choisi, ..."
        ## fonction Cramer-Shoup en mode chiffrement
    elif choix == 3:
        print " -> Hash d'un message choisi, ..."
        ## fonction da hashage
    elif choix == 4:
        " -> Déchiffrement symétrique ThreeFish choisi, le guide revient sur ses pas <(((>< ..."

        ## fonction ThreeFish en mode déchiffrement
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
