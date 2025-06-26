import json
import os
import requests
import re
from bs4 import BeautifulSoup


#-------------------Useful fonctions------------------
def sanitize_filename(filename):
    # Liste des caractères non autorisés dans les noms de fichiers sous Windows
    invalid_chars = r'[".,<>:/\\|?*]'
    
    # Remplacer tous les caractères invalides par un underscore '_'
    sanitized_filename = re.sub(invalid_chars, '_', filename)
    
    # Optionnel : Retirer les espaces au début et à la fin du nom du fichier
    sanitized_filename = sanitized_filename.strip()
      
    return sanitized_filename


#Fonction pour ouvrir convenablement un fichier json
def open_json(file_path):
    """Fonction pour ouvrir et charger un fichier JSON."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Charger le contenu JSON dans une variable
            return data
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} n'a pas été trouvé.")
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {file_path} n'est pas un fichier JSON valide.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

#Fonction pour creer un dossier s'il n'existe pas déja
def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Dossier créé : {directory_path}")
    else:
        print(f"Le dossier existe déjà : {directory_path}")


#fonction qui effectue une sauvegarde sous formaat d'une page web à parir d'un lien
#passé en paramètre 
#parametre : -nom du dossier de sauvegarde
#            -lien de la page web des terms and conditions
#output :    Ne retourne rien
#            Effectue une sauvegarde de la page web sous format html
def save_html(app_id, term_condition_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    # Définir un délai maximum pour la requête (par exemple, 10 secondes)
    timeout_seconds = 20

    try:
        # Requête HTML pour accéder à la page web
        response = requests.get(term_condition_link, headers=headers, timeout=timeout_seconds)

        # Vérifie si la requête a réussi (code 200)
        response.raise_for_status()
        
        term_condition_file = f"terms_condition_of_{app_id}.html"
        
        # Sauvegarde
        with open(term_condition_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Page des conditions d'utilisation enregistrée sous : {term_condition_file}")

    except requests.exceptions.Timeout:
        print(f"Erreur : Le délai de réponse de {timeout_seconds} secondes a été dépassé pour {term_condition_link}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de la page des conditions d'utilisation : {e}")


#Fonction
#parametre: -nom du dossier de sauvegarde
#           -dictionnaire des permisions de l'app
#output :   Ne retourne rien
#           Effectue une sauvegarde des permission sous format json
def save_permisions(app_id, permisions):
    # Sauvegarde au format JSON
    file_name= "permisions_of_"+app_id+".json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(permisions, f, indent=4, ensure_ascii=False)


# Fonction pour rechercher récursivement un sous-dossier donné dans le dossier MOBILITY
def find_folder_in_mobility(base_folder, target_folder):
    for root, dirs, files in os.walk(base_folder):
        if os.path.basename(root) == target_folder:
            return root
    return None


#Fontion qui prends en parametre le lien d'un fichier json et qui retourne la liste des app id
# il cree les dossiers de chaque app avec dedans leur terms conditions
# et les permissions
#Avec création du fichier app
def app_2_tools(json_file):
    L=[]
    data=open_json(json_file)

    create_directory_if_not_exists("applications")#test à enlever
    os.chdir("applications")

    # Extraire les informations nécessaires
    for dict_app in data["applications"]:
        app_id = dict_app.get("appId")
        term_conditions_link = dict_app.get("privacyPolicy")
        permisions = dict_app.get("permisions") 
        L.append(app_id)

        #On crée le fichier de l'app
        create_directory_if_not_exists(app_id)
        os.chdir(app_id)

        #On sauvegarde les terms and conditions 
        save_html(app_id, term_conditions_link)

        #on enregistre les permissions
        save_permisions(app_id, permisions)

        #on sort du dossier
        os.chdir(os.path.join(os.getcwd(), os.pardir))

    return L



# Fonction qui parcourt le dossier MOBILITY, lit les fichiers JSON 
# qui commencent par List_app_details_q&s , effectue le procecuss de 
# app_2_tools
def create_folders_app():
    # Dossier où seront créés tous les sous-dossiers pour les applications
    applications_folder = "applications"
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)

    base_path=os.getcwd()
    # Dossier à parcourir (MOBILITY)
    mobility_folder = "MOBILITY"

    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = set()

    # Parcourir tous les fichiers dans le dossier MOBILITY et ses sous-dossiers
    for root, dirs, files in os.walk(mobility_folder):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print("traitement de"+filename)
                
                # charger et Ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data=open_json(file_path)

                #On parcours le fichier
                for dict_app in data["applications"]:
                    # Extraire les informations nécessaires
                    app_id = dict_app.get("appId")
                    term_conditions_link = dict_app.get("privacyPolicy")
                    permisions = dict_app.get("permisions")
                                    
                    # Vérifier si l'appId a déjà été traité
                    if app_id not in processed_app_ids:

                        processed_app_ids.add(app_id)

                        #On crée le fichier de l'app
                        app_directory = os.path.join(save_path, app_id)
                        create_directory_if_not_exists(app_directory)
                        os.chdir(app_directory)


                        #On sauvegarde les terms and conditions 
                        save_html(app_id, term_conditions_link)

                        #on enregistre les permissions
                        save_permisions(app_id, permisions)
                    
                    os.chdir(base_path)

    
    return processed_app_ids


#Fonction qui permet d'obtenir les permissions de chaque application
def list_of_app_taxo_permisions():
    # Dossier où seront créés tous les sous-dossiers pour les applications
    applications_folder = "applications_permissions_names"
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)

    base_path=os.getcwd()
    # Dossier à parcourir (MOBILITY)
    mobility_folder = "MOBILITY"

    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = {}

    # Parcourir tous les fichiers dans le dossier MOBILITY et ses sous-dossiers
    for root, dirs, files in os.walk(mobility_folder):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print("traitement de"+filename)
                
                # charger et Ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data=open_json(file_path)

                #On parcours le fichier
                for dict_app in data["applications"]:
                    # Extraire les informations nécessaires
                    app_id = dict_app.get("appId")
                    app_name=dict_app.get("title")
                    app_name=sanitize_filename(app_name)
                    permisions = dict_app.get("permisions")

                    # Vérifier si le nom de l'application a déjà été traité
                    original_app_name = app_name  
                    counter = 2  # Commencer avec le suffixe "_2"
                    
                    # Si le nom existe déjà dans processed_app_ids, on ajoute un suffixe
                    while app_name in processed_app_ids.values():
                        app_name = f"{original_app_name}_{counter}"
                        counter += 1
                    
                                    
                    # Vérifier si l'appId a déjà été traité
                    if app_id not in processed_app_ids:                        
                        
                        processed_app_ids[app_id]= app_name

                        #On crée le fichier de l'app
                        app_directory = os.path.join(save_path, app_name)
                        create_directory_if_not_exists(app_directory)
                        os.chdir(app_directory)


                        #On sauvegarde permissions
                        save_permisions(app_name, permisions)


                    os.chdir(base_path)
    
    os.chdir(applications_folder)
    with open("list_of_the_apps.json", "w", encoding="utf-8") as f:
        json.dump(processed_app_ids, f, indent=4, ensure_ascii=False)
    
    return processed_app_ids
#----------------------------------------------------------------------








#--------Fonctions pour obtenir la Liste brute des applications--------
def list_of_app_taxo_names_raw():
    # Dossier où seront créés tous les sous-dossiers pour les applications
    applications_folder = "applications_names_raw"
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)

    base_path=os.getcwd()
    # Dossier à parcourir (MOBILITY)
    mobility_folder = "MOBILITY"

    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = {}

    # Parcourir tous les fichiers dans le dossier MOBILITY et ses sous-dossiers
    for root, dirs, files in os.walk(mobility_folder):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print("traitement de"+filename)
                
                # charger et Ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data=open_json(file_path)

                #On parcours le fichier
                for dict_app in data["applications"]:
                    # Extraire les informations nécessaires
                    app_id = dict_app.get("appId")
                    app_name=dict_app.get("title")
                    app_name=sanitize_filename(app_name)

                    # Vérifier si le nom de l'application a déjà été traité
                    original_app_name = app_name  
                    counter = 2  # Commencer avec le suffixe "_2"
                    
                    # Si le nom existe déjà dans processed_app_ids, on ajoute un suffixe
                    while app_name in processed_app_ids.values():
                        app_name = f"{original_app_name}_{counter}"
                        counter += 1
                    
                                    
                    # Vérifier si l'appId a déjà été traité
                    if app_id not in processed_app_ids:                        
                        
                        processed_app_ids[app_id]= app_name

                        #On crée le fichier de l'app
                        app_directory = os.path.join(save_path, app_name)
                        create_directory_if_not_exists(app_directory)
                        os.chdir(app_directory)


                        #On sauvegarde dict_app
                        with open("details_of_"+app_name+".json" , "w", encoding="utf-8") as f:
                            json.dump(dict_app, f, indent=4, ensure_ascii=False)


                    os.chdir(base_path)
    
    os.chdir(applications_folder)
    with open("list_of_the_apps.json", "w", encoding="utf-8") as f:
        json.dump(processed_app_ids, f, indent=4, ensure_ascii=False)
    
    return processed_app_ids


def list_of_app_taxo_id_raw():
    # Dossier où seront créés tous les sous-dossiers pour les applications
    applications_folder = "applications_id_raw"
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)

    base_path=os.getcwd()
    # Dossier à parcourir (MOBILITY)
    mobility_folder = "MOBILITY"

    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = {}

    # Parcourir tous les fichiers dans le dossier MOBILITY et ses sous-dossiers
    for root, dirs, files in os.walk(mobility_folder):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print("traitement de"+filename)
                
                # charger et Ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data=open_json(file_path)

                #On parcours le fichier
                for dict_app in data["applications"]:
                    # Extraire les informations nécessaires
                    app_id = dict_app.get("appId")
                    app_name=dict_app.get("title")
                    app_name=sanitize_filename(app_name)

                    # Vérifier si le nom de l'application a déjà été traité
                    original_app_name = app_name  
                    counter = 2  # Commencer avec le suffixe "_2"
                    
                    # Si le nom existe déjà dans processed_app_ids, on ajoute un suffixe
                    while app_name in processed_app_ids.values():
                        app_name = f"{original_app_name}_{counter}"
                        counter += 1
                
                                    
                    # Vérifier si l'appId a déjà été traité
                    if app_id not in processed_app_ids:
                        processed_app_ids[app_id]= app_name

                        #On crée le fichier de l'app
                        app_directory = os.path.join(save_path, app_id)
                        create_directory_if_not_exists(app_directory)
                        os.chdir(app_directory)


                        #On sauvegarde dict_app
                        with open("details_of_"+app_id+".json" , "w", encoding="utf-8") as f:
                            json.dump(dict_app, f, indent=4, ensure_ascii=False)

                    
                    os.chdir(base_path)
    
    os.chdir(applications_folder)
    with open("list_of_the_apps.json", "w", encoding="utf-8") as f:
        json.dump(processed_app_ids, f, indent=4, ensure_ascii=False)

    
    return processed_app_ids


#--------Fonctions pour obtenir la Liste des aplications nettoyées-------
Genre_filter= ["Travel & Local", "Maps & Navigation","Auto & Vehicles",
               "Sports","Tools", "Health & Fitness",          
               "Lifestyle","Personalization" ]                         
                       
def list_of_app_taxo_names_clean():
    # Dossier où seront créés tous les sous-dossiers pour les applications
    applications_folder = "applications_names_clean"
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)

    base_path=os.getcwd()
    # Dossier à parcourir (MOBILITY)
    mobility_folder = "MOBILITY"

    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = {}

    # Parcourir tous les fichiers dans le dossier MOBILITY et ses sous-dossiers
    for root, dirs, files in os.walk(mobility_folder):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print("traitement de"+filename)
                
                # charger et Ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data=open_json(file_path)

                #On parcours le fichier
                for dict_app in data["applications"]:
                    # Extraire les informations nécessaires
                    app_id = dict_app.get("appId")
                    app_name=dict_app.get("title")
                    app_name=sanitize_filename(app_name)
                    app_genre=dict_app.get("genre")

                    # Vérifier si le nom de l'application a déjà été traité
                    original_app_name = app_name  
                    counter = 2  # Commencer avec le suffixe "_2"

                    # Si le nom existe déjà dans processed_app_ids, on ajoute un suffixe
                    while app_name in processed_app_ids.values():
                        app_name = f"{original_app_name}_{counter}"
                        counter += 1


                    #ON filtre en fonction du genre
                    if app_genre in Genre_filter:
                                    
                        # Vérifier si l'appId a déjà été traité
                        if app_id not in processed_app_ids:                        
                            
                            processed_app_ids[app_id]= app_name

                            #On crée le fichier de l'app
                            app_directory = os.path.join(save_path, app_name)
                            create_directory_if_not_exists(app_directory)
                            os.chdir(app_directory)


                            #On sauvegarde dict_app
                            with open("details_of_"+app_name+".json" , "w", encoding="utf-8") as f:
                                json.dump(dict_app, f, indent=4, ensure_ascii=False)


                        os.chdir(base_path)
    
    os.chdir(applications_folder)
    with open("list_of_the_apps.json", "w", encoding="utf-8") as f:
        json.dump(processed_app_ids, f, indent=4, ensure_ascii=False)

    
    return processed_app_ids


def list_of_app_taxo_id_clean():
    # Dossier où seront créés tous les sous-dossiers pour les applications
    applications_folder = "applications_id_clean"
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)

    base_path=os.getcwd()
    # Dossier à parcourir (MOBILITY)
    mobility_folder = "MOBILITY"

    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = {}

    # Parcourir tous les fichiers dans le dossier MOBILITY et ses sous-dossiers
    for root, dirs, files in os.walk(mobility_folder):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print("traitement de"+filename)
                
                # charger et Ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data=open_json(file_path)

                #On parcours le fichier
                for dict_app in data["applications"]:
                    # Extraire les informations nécessaires
                    app_id = dict_app.get("appId")
                    app_name=dict_app.get("title")
                    app_name=sanitize_filename(app_name)
                    app_genre=dict_app.get("genre")

                    # Vérifier si le nom de l'application a déjà été traité
                    original_app_name = app_name  
                    counter = 2  # Commencer avec le suffixe "_2"
                    
                    # Si le nom existe déjà dans processed_app_ids, on ajoute un suffixe
                    while app_name in processed_app_ids.values():
                        app_name = f"{original_app_name}_{counter}"
                        counter += 1


                    #ON filtre en fonction du genre
                    if app_genre in Genre_filter:
                                    
                        # Vérifier si l'appId a déjà été traité
                        if app_id not in processed_app_ids:
                            processed_app_ids[app_id]= app_name

                            #On crée le fichier de l'app
                            app_directory = os.path.join(save_path, app_id)
                            create_directory_if_not_exists(app_directory)
                            os.chdir(app_directory)


                            #On sauvegarde dict_app
                            with open("details_of_"+app_id+".json" , "w", encoding="utf-8") as f:
                                json.dump(dict_app, f, indent=4, ensure_ascii=False)

                        
                        os.chdir(base_path)
    
    os.chdir(applications_folder)
    with open("list_of_the_apps.json", "w", encoding="utf-8") as f:
        json.dump(processed_app_ids, f, indent=4, ensure_ascii=False)

    
    return processed_app_ids

#-----------------------------------------------------------------------------------





#-----------Compter les apllications depuis un noeud-------------------
"""
# Fonction principale qui parcourt le dossier spécifié et crée les dossiers d'applications
def list_of_app_node_taxo_id_(folder_name):
    # Dossier où seront créés tous les sous-dossiers pour les applications
    applications_folder = "applications_id_of_" + folder_name
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)
    

    # Dossier principal (MOBILITY)
    mobility_folder = "MOBILITY"
    base_path=os.path.join(os.getcwd(), mobility_folder)
    
    # Rechercher le sous-dossier spécifié dans MOBILITY
    target_folder_path = find_folder_in_mobility(mobility_folder, folder_name)
    
    if target_folder_path is None:
        print(f"Le sous-dossier {folder_name} n'a pas été trouvé dans {mobility_folder}.")
        return
    
    target_path = os.path.abspath(target_folder_path)


    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = {}

    # Parcourir tous les fichiers dans le sous-dossier trouvé
    for root, dirs, files in os.walk(target_folder_path):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print(f"Traitement du fichier : {filename}")
                
                # Charger et ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data = open_json(file_path)

                # On parcourt les applications dans le fichier JSON
                if data and "applications" in data:
                    for dict_app in data["applications"]:
                        # Extraire les informations nécessaires
                        app_id = dict_app.get("appId")
                        app_name = dict_app.get("title")
                        app_name = sanitize_filename(app_name)

                        # Vérifier si le nom de l'application a déjà été traité
                        original_app_name = app_name  
                        counter = 2  # Commencer avec le suffixe "_2"
                        
                        # Si le nom existe déjà dans processed_app_ids, on ajoute un suffixe
                        while app_name in processed_app_ids.values():
                            app_name = f"{original_app_name}_{counter}"
                            counter += 1
                        
                        # Vérifier si l'appId a déjà été traité
                        if app_id not in processed_app_ids:
                            processed_app_ids[app_id] = app_name

                            # Créer un sous-dossier pour chaque application dans le dossier "applications"
                            app_folder = os.path.join(save_path, app_id)
                            create_directory_if_not_exists(app_folder)
                            os.chdir(app_folder)

                            # Sauvegarder les informations de l'application dans un fichier JSON
                            with open(f"details_of_{app_id}.json", "w", encoding="utf-8") as f:
                                json.dump(dict_app, f, indent=4, ensure_ascii=False)

                            # Revenir au répertoire principal
                            os.chdir(base_path)
                    
    # Sauvegarde du fichier list des applications traitées
    os.chdir(save_path)
    with open("list_of_the_apps.json", "w", encoding="utf-8") as f:
        json.dump(processed_app_ids, f, indent=4, ensure_ascii=False)
    
    return processed_app_ids

"""

def list_of_app_node_taxo_id_(folder_name):
    # Fonction qui parcourt le dossier MOBILITY et ses sous-dossiers spécifiés pour traiter les fichiers JSON.

    # Créer le dossier où les informations des applications seront stockées
    applications_folder = "applications_id_of_" + folder_name
    create_directory_if_not_exists(applications_folder)
    save_path = os.path.join(os.getcwd(), applications_folder)
    base_path=os.getcwd()
    
    # Dossier principal (MOBILITY)
    mobility_folder = "MOBILITY"
    
    # Trouver le sous-dossier spécifié dans MOBILITY
    target_folder_path = find_folder_in_mobility(mobility_folder, folder_name)
    
    if target_folder_path is None:
        print(f"Le sous-dossier {folder_name} n'a pas été trouvé dans {mobility_folder}.")
        return
    
    # Sauvegarde du chemin du dossier cible
    target_path = os.path.abspath(target_folder_path)

    # Ensemble pour suivre les applications déjà traitées
    processed_app_ids = {}

    # Parcourir tous les fichiers dans le sous-dossier trouvé
    for root, dirs, files in os.walk(target_folder_path):
        for filename in files:
            if filename.startswith("List_app_details_q&s"): 
                print(f"Traitement du fichier : {filename}")
                
                # Charger et ouvrir le fichier JSON
                file_path = os.path.join(root, filename)
                data = open_json(file_path)

                # On parcourt les applications dans le fichier JSON
                if data and "applications" in data:
                    for dict_app in data["applications"]:
                        # Extraire les informations nécessaires
                        app_id = dict_app.get("appId")
                        app_name = dict_app.get("title")
                        app_name = sanitize_filename(app_name)

                        # Vérifier si le nom de l'application a déjà été traité
                        original_app_name = app_name  
                        counter = 2  # Commencer avec le suffixe "_2"
                        
                        # Si le nom existe déjà dans processed_app_ids, on ajoute un suffixe
                        while app_name in processed_app_ids.values():
                            app_name = f"{original_app_name}_{counter}"
                            counter += 1
                        
                        # Vérifier si l'appId a déjà été traité
                        if app_id not in processed_app_ids:
                            processed_app_ids[app_id] = app_name

                            # Créer un sous-dossier pour chaque application dans le dossier "applications"
                            app_folder = os.path.join(save_path, app_id)
                            create_directory_if_not_exists(app_folder)
                            os.chdir(app_folder)

                            # Sauvegarder les informations de l'application dans un fichier JSON
                            with open("details_of_"+ app_id +".json", "w", encoding="utf-8") as f:
                                json.dump(dict_app, f, indent=4, ensure_ascii=False)
                            
                        os.chdir(base_path)
                            
                    
    # Sauvegarde du fichier list des applications traitées
    with open(f"{applications_folder}/list_of_the_apps.json", "w", encoding="utf-8") as f:
        json.dump(processed_app_ids, f, indent=4, ensure_ascii=False)
    
    return processed_app_ids









#print(find_folder_in_mobility("MOBILITY","bicycle"))
#os.chdir(find_folder_in_mobility("MOBILITY","public transport"))
#print("-----------------------")
#print(os.path.abspath(find_folder_in_mobility("MOBILITY","bicycle")))


#for every branch how many app we have, every node
#who is behind the applications , the company , the country , the locations 
#distribution of nb of download , price , genre , key word of the prmissions, rating
#key word and permissions vs genre (try to see coorelation)
#The ne