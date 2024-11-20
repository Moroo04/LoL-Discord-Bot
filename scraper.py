from bs4 import BeautifulSoup
import requests

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Funktion, um die HTML-Daten für einen Champion zu laden
def get_champion_data(champion_name):
    url = f"https://u.gg/lol/champions/{champion_name}/build"
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
            rune_name = active_perk.find("img")["alt"]
            primary_runes.append(rune_name)
    return primary_runes

# Sekundäre Runen
def get_secondary_runes(soup):
    secondary_runes = []
    secondary_tree = soup.find("div", class_="secondary-tree")  # Zweiter Baum (sekundär)
    if secondary_tree:
        for active_perk in secondary_tree.find_all("div", class_="perk perk-active"):
            rune_name = active_perk.find("img")["alt"]
            secondary_runes.append(rune_name)
    return secondary_runes

# Stat-Shards
def get_stat_shards(soup):
    stat_shards = []
    for shard in soup.find_all("div", class_="shard shard-active"):
        stat_shards.append(shard.find("img")["alt"])
        if len(stat_shards) == 3:
            break
    return stat_shards