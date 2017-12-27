
# coding: utf-8

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
        print " -> Chiffrement symétrique ThreeFish choisi, suivez le guide ><(((> ..."
        ## fonction ThreeFish en mode chiffrement
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






