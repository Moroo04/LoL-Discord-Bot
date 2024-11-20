import discord
from discord.ext import commands
from scraper import get_champion_data, get_primary_runes, get_secondary_runes, check_for_errors
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
        if check_for_errors(soup):
            await ctx.send(f"Entschuldigung, keine Daten für {champion} gefunden. Überprüfe den Namen!")
            return
        
        # Runen-Daten extrahieren
        primary = get_primary_runes(soup)
        secondary = get_secondary_runes(soup)

        # Sende die Bilder der primären Runen
        await ctx.send("Primäre Runen:")
        for rune in primary:
            await ctx.send(rune)  # Bild-URL direkt senden

        # Sende die Bilder der sekundären Runen
        await ctx.send("Sekundäre Runen:")
        for rune in secondary:
            await ctx.send(rune)  # Bild-URL direkt senden

# Bot starten
bot.run(config["token"])
