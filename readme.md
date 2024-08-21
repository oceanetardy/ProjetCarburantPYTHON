# Projet PYTHON : Carburant GasGenius

Site permettant d'avoir des statistiques nationales sur les différents prix des carburants en France récupérés depuis une API
gouvernementale.
Possibilité de rechercher par code postal les stations avec les prix des différents carburants disponible

## Lancer le projet
- docker-compose up-d
- Acces sur localhost:8000

## Fichiers
- station_names_github.json => Fichier récupéré sur GitHub contenant le nom et la marque de certaines stations
- recupIds.py => Permet de récupérer dans un fichier ids_stations_gouv.csv les ids stations présents dans le cache
- ids_stations_gouv.csv => Contients les ids des stations du cache
- recupNames.py => Permet de sauvegarder dans le fichier stations_with_name.csv les infos de nom et marques des stationsrécupérer du fichiers stations_name.json pour les id dans ids_stations.csv
- stations_with_name.csv => Contient toutes les infos des stations avec la marque et le nom en plus 
- index.py => Programme principal

## Ordre de lancement des scripts et fonctionnement
- index.py => Récupération des infos et mise en cache avec insertion en BDD
- recupIds.py => Récupération des ids des stations récupérés depuis le site gouvernenmental
- recupNames.py  => Récupération des noms des stations des ids précédemment récupérés
- index. py => Chargement de nouveau en prenant en compte le nom et la marque des stations


_Réalisé par GUNGOR Muhammet & TARDY Océane_

_Mangagement de Projet Informatique 2023_
