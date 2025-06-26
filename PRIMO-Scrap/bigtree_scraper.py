from bigtree import Node, find, findall
import os
from pathlib import Path
from serpapi import GoogleSearch
import json
from google_play_scraper import permissions
from google_play_scraper import app
from scraper import app_name_from_id, info_app, query_for_list_app_info
import time


MOBILITY=Node("MOBILITY")

individual_transport=Node("individual transport", parent=MOBILITY)
public_transport=Node("public transport", parent=MOBILITY)
collective_transport=Node("collective transport", parent=MOBILITY)


#Arbre coté gauche individual transport

Active_Mobility=Node("Active Mobility", parent=individual_transport)
Passive_Mobility=Node("Passive Mobility", parent=individual_transport)

    ##Active Mobility
        ###Noeud Bycicle et fils de bycicle

bicycle=Node("bicycle", parent=Active_Mobility)
rent_1=Node("rent",synonymous=["lease", "leasing", "hire", "borrow", "rental", "renting"], parent=bicycle)
find_an_itinerary_1=Node("find an itinerary",synonymous=["plan a route", "locate directions", "search for a path"], parent=bicycle)
charging_station_1=Node("charging station",synonymous=["EV station", "electric charging point", "charge hub"], parent=bicycle)
navigation_1=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=bicycle)

        ##Noeud scooter et fils de scooter
scooter=Node("scooter", parent=Active_Mobility)
rent_2=Node("rent",synonymous=["lease", "leasing", "hire", "borrow", "rental", "renting"], parent=scooter)
find_an_itinerary_2=Node("find an itinerary",synonymous=["plan a route", "locate directions", "search for a path"], parent=scooter)
charging_station_2=Node("charging station",synonymous=["EV station", "electric charging point", "charge hub"], parent=scooter)
navigation_2=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=scooter)

        ##Noeud foot et fils de foot
foot=Node("foot", parent=Active_Mobility)
find_an_itinerary_3=Node("find an itinerary",synonymous=["plan a route", "locate directions", "search for a path"], parent=foot)
walk =Node("walk", synonymous=["run","hike","Guidance"], parent=foot)
navigation_3=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=foot)

        ##Noeud trotinette et fils de trotinette
trotinette=Node("trotinette", parent=Active_Mobility)
rent_3=Node("rent",synonymous=["lease", "leasing", "hire", "borrow", "rental", "renting"], parent=trotinette)
find_an_itinerary_4=Node("find an itinerary",synonymous=["plan a route", "locate directions", "search for a path"], parent=trotinette)
charging_station_3=Node("charging station",synonymous=["EV station", "electric  charging point", "charge hub"], parent=trotinette)
navigation_4=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=trotinette)

    ##Passive Mobility
        ###Noeud car et fils de car
car_1=Node("car", parent=Passive_Mobility)
rent_4=Node("rent",synonymous=["lease", "leasing", "hire", "borrow", "rental", "renting"], parent=car_1)
find_an_itinerary_5=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=car_1)
charging_station=Node("charging station",synonymous=["EV station", "electric  charging point", "charge hub"], parent=car_1)
road_traffic_1=Node("road traffic", synonymous=["vehicle flow","vehicle traffic", "traffic conditions", "bottling","traffic information"], parent=car_1)
reserve=Node("reserve", synonymous=["reservation", "request a service", "book a trip","order","schedule","place a reservation"], parent=car_1)
navigation_5=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=car_1)

        ###Noeud bike et fils de bike
bike=Node("bike", parent=Passive_Mobility)
rent5=Node("rent",synonymous=["lease", "leasing", "hire", "borrow", "rental", "renting"], parent=bike)
find_an_itinerary6=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=bike)
road_traffic_2=Node("road traffic", synonymous=["vehicle flow","vehicle traffic", "traffic conditions", "bottling","traffic information"], parent=bike)
navigation_6=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=bike)




#Arbre milieu public transport
    ##Noeud Bus et fils de Bus
bus_1=Node("bus", parent=public_transport)
buy_a_ticket_1=Node("buy a ticket", synonymous=["purchase a ticket", "book a ticket", "ticket reservation","procure a ticket"], parent=bus_1)
road_traffic_3=Node("road traffic",synonymous=["vehicle flow","vehicle traffic", "traffic conditions", "bottling","traffic information"], parent=bus_1)
find_an_itinerary7=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=bus_1)
navigation_7=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=bus_1)

    ##Noeud train et fils de train
train=Node("train", parent=public_transport)
buy_a_ticket_2=Node("buy a ticket",synonymous=["purchase a ticket", "book a ticket", "ticket reservation","procure a ticket"], parent=train)
find_an_itinerary_8=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=train)
travel_1=Node("travel",synonymous=["journey", "commute", "move","trip","voyage"], parent=train)
navigation_8=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=train)

    ##Noeud tram et fils de tram
tram=Node("tram", parent=public_transport)
buy_a_ticket_3=Node("buy a ticket",synonymous=["purchase a ticket", "book a ticket", "ticket reservation","procure a ticket"], parent=tram)
find_an_itinerary_9=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=tram)
view_traffic_1=Node("view traffic", synonymous=["check traffic", "monitor traffic", "traffic updates","congestion"], parent=tram)
navigation_9=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=tram)

    ##Noeud metro et fils de metro
metro=Node("metro", parent=public_transport)
buy_a_ticket_4=Node("buy a ticket",synonymous=["purchase a ticket", "book a ticket", "ticket reservation","procure a ticket"], parent=metro)
view_traffic_2=Node("view traffic",synonymous=["check traffic", "monitor traffic", "traffic updates","congestion"], parent=metro)
find_an_itinerary_10=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=metro)
navigation_10=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=metro)

    ##Noeud rer et fils de rer
rer=Node("rer", parent=public_transport)
buy_a_ticket_5=Node("buy a ticket",synonymous=["purchase a ticket", "book a ticket", "ticket reservation","procure a ticket"], parent=rer)
road_traffic_4=Node("road traffic",synonymous=["vehicle flow","vehicle traffic", "traffic conditions", "bottling","traffic information"], parent=rer)
find_an_itinerary_11=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=rer)
navigation_11=Node("navigation", synonymous=["Routing","Wayfinding","Guidance"], parent=rer)



#Arbre de droite collective transport
    ##Noeud coach et fils de coach
coach=Node("coach", parent=collective_transport)
reserve_a_seat=Node("reserve a seat", synonymous=["book a seat", "reserve a place", "secure a seat", "arrange a seat", "seat reservation"], parent=coach)
find_an_itinerary_12=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=coach)
travel_2=Node("travel", synonymous=["journey", "commute", "move","trip","voyage"], parent=coach)

    ##Noeud car et fils de car
car_2=Node("car", parent=collective_transport)
road_traffic_5=Node("road traffic",synonymous=["vehicle flow","vehicle traffic", "traffic conditions", "bottling","traffic information"], parent=car_2)
find_an_itinerary_13=Node("find an itinerary",synonymous=["plan a route", "locate directions"], parent=car_2)
carpool=Node("carpool", synonymous=["shared commute","car-pooling"], parent=car_2)
carshare=Node("car-share", synonymous=["Ride-sharing","Shared service"], parent=car_2)



#--------------------fonctions---------------------

def remove_duplicates(lst):
    seen = set()
    lst[:] = [item for item in lst if not (item in seen or seen.add(item))]

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Dossier créé : {directory_path}")
    else:
        print(f"Le dossier existe déjà : {directory_path}")

def query_key_word_synonymous(leaf):


    if leaf.children :
        print("the node " + leaf.name  + " is not a leaf")
    
    else:

        #Mesurer le temps d'exécution total de la fonction arbo_taxonomie
        #Temps de départ global
        start_time_total = time.time()  

        #dictionnaire de réponse 
        dict_app_details = {"applications": []}

        query_principal= leaf.name +" "+ leaf.parent.name

        #On crée le fichier principal pour y afficher tous les dossiers des différentes requêtes
        create_directory_if_not_exists("apps_of_query_" + query_principal + "_&_synonymous")
        os.chdir("apps_of_query_" + query_principal + "_&_synonymous")

        #On crée le dossier de la requête principal et on effectue le travail
        create_directory_if_not_exists(query_principal)
        os.chdir(query_principal)

        (L_app_id_q , dict_app_details_q) = query_for_list_app_info(query_principal)


        os.chdir(os.path.join(os.getcwd(), os.pardir))

        #On passe aux synonymes
        for elt in leaf.synonymous :
            query_synonymous=elt +" "+ leaf.parent.name
            create_directory_if_not_exists(query_synonymous)
            os.chdir(query_synonymous) 

            (L_app_id_s , dict_app_details_s) =query_for_list_app_info(query_synonymous)

            #Mise à jour de la liste finale de reponse
            L_app_id_q= list(set( L_app_id_q + L_app_id_s ))

            os.chdir(os.path.join(os.getcwd(), os.pardir))
        

        #Remplissage du dictionnaire finale des apps et de leurs détails 
        for id_app in L_app_id_q:     
            dict_app_details["applications"].append(info_app(id_app))
                
        #on crée un dictionnaire  qui liste les apps et de leurs id
        L_app_name = app_name_from_id(L_app_id_q)
        couple_name_id = {name: id for name, id in zip(L_app_name, L_app_id_q)}    

        #SAUVEGARDE
        # Sauvegarder dict_app_details
        with open("List_of_app_q&s_of_" + query_principal + ".json", "w", encoding="utf-8") as f:
            json.dump(couple_name_id, f, ensure_ascii=False, indent=4)
        # Sauvegarder couple_app_name_id
        with open("List_app_details_q&s_of_" + query_principal + ".json", "w", encoding="utf-8") as f:
            json.dump(dict_app_details, f, ensure_ascii=False, indent=4)


        #on n'oublie pas de sortir du fichier
        os.chdir(os.path.join(os.getcwd(), os.pardir))

        # Calculer et afficher le temps total 
        end_time_total = time.time()  
        elapsed_time_total = end_time_total - start_time_total 
        print(f"Temps d'exécution de {query_principal}_&_synonymous : {elapsed_time_total:.4f} secondes")



print(MOBILITY.show(attr_list=["synonymous"]))

#--------------------------------------------------


#fonction qui retourne l'arborescence de dossier avec les fichiers crées
#paramètre : le noeud dont on veut créer l'arborescence de fichiers requete
#sortie: Ne retourne rien
# Crée les fichiers json qui contiennent les applications scrappées 
def arbo_taxonomie(node,parent_path):
        
    # Créer le chemin complet pour le noeud
    current_directory_path = os.path.join(parent_path, node.name)
    create_directory_if_not_exists(current_directory_path)


    # Cas où le noeud est une feuille
    if not node.children:
        os.chdir(current_directory_path)
        query_key_word_synonymous(node)
      
        
    # Parcourir ensuite les enfants du noeud, appel récursif
    for child in node.children:
        arbo_taxonomie(child, current_directory_path)



path=os.getcwd()
#arbo_taxonomie(Active_Mobility, path)

