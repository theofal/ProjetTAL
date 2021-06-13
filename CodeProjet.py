# -*- coding: utf-8 -*-

import math
import sys
from collections import Counter
from nltk import bigrams, trigrams
import gdocData

# Corpus de reference
textENG2 = open('corpus/en_pud-ud-test.txt', 'r')
textENG = textENG2.read()
textENG2.close()

textESP1 = open('corpus/es_pud-ud-test.txt', 'r')
textESP = textESP1.read()
textESP1.close()

textITA1 = open('corpus/it_pud-ud-test.txt', 'r')
textITA = textITA1.read()
textITA1.close()

textFR2 = open('corpus/fr_pud-ud-test.txt', 'r')
textFR = textFR2.read()
textFR2.close()

# Utile pour la separation du corpus en "separation" (n) caracteres
separation = gdocData.separation
listGdoc = [[separation]]


# Fonction pour l'utilisation du terminal
def fileOpen():
    if len(sys.argv) == 1:
        print("Opération impossible : Il manque des arguments. Référez-vous au fichier README pour plus d'informations"
              " concernant l'utilisation du logiciel.")
        return None

    elif (len(sys.argv) == 2) & sys.argv[1].__contains__(".txt"):
        with open(sys.argv[1], 'r') as file_object:
            text = file_object.read()
        return text

    else:
        text = ""
        for i in range(1, len(sys.argv)):
            text += sys.argv[i]
            text += " "
        return text


# texte à analyser
new_text = fileOpen()


# Crée un dictionnaire d'unigrammes
def unigrammes(texte):
    dico = dict(Counter(sorted(texte)))
    return dico


# Crée un dictionnaire de bigrammes
def bigrammes(text):
    bigramme = Counter(sorted(i for i in bigrams(j for j in text)))
    dict(bigramme)
    return bigramme


# Crée un dictionnaire de trigrammes
def trigrammes(text):  # trigrams analysis
    trigramme = Counter(sorted(i for i in trigrams(j for j in text)))
    dict(trigramme)
    return trigramme


# Decoupe le nouveau texte en phrases de "separation = n" characters
def text_tokenize(texte):
    listephrase = [texte[i:i + separation] for i in range(0, len(texte), separation)]
    print(len(texte))
    return listephrase


# Separation en phrases
# def text_tokenize(texte):
#     nouveautexte = texte.replace(". ", ".")
#     l = nouveautexte.split('.')
#     listephrase = []
#     for e in l:
#         if len(e) != 0:
#             listephrase.append(e)
#     return listephrase


# Non-utilisé dans cette version du code. Transforme un dictionnaire en liste de listes
# Necessaire pour exporter des données sur le Google sheet
def dict_to_array(dict1):
    return [[i, j] for i, j in dict1.items()]


# Non-utilisé dans cette version du code. Transforme une liste de listes en dictionnaire
# Necessaire pour importer des données du Google sheet
def array_to_dict(array):
    return {i: j for [i, j] in array}


# Crée une liste de dictionnaire à partir des n-grammes de chaque phrase
def Dico_phrase(listdephrase, number):
    list_dico = []
    if number == 1:
        for elt in listdephrase:
            list_dico.append(unigrammes(elt))
    elif number == 2:
        for elt in listdephrase:
            list_dico.append(bigrammes(elt))
    elif number == 3:
        for elt in listdephrase:
            list_dico.append(trigrammes(elt))
    return list_dico


# Mesure de similarité entre le dictionnaire de référence et le nouveau dictionnaire
def calcul_cos(old_dict, new_dict):
    numer = 0
    denom1 = 0
    denom2 = 0
    common_key = old_dict.keys() & new_dict.keys()
    # print(common_key)
    for key in common_key:
        numer += old_dict[key] * new_dict[key]
    for key in old_dict.keys():
        denom1 += math.pow(old_dict[key], 2)
    for key in new_dict.keys():
        denom2 += math.pow(new_dict[key], 2)
    denom = math.sqrt(denom1) * math.sqrt(denom2)
    cos_theta = numer / denom
    return cos_theta


# Mesurer la similarité des listes de dicos créées avec les dico de réfécrence
def calcul_cos_listes(old_dict_list, listdedico):
    numer = 0
    denom1 = 0
    denom2 = 0
    list_cos = []
    for i in range(len(listdedico)):
        common_key = old_dict_list.keys() & listdedico[i].keys()
        for key in common_key:
            numer += old_dict_list[key] * listdedico[i][key]
        for key in old_dict_list.keys():
            denom1 += math.pow(old_dict_list[key], 2)
        for key in listdedico[i]:
            denom2 += math.pow(listdedico[i][key], 2)
        denom = math.sqrt(denom1) * math.sqrt(denom2)
        cos_theta = numer / denom
        list_cos.append(cos_theta)
    return list_cos


# Compare les cos des textes de reference vs nouveautext pour chaque item dans la liste de dictionnaires
# (= chaque phrase du nouveau texte)
# Calcule aussi le score d'accuracy
def compare_cos(listcos_ENG_newtext, listcos_FR_newtext, listcos_ESP_newtext,
                listcos_ITA_newtext, number):
    nb_phrase_anglais = 0
    nb_phrase_francais = 0
    nb_phrase_esp = 0
    nb_phrase_ita = 0

    if number == 1:
        nb_total_phrase_corpus = len(listdedico)
    elif number == 2:
        nb_total_phrase_corpus = len(listdedico2)
    else:
        nb_total_phrase_corpus = len(listdedico3)

    for i in range(nb_total_phrase_corpus):
        if (listcos_ITA_newtext[i] > listcos_ENG_newtext[i]) & \
                (listcos_ITA_newtext[i] > listcos_ESP_newtext[i]) & \
                (listcos_ITA_newtext[i] > listcos_FR_newtext[i]):
            nb_phrase_ita += 1
        elif (listcos_ENG_newtext[i] > listcos_FR_newtext[i]) & \
                (listcos_ENG_newtext[i] > listcos_ESP_newtext[i]) & \
                (listcos_ENG_newtext[i] > listcos_ITA_newtext[i]):
            nb_phrase_anglais += 1
        elif (listcos_FR_newtext[i] > listcos_ENG_newtext[i]) & \
                (listcos_FR_newtext[i] > listcos_ESP_newtext[i]) & \
                (listcos_FR_newtext[i] > listcos_ITA_newtext[i]):
            nb_phrase_francais += 1
        elif (listcos_ESP_newtext[i] > listcos_ENG_newtext[i]) & \
                (listcos_ESP_newtext[i] > listcos_FR_newtext[i]) & \
                (listcos_ESP_newtext[i] > listcos_ITA_newtext[i]):
            nb_phrase_esp += 1
        else:
            continue

    print("nb_phrase_anglais:", nb_phrase_anglais)
    print("nb_phrase_français:", nb_phrase_francais)
    print("nb_phrase_esp:", nb_phrase_esp)
    print("nb_phrase_ita:", nb_phrase_ita)
    print("nb_phrase_total:", nb_total_phrase_corpus)
    maxi = max(nb_phrase_anglais, nb_phrase_francais, nb_phrase_esp, nb_phrase_ita)
    if maxi == nb_phrase_anglais:
        text_language = "Anglais"
    elif maxi == nb_phrase_francais:
        text_language = "Francais"
    elif maxi == nb_phrase_esp:
        text_language = "Espagnol"
    else:
        text_language = "Italien"

    # Score d'accuracy
    score_accuracy = maxi / nb_total_phrase_corpus * 100
    listGdoc.append([score_accuracy])
    print("Le score d'accuracy : ", score_accuracy, "%. La langue du texte est : " + text_language + " !")
    print()


# Preparation des données pour l'analyse des unigrammes
# renvoie une liste de cosinus pour chaque phrase dans la liste de dictionnaires
listdedico = Dico_phrase(text_tokenize(new_text), 1)  # liste d'unigrammes
listcos_ENG_newtext = calcul_cos_listes(unigrammes(textENG), listdedico)  # liste de cosinus (ENG vs newtext)
listcos_FR_newtext = calcul_cos_listes(unigrammes(textFR), listdedico)  # liste de cosinus (FR vs newtext)
listcos_ESP_newtext = calcul_cos_listes(unigrammes(textESP), listdedico)  # liste de cosinus (ESP vs newtext)
listcos_ITA_newtext = calcul_cos_listes(unigrammes(textITA), listdedico)  # liste de cosinus (ITA vs newtext)


# Preparation des données pour l'analyse des bigrammes
# renvoie une liste de cosinus pour chaque phrase dans la liste de dictionnaires
listdedico2 = Dico_phrase(text_tokenize(new_text), 2)  # liste de bigrammes
listcos_ENG_newtext2 = calcul_cos_listes(bigrammes(textENG), listdedico2)  # liste de cosinus (ENG vs newtext)
listcos_FR_newtext2 = calcul_cos_listes(bigrammes(textFR), listdedico2)  # liste de cosinus (FR vs newtext)
listcos_ESP_newtext2 = calcul_cos_listes(bigrammes(textESP), listdedico2)  # liste de cosinus (ESP vs newtext)
listcos_ITA_newtext2 = calcul_cos_listes(bigrammes(textITA), listdedico2)  # liste de cosinus (ITA vs newtext)


# Preparation des données pour l'analyse des trigrammes
# renvoie une liste de cosinus pour chaque phrase dans la liste de dictionnaires
listdedico3 = Dico_phrase(text_tokenize(new_text), 3)
listcos_ENG_newtext3 = calcul_cos_listes(trigrammes(textENG), listdedico3)  # liste de cosinus (ENG vs newtext)
listcos_FR_newtext3 = calcul_cos_listes(trigrammes(textFR), listdedico3)  # liste de cosinus (FR vs newtext)
listcos_ESP_newtext3 = calcul_cos_listes(trigrammes(textESP), listdedico3)  # liste de cosinus (ESP vs newtext)
listcos_ITA_newtext3 = calcul_cos_listes(trigrammes(textITA), listdedico3)  # liste de cosinus (ITA vs newtext)


if __name__ == '__main__':
    """les unigrammes"""
print("--------------------")
print("MODÈLE UNIGRAMME")
print("Modèle unigramme: calcul du cos entre textanglais et nouveautext ",
      calcul_cos(unigrammes(textENG), unigrammes(new_text)))
print("Modèle unigramme: calcul du cos entre textfrançais et nouveautext ",
      calcul_cos(unigrammes(textFR), unigrammes(new_text)))
print("Modèle unigramme: calcul du cos entre textespagnol et nouveautext ",
      calcul_cos(unigrammes(textESP), unigrammes(new_text)))
print("Modèle unigramme: calcul du cos entre textitalien et nouveautext ",
      calcul_cos(unigrammes(textITA), unigrammes(new_text)))
print()
compare_cos(listcos_ENG_newtext, listcos_FR_newtext, listcos_ESP_newtext,
            listcos_ITA_newtext, 1)

print("--------------------")
print("MODÈLE BIGRAMME")
print("Modèle bigramme: calcul du cos entre textanglais et nouveautext ",
      calcul_cos(bigrammes(textENG), bigrammes(new_text)))
print("Modèle bigramme: calcul du cos entre textfrançais et nouveautext ",
      calcul_cos(bigrammes(textFR), bigrammes(new_text)))
print("Modèle bigramme: calcul du cos entre textespagnol et nouveautext ",
      calcul_cos(bigrammes(textESP), bigrammes(new_text)))
print("Modèle bigramme: calcul du cos entre textitalien et nouveautext ",
      calcul_cos(bigrammes(textITA), bigrammes(new_text)))
print()
compare_cos(listcos_ENG_newtext2, listcos_FR_newtext2, listcos_ESP_newtext2,
            listcos_ITA_newtext2, 2)

print("--------------------")
print("MODÈLE TRIGRAMME")
print("Modèle trigramme: calcul du cos entre textanglais et nouveautext ",
      calcul_cos(trigrammes(textENG), trigrammes(new_text)))
print("Modèle trigramme: calcul du cos entre textfrançais et nouveautext ",
      calcul_cos(trigrammes(textFR), trigrammes(new_text)))
print("Modèle trigramme: calcul du cos entre textespagnol et nouveautext ",
      calcul_cos(trigrammes(textESP), trigrammes(new_text)))
print("Modèle trigramme: calcul du cos entre textitalien et nouveautext ",
      calcul_cos(trigrammes(textITA), trigrammes(new_text)))
compare_cos(listcos_ENG_newtext3, listcos_FR_newtext3, listcos_ESP_newtext3,
            listcos_ITA_newtext3, 3)

# Ajoute la liste d'accuracy au Google Sheet
gdocData.updateGdoc(listGdoc)
