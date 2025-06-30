from serpapi import GoogleSearch
import json
import json
from google_play_scraper import permissions
from google_play_scraper import app
import os
from pathlib import Path
import time


def erase_entry(dict, L):
    for elt in L:
        if elt in dict.keys() :
            del dict[elt]
    return dict

#Fonction qui donne les infos sur une app donné à partir de son id
#paramètre : id de l'app en question
#sortie : le dictionnaire contennant toutes les infos voulues sur l'app
def info_app(idapp):
    result1 = app(
    idapp,
    lang='en', # defaults to 'en'
    country='fr' # defaults to 'us'
)
    result2 = permissions(
    idapp,
    lang='en', 
    country='fr', 
)
    erase_entry(result1,["adSupported","contentRatingDescription","videoImage",
    "video","screenshots","genreId","categories","icon","headerImage",
    "developerId","offersIAP","saleText","originalPrice","sale","saleTime",
    "reviews","histogram","realInstalls","minInstalls","descriptionHTML",
    "updated","version","comments","containsAds","url","inAppProductPrice","free"])
    
    d=dict()
    d["permisions"]=result2 
    f_result= result1 | (d)

    # Sauvegarde au format JSON
#    with open("app " + idapp+'.json', 'w',encoding="utf-8") as fp:
#        json.dump(f_result, fp,  indent=4, ensure_ascii=False)    
    return f_result 

#Fonction qui retourne le nom d'une app connaissant son id
#Parametre: Liste d'app id
def app_name_from_id(L):
    L_rep=[]
    for elt in L:
        app_name=info_app(elt)["title"]
        L_rep.append(app_name)
    return L_rep


#Fonction qui effectue une recherche google plays store à partir du mot clé query
#Et renvoie la liste des id des applications tout en les stockant dans un fichier json
#paramètre : le mot clé qui représente la recherche à effectuer
#sortie: Un couple le 1er element est La liste des ids toutes les applications de cette recherche 
#        et le 2ème est un dictionnaire qui liste les apps. 
#        Sauvegarde de ce dictionnaire dans un fichier json
"""
def search_google_play(query):
    params = {
    "engine": "google_play",
    "hl": "en",
    "gl": "fr",
    "store": "apps",
    "q": query,
    "api_key": 
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    L=[]
    for dict in (((results["organic_results"])[0])["items"]) :
        L.append(dict["product_id"])
        erase_entry(dict,["description","thumbnail","video","downloads",
        "feature_image","category","author","rating","serpapi_link","link","description"])
    
    # Sauvegarde au format JSON
    with open("List_app_query= "+ query + ".json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    return (L,results)
"""

def search_google_play(query):
    # Paramètres de recherche
    params = {
        "engine": "google_play",
        "hl": "en",
        "gl": "fr",
        "store": "apps",
        "q": query,
        "api_key": "8f487639041390cb31289df387fe96cc0ef12a70d0ddafe822e087562a97a6ca"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Liste pour stocker les résultats des applications
    L = []

    # Vérification de la présence de la clé 'organic_results'
    if "organic_results" in results:
        organic_results = results["organic_results"]

        # Vérifier si la clé 'organic_results' contient des éléments
        if organic_results:
            # Parcours des résultats dans 'organic_results' et ajout des IDs de produits
            for dict in organic_results[0].get("items", []):  # Assurez-vous que 'items' existe
                L.append(dict["product_id"])
                erase_entry(dict, ["description", "thumbnail", "video", "downloads",
                                    "feature_image", "category", "author", "rating", "serpapi_link", "link", "description"])

        else:
            print("Aucun résultat trouvé pour la requête.")
    else:
        print("La clé 'organic_results' n'est pas présente dans les résultats de la recherche.")

    # Sauvegarde des résultats au format JSON
    with open(f"List_app_query={query}.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    return L, results


# Fonction finale 
# paramètre : La requete qui est la recherche google play store
# output : -dict app_details qui contient la liste des applications 
#          obtenues par cette recherche et les spécificités de chaque app
#          -La liste des applications
#          ++Enregistre 2 fichiers json , le premier : une simple dictionnaire contenant 
#          la liste des applis scrappé (nom et id) et les spécifications de l'API utilisé pour ce scrappage
#          le second: le dictionnaire app_details 
def query_for_list_app_info(query):
    app_details = {"applications": []}
    L=(search_google_play(query))[0]
    for idapp in L:
        app_info = info_app(idapp)
        app_details["applications"].append(app_info)

    # Sauvegarde au format JSON
    with open("apps_details_query= "+ query + ".json", "w", encoding="utf-8") as f:
        json.dump(app_details, f, indent=4, ensure_ascii=False)

    return (L,app_details)




#Input: lien du fichier json
#Output: La liste des applications communes aux différentes requêtes
#Sauvegarde de 2 fichiers en json :
#Methode archaîque car obligation de rentrer les requetes à la main

def app_of_query_and_synonymous(data):
    with open(data, "r") as f:  #chargement de fichier json
        dict = json.load(f)
    
    base_path = os.getcwd() #chemin inital


    for key_word, list_of_synonymous in dict.items(): #on parcour du dictionnnaire sous forme de couple clé valeur (key_word, list_of_synonyms)
        
        #On crée l'arborescence des fichiers , chaque fichier json liés à une 
        #requête précise sera rangé dans un dossier qui lui est propre
        os.chdir(base_path)
        principal_path = "datas_of_"+key_word+" & synonymous"  #dossier principal de chaque groupe de requete
        os.mkdir(principal_path)
        os.chdir(principal_path)

        #dictionnaire de réponse 
        dict_app_details = {"applications": []}

        os.mkdir(key_word)
        os.chdir(key_word)
        (L_app_id , dict_app_details_nu) = query_for_list_app_info(key_word) 
        os.chdir(os.path.join(os.getcwd(),os.pardir))         

        for synonymous in list_of_synonymous:  #ensuite on parcourt les attributs de la clé , qui sont les synonymes du key word
            os.mkdir(synonymous)
            os.chdir(synonymous)
            (Lsyno_app_id,syno_dict) =query_for_list_app_info(synonymous)
            L_app_id= list(set( L_app_id + Lsyno_app_id ))
            os.chdir(os.path.join(os.getcwd(),os.pardir))

        
        L_app_name= app_name_from_id(L_app_id) 
        couple_name_id = {name: id for name, id in zip(L_app_name, L_app_id)}


        #on remplit finalement le dictionnaire de réponse , par les toutes les 
        # applications identifés avec leurs détails compris .
        for id_app in L_app_id:     
            dict_app_details["applications"].append(info_app(id_app))

        # Sauvegarde au format JSON la liste des applications pour le key word 
        #et ses synonymes
        with open("List_of_app_q&s_of "+ key_word +".json", "w", encoding="utf-8") as f:
            json.dump(couple_name_id, f, ensure_ascii=False, indent=4)

        #on save au format json la liste des applications et leurs détails
        # pour le key word et ses synonymes
        with open("List_app_details_q&s_of "+ key_word +".json", "w", encoding="utf-8") as f:
            json.dump(dict_app_details, f, ensure_ascii=False, indent=4)
    

    return L_app_id



#app_of_query_and_synonymous("request.json")

