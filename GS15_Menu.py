
# coding: utf-8
import os
def print_menu():
    print "Bienvenue ! Vous venez d'entrer dans un nouveau monde, celui de la cryptographie ! 'whouaaa'"
    print "Ce petit script vous permettra d'utiliser 2 chiffrements et une fonction de hashage."
    print "Son fonctionnement est très simple... Dans le menu suivant, il vous suffit de choisir la fonction désirée et de se laisser guider... Bon voyage !\n"
    print "<"+5 * "-="+"GS15 PROJECT / MENU"+5 * "=-"+">"
    print "->1<- Chiffrement symétrique ThreeFish"
    print "->2<- Chiffrement de Cramer-Shoup"
    print "->3<- Hash d'un message"
    print "->4<- Déchiffrement symétrique ThreeFish"
    print "->5<- Déchiffrement de Cramer-Shoup"
    print "->6<- Vérification d'un hash"
    print "->7<- Exit..."
    print "<-="+9 * "-="+9 * "=-"+"=->"

loop = True
while loop:
    print_menu()
    choix = input("\nSaisir le numéro de la fonction choisie [1-7] : ")

    if choix==1:
        print " -> Chiffrement symétrique ThreeFish choisi, suivez le guide ><(((º> ..."
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
                print("1024 bits choisis pour ")
                tailleBlocs = False
            else:
                print "Il semblerait que le choix entre 256, 512 ou 1024 ait été trop compliqué, veuillez réessayer"
        print tailleBlocs
        with open(os.path.expanduser("~/Desktop/myfile.rtf"), "rb") as file:
            byte = file.read(1)
            while byte != "":
                # Do stuff with byte.
                byte = file.read(1)
                bits = int(byte) >> 8,
                print bits,

    elif choix==2:
        print " -> Chiffrement de Cramer-Shoup choisi, ..."
        ## fonction Cramer-Shoup en mode chiffrement
    elif choix==3:
        print " -> Hash d'un message choisi, ..."
        ## fonction da hashage
    elif choix==4:
        " -> Déchiffrement symétrique ThreeFish choisi, le guide revient sur ses pas <(((>< ..."
        ## fonction ThreeFish en mode déchiffrement
    elif choix==5:
        print " -> Déchiffrement de Cramer-Shoup choisi, ..."
        ## fonction Cramer-Shoup en mode déchiffrement
    elif choix==6:
        print " -> Vérification d'un hash choisi, ..."
        ## fonction de hashage
    elif choix==7:
        print " Vous avez choisi de partir, c'est bien dommage..."
        loop=False
    else:
        raw_input("---ERROR--ERROR--ERROR---\nCette option n'existe pas, veuillez appuyer sur une touche pour continuer...")






