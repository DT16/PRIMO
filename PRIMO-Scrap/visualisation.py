from matplotlib import pyplot as plt
import pandas as pd

# Charger les données
data = pd.read_csv("applications_raw_csv.csv")

# Compter les occurrences de chaque genre
visu = data["Genre"].value_counts()

# Affichage des résultats pour vérifier
print(visu)

# Création du pie chart
plt.figure(figsize=(10, 8))
plt.pie(visu, labels=visu.index, autopct='%1.1f%%', startangle=140)
plt.title('Répartition des Genres d\'Applications')
plt.axis('equal')  # Pour que le pie chart soit circulaire

# Afficher le graphique
plt.show()
