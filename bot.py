import discord
from discord.ext import commands
from scraper import get_champion_data, get_primary_runes, get_secondary_runes, get_stat_shards
import json

# Token laden
with open("config.json", "r") as file:
    config = json.load(file)

# Bot-Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} ist online!")

# Dynamischer Runen-Befehl
@bot.command()
async def runes(ctx, champion: str):
    # Daten für den Champion abrufen
    soup = get_champion_data(champion.lower())  # Champion-Name klein schreiben
    if soup:
        # Runen-Daten extrahieren
        primary = get_primary_runes(soup)
        secondary = get_secondary_runes(soup)
        shards = get_stat_shards(soup)

        # Nachricht erstellen
        message = (
            f"**Runen für {champion.capitalize()}:**\n\n"
            f"**Primäre Runen:**\n" + ", ".join(primary) + "\n\n"
            f"**Sekundäre Runen:**\n" + ", ".join(secondary) + "\n\n"
            f"**Stat-Shards:**\n" + ", ".join(shards)
        )
    else:
        # Fehlermeldung, falls Champion nicht gefunden wird
        message = f"Entschuldigung, keine Daten für {champion} gefunden. Überprüfe den Namen!"

    await ctx.send(message)

# Bot starten
bot.run(config["token"])
