# Google Play Store Scraping Automation

Ce programme permet d'automatiser des requêtes de recherche sur le Google Play Store via les outils **SerpApi** et **google_play_scraper**. L'entrée du programme consiste en un arbre qui décrit l'ensemble des requêtes que vous souhaitez effectuer. En sortie, un dossier est créé contenant des fichiers au format JSON avec les détails des recherches effectuées et les applications scrappées.

### Prérequis

Le scrappage est effectué à l'aide de **SerpApi**, qui permet de récupérer des données des applications du Google Play Store, et de la bibliothèque **google_play_scraper** pour obtenir des détails supplémentaires sur les applications.

#### Utilisation de SerpApi

1. Créez un compte sur [SerpApi](https://serpapi.com/).
2. Récupérez votre clé API personnelle.
3. Remplacez cette clé API dans le fichier **`.env`** ou directement dans les fonctions dans votre code (voir **search_google_play(query)**) pour authentifier vos requêtes.

#### Installation des bibliothèques nécessaires

Pour installer les dépendances nécessaires, utilisez les commandes suivantes :

```bash
pip install serpapi
pip install google-play-scraper
``` 

### Fonctions utiles

#### `info_app(idapp)`
Cette fonction permet d’obtenir les informations détaillées d'une application à partir de son identifiant unique (`idapp`) sur le Google Play Store.

#### `search_google_play(query)`
Cette fonction effectue une recherche sur le Google Play Store à partir du mot-clé `query` et renvoie les résultats associés.

### Fonction finale

#### `arbo_taxonomie`
La fonction **`arbo_taxonomie`** est la fonction principale qui permet de parcourir l'arbre des requêtes et de récupérer les résultats des recherches. Elle prend un nœud de l'arbre comme entrée et effectue les requêtes pour chaque nœud et ses synonymes.

Voici les principales étapes de son fonctionnement :

1. **Création de répertoires** : La fonction crée un répertoire pour chaque nœud de l'arbre où les résultats seront stockés.
2. **Recherche des applications** : Pour chaque nœud et ses synonymes, des recherches sont effectuées sur le Google Play Store via **SerpApi**.
3. **Récupération des résultats** : Les identifiants des applications sont collectés et leurs informations détaillées sont récupérées via **google_play_scraper**.
4. **Sauvegarde des résultats** : Les données sont sauvegardées dans des fichiers JSON pour chaque recherche effectuée.

### Exécution du programme
Pour exécuter le programme, il suffit de lancer le fichier bigtree_scraper.py



## Google Play Store Scraping Automation

**File:** `Extraction.py`

**Description:**
Once the applications are scraped, a second program will browse the local database of created files. It will create a folder named "applications". For each scraped application, this program will create a subfolder named after the application's ID. This subfolder will contain the HTML page of the terms and conditions as well as the app's permissions.

**Function:** `create_folders_app() `

