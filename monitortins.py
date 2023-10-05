import requests
from bs4 import BeautifulSoup
import hashlib
import time
import json

# URL de la page à surveiller
url = "https://cartesplus.fr/produit/display-minitins-ev3-5/"

# URL du webhook Discord
discord_webhook_url = "https://discord.com/api/webhooks/1158703634457055234/eHowgwlFJNk_DeXT4r5CEPjxlJSKbP49S_EE_XjxOIFE8fFiUU4CbKS2RGZ07PQvu_66"

# Fonction pour récupérer le contenu de la page
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Fonction pour calculer la somme de contrôle MD5 du contenu de la page
def calculate_md5(content):
    return hashlib.md5(content.encode()).hexdigest()

# Fonction pour envoyer une notification à Discord
def send_discord_notification(content):
    payload = {
        "content": content
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(discord_webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 204:
        print("Notification envoyée avec succès à Discord")
    else:
        print("Erreur lors de l'envoi de la notification à Discord")

# Fonction pour envoyer un message initial à Discord
def send_initial_discord_notification():
    send_discord_notification("Moniteur lancé sur la page " + url)

# Définir la somme de contrôle MD5 initiale
initial_md5 = calculate_md5(get_page_content(url))

# Envoyer un message initial à Discord au démarrage du script
send_initial_discord_notification()

while True:
    # Obtenir le contenu actuel de la page
    current_content = get_page_content(url)

    if current_content:
        # Calculer la somme de contrôle MD5 du contenu actuel
        current_md5 = calculate_md5(current_content)

        # Vérifier s'il y a eu un changement
        if current_md5 != initial_md5:
            print("La page a été modifiée !")
            send_discord_notification("La page a été modifiée sur " + url + " **OUBLIEZ PAS LE CODE MATTISPOKEMON POUR 5% DE RABAIS** ")
            initial_md5 = current_md5

    # Attendre un certain temps avant de vérifier à nouveau la page (par exemple, toutes les 15 minutes)
    time.sleep(5)
