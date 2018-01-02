# coding: utf-8
import os
import sys
import random

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

def genererCles(tailleBlocs):
    C = "0001101111010001000110111101101010101001111111000001101000100010"
    tweaks = []
    t0 = ""
    t1 = ""
    t2 = ""
    for i in range(0, 64, 1):
        a = random.randint(0,1)
        t0 = str(t0)+str(a)
        b = random.randint(0,1)
        t1 = str(t1)+str(b)
        t2 = int(t0, 2) ^ int(t1, 2)
    print "===================="
    # print("T0 = " + str(t0))
    # print("T1 = " + str(t1))
    # print "T2 = " + str(bin(t2)[2:].zfill(len(t0)))
    tweaks.append(t0)
    tweaks.append(t1)
    tweaks.append(bin(t2)[2:].zfill(64))
    for i in range(len(tweaks)):
        print "T" + str(i) + " = " + str(tweaks[i])
    cleK = []
    for i in range(0, tailleBlocs/64, 1):
        a = random.randint(0, 1)
        cleK.append(str(a))
        for j in range(0, 63, 1):
            a = random.randint(0, 1)
            cleK[i] = str(cleK[i]) + str(a)
    kN = "0"
    for i in range(len(cleK)):
        kN = int(str(kN), 10) ^ int(cleK[i], 2)
    kN = int(str(kN), 10) ^ int(C, 2)
    print("k"+str(tailleBlocs/64)+" = " + str(bin(kN)[2:].zfill(64)))

    print "Clé générée : "
    for i in range(len(cleK)):
        print cleK[i]
        #sys.stdout.write(cleK[i])
    print("")

    cleK.append(bin(kN)[2:].zfill(64))

    print("Clé finale (A CONSERVER) : ")
    for i in range(len(cleK)):
        print cleK[i]
        #sys.stdout.write(cleK[i])
    print ""
    print("====================")
    N = tailleBlocs/64
    tableauClesDeTournee = []
    compteurImodulo = 0
    for compteurI in range(0, 20, 1):
        compteurImodulo = compteurI%(N+1)
        cleDeTournee = []
        #print compteurI
        compteurN = 0
        #Pour le bloc n inclus entre {0, N-4}
        while compteurN <= N-4:
            cleDeTournee.append(str(cleK[(compteurI + compteurN) % (N + 1)]))
            compteurN += 1

        #Pour le bloc n  = N-3
        resultatTemporel = int(tweaks[compteurI%3], 2) ^ int(cleK[(compteurI+compteurN) % (N+1)], 2)
        cleDeTournee.append(bin(resultatTemporel)[2:].zfill(64))

        #Pour le bloc n = N-2
        resultatTemporel = int(tweaks[(compteurI+1)%3], 2) ^ int(cleK[(compteurI+compteurN) % (N+1)], 2)
        cleDeTournee.append(bin(resultatTemporel)[2:].zfill(64))

        #Pour le bloc n = N-1
        resultatTemporel = int(str(compteurI), 10) ^ int(cleK[(compteurI+compteurN) % (N+1)], 2)
        cleDeTournee.append(bin(resultatTemporel)[2:].zfill(64))

        tableauClesDeTournee.append(cleDeTournee)

    for i in range(len(tableauClesDeTournee)):
        print("CLE " + str(i) + " : ")
        for j in range(len(tableauClesDeTournee[i])):
            # sys.stdout.write(tableauClesDeTournee[i][j])
            print tableauClesDeTournee[i][j]
    return tableauClesDeTournee

def chiffrementThreeFish(tableauClesDeTournee, tableauMotsFichier):
    print("=====================================CHIFFREMENT=====================================")
    print("===================================CLEFS DE TOURNEE==================================")
    for i in range(len(tableauClesDeTournee)):
        print("CLE " + str(i) + " : ")
        for j in range(len(tableauClesDeTournee[i])):
            print tableauClesDeTournee[i][j]
    print("=====================================MOTS FICHIER====================================")
    for i in range(len(tableauMotsFichier)):
        print tableauMotsFichier[i]

def lectureFichier():

    motsFichier = []
    with open(os.path.expanduser("~/Desktop/myfile.rtf"), "rb") as file:
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

    return motsFichier

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

    chiffrementThreeFish(genererCles(tailleBlocs), lectureFichier())

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


