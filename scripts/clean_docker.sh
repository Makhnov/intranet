#!/bin/bash

# Arrêt et suppression de tous les conteneurs
echo -e "\033[0;34mArrêt et suppression de tous les conteneurs...\033[0m"
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
echo -e "\033[0;32mTous les conteneurs ont été arrêtés et supprimés.\033[0m"

# Nettoyage des conteneurs arrêtés
echo -e "\033[0;34mNettoyage des conteneurs arrêtés...\033[0m"
docker container prune -f

# Nettoyage des images non utilisées
echo -e "\033[0;34mNettoyage des images non utilisées...\033[0m"
docker image prune -a -f

# Nettoyage des volumes non utilisés
echo -e "\033[0;34mNettoyage des volumes non utilisés...\033[0m"
docker volume prune -f

# Nettoyage des réseaux non utilisés
echo -e "\033[0;34mNettoyage des réseaux non utilisés...\033[0m"
docker network prune -f

echo ""
echo -e "\033[0;32mNettoyage complet terminé.\033[0m"

# Affichage des ressources Docker restantes
echo ""
echo -e "\033[0;34mContainers :\033[0m"
docker ps -a

echo ""
echo -e "\033[0;34mImages :\033[0m"
docker images

echo ""
echo -e "\033[0;34mVolumes :\033[0m"
docker volume ls

echo ""
echo -e "\033[0;34mRéseaux :\033[0m"
docker network ls
echo ""
