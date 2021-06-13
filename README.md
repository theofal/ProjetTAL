# Projet TAL : Détection de la langue d'un texte

-   **Présentation**

Ce projet est a été réalisé par Loubna Khennou et Théo Falgayrettes dans le cadre de notre L3 en informatique appliquée à la linguistique. Il s'agit d'un logiciel de détection de la langue d'un texte. 

Nous savons que, par exemple, la lettre "w" apparait bien plus souvent dans les textes de langue anglaise que dans les textes français. La fréquence des caractères n'est donc pas la même selon les différentes langues.
Ce logiciel analyse un mot, un paragraphe ou un fichier texte et compare l'occurence des caractères avec une base de données déjà présente. Ceci dans le but d'en déterminer la langue.

Les langues prises en charge actuellement sont le français, l'anglais, l'espagnol et l'italien.

-   **Le statut du projet**

Ce projet est encore au stade de développement, avons quelques idées d'améliorations de notre logiciel :
-- Augmenter l'efficacité en augmentant la taille des mots analysés.
-- Mise en place d'un système d'apprentissage automatique augmentant la taille de notre corpus de référence lorsqu'un texte/une phrase a été reconnue comme appartenant à 100% à une langue (nécessitera une approbation manuelle au début).
-- Prise en charge de langues supplémentaires.
-- Création d'une interface graphique.

-   **Les exigences concernant l’environnement de développement en vue de son intégration.**

L'utilisation de ce logiciel requiert l'installation préalable de Python : https://www.python.org/downloads/

-   **Une instruction pour l’installation et l’utilisation.**

Une fois le fichier téléchargé, rendez vous dans celui-ci via le terminal.

Il existe deux manières d'analyser un texte :

-- Analyse d'un fichier .txt : Python CodeProjet.py ~/monFichier.txt
-- Analyse d'un mot ou paragraphe en écriture libre: Python CodeProjet.py "mon paragraphe à analyser"

-  **Les technologies utilisées**

Google sheet (afin d'analyser les données) : https://docs.google.com/spreadsheets/d/1UR3POVh4q2Qr6kkQJfjFEOTbYE55BPWbU_eLBULXDh0/edit?usp=sharing


