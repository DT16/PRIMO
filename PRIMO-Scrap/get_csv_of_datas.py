import os
import json
import pandas as pd


#------------------Useful fonctions-------------
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


def parse_number(number_str):
    # Enlever les virgules et le signe '+' à la fin
    cleaned_str = number_str.replace(",", "").rstrip("+")
    # Convertir en entier
    return int(cleaned_str)

#------------------


def read_files_in_applications(applications_folder):
    
    data_dicts = []  

    title = []
    appId = []
    installs =[]
    score =[]
    ratings=[]
    price=[]
    developer=[]
    developerAddress=[]
    genre=[]
    contentRating=[]
    permision_key=[]
    

    # Parcours du dossier 'applications' et de ses sous-dossiers
    for root, dirs, files in os.walk(applications_folder):
        for filename in files:
            # Vérifier si le fichier commence par 'details_of_'
            if filename.startswith("details_of_") and filename.endswith(".json"):
                
                #Lecture du fichier 
                file_path = os.path.join(root, filename)
                data=open_json(file_path)

                # Ajouter les données aux listes
                title.append(data.get("title", "").strip())
                appId.append(data.get("appId", "").strip())
                installs.append( parse_number(data.get("installs", 0)) )  
                score.append(data.get("score", 0.0))
                ratings.append(data.get("ratings", 0.0))  
                price.append(data.get("price", 0))  
                developer.append(data.get("developer", "").strip())
                contentRating.append(data.get("contentRating", "").strip())
                genre.append(data.get("genre", "").strip())


                # Vérifier si "developerAddress" est None ou contient des retours à la ligne, puis nettoyer
                developerAddress_value = data.get("developerAddress", None)
                if developerAddress_value:
                    # Remplacer les "\n" par des espaces
                    developerAddress_value = developerAddress_value.replace("\n", " ").strip()
                developerAddress.append(developerAddress_value if developerAddress_value else "")


                # Vérification si "permision_key" existe et n'est pas None
                perm_key = data.get("permisions")
                if perm_key:  # Si permision_key existe et n'est pas None
                    permision_key.append(list(perm_key.keys()))  # Extraire les clés et les ajouter à la liste
                else:
                    permision_key.append([])  # Si permision_key est None, ajouter une liste vide


    # Création du dataframe à partir des listes
    df = pd.DataFrame({
        "Title": title,
        "AppId": appId,
        "Installs": installs,
        "Score": score,
        "Ratings": ratings,
        "Price": price,
        "Developer": developer,
        "DeveloperAddress": developerAddress,
        "ContentRating": contentRating,
        "Genre": genre,
        "permision key":permision_key
    })

    return df



# Appel de la fonction pour récupérer les données
folder_name="applications_id_raw"
df_applications = read_files_in_applications(folder_name)

# Enlever les espaces indésirables dans les colonnes (noms des colonnes)
df_applications.columns = [col.strip() for col in df_applications.columns]

csv_file_path = folder_name+"_csv.csv"
df_applications.to_csv(csv_file_path, index=False, encoding="utf-8")