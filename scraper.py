from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Funktion, um die HTML-Daten für einen Champion zu laden
def get_champion_runes(champion_name):
    url = f"https://u.gg/lol/champions/{champion_name}/build"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        return None

def get_champion_build(champion_name):
    url = f"https://mid.gg/champion/{champion_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        return None

# Primäre Runen
def get_primary_runes(soup):
    primary_runes = []
    primary_tree = soup.find("div", class_="rune-tree primary-tree")
    if primary_tree:
        for active_perk in primary_tree.find_all("div", class_=["perk perk-active", "perk keystone perk-active"]):
            rune_name = active_perk.find("img")["src"]
            primary_runes.append(rune_name)
    return primary_runes

# Sekundäre Runen
def get_secondary_runes(soup):
    secondary_runes = []
    secondary_tree = soup.find("div", class_="secondary-tree")  # Zweiter Baum (sekundär)
    if secondary_tree:
        for active_perk in secondary_tree.find_all("div", class_="perk perk-active"):
            rune_name = active_perk.find("img")["src"]
            secondary_runes.append(rune_name)
    return secondary_runes

# Champion-Build
def get_build(soup):
    build = []
    items = soup.find("div", class_="item-container")
    if items:
        for item in items.find_all("div", class_="ng-star-inserted"):
            item_name = item.find("img")["src"]
            build.append(item_name)

    return build

# Testen auf Fehler
def check_for_errors(soup):
    error_message = soup.find("div", class_="error-404 content-side-padding")
    if error_message:
        return True
    else:
        return False