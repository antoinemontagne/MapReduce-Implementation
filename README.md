# Implémentation d'un WordCount avec MapReduce en Python

## 1. Présentation et objectif du projet

Le but de ce projet est de réimplémenter l'algorithme de MapReduce pour le calcul distribué puis de l'utiliser pour exécuter un Wordcount sur un fichier d'une taille élevé d'au moins 1Go pour retrouver la loi d'Amdahl : 

<p align='center'>
 $$ speedup = {1 \over {1 - p + {1 \over s}}} $$
</p>

* p : taux de parallélisation de notre code
* s : nombre de machines utilisés

<p align='center'>
  <img src="image/repartis.jpg"/>
  <p align='center'>Schéma du projet</p>
</p>


## 2. Données

Les fichiers utilisés pour les tests ont été récupérés à partir du site : [Commoncrawl](https://data.commoncrawl.org/). Les données ont ensuite été nettoyés et mises bout à bout pour créer des fichiers avec une liste de mots séparés par des espaces.
Le fichier *split_final.txt* est un exemple de fichier qui peut être utilisé pour ce projet. Le fichier *result.txt* dans le répertoire */data* est le résultat pour le fichier d'entrée par défaut.

## 3. Utilisation
  
Dans ce répertoire, on retrouve 3 fichiers de code : 
* *client.py*
* *server.py*
* *deploy.sh*

### Les modifications à effectuer
* Pour lancer le code, il faut renseigner la liste des ordinateur dans le *deploy.sh* et le *client.py*.
* Dans le *client.py*, la variable globale **HOSTS** doit contenir la liste des ordinateurs.
* Il faut ensuite modifier la variable **login** dans le fichier *deploy.sh*.

### Commande pour lancer le code
Sur la même machine dans le réseau des machines renseignées dans le champ **HOSTS**, lancé successivement :

1. <code>./deploy.sh</code>
2. <code>python client.py</code>, selon la version de Python installée
