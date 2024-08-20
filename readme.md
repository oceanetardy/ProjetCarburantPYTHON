# Projet PYTHON : Carburant

Ce projet à pour but de réaliser une programme permettant d'indiquer un code postal et d'indiquer chaque station d'essence, ainsi que les tarifs pour chaque carburant.

## Lancer le projet
- docker-compose up-d
- Acces sur localhost:8000

## Fichiers
- station_name.json => Fichier récupéré sur GitHub contenant le nom de certaines stations
- recupIds.py => oPermet de récupérer dans un fichier ids_stations.csv les ids stations présents dans le cache
- ids_stations.csv => Contients les ids des stations du cache
- recupNames.py => Permet de sauvegarder dans le fichier stations_with_name.csv les infos denom et marques des stationsrécupérer du fichiers stations_name.json pour les id dans ids_stations.csv
 - stations_with_name.csv => Contient toutes les infos des stations avec la marque et le nom en plus
 - index.py => Programme principale

## Ordre de lancement des scripts et fonctionnement
- index.py => Récup des infos et mise en cache avec insertion en BDD
- recupIds.py => Récupération des ids des stations récupéré depuis le site gouvernenmental
- recupNames.py  => Récupérer les noms des stations des ids précédemment récupérés
- index. py => Chargement de nouveau en prenant en compte le nom des stations


_Réalisé par GUNGOR Muhammet & TARDY Océane_

_Mangagement de Projet Informatique 2023_
