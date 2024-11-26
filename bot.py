import discord
from discord.ext import commands
from scraper import get_champion_runes, get_champion_build, get_primary_runes, get_secondary_runes, get_build, check_for_errors
import json

# Token laden
with open("config.json", "r") as file:
    config = json.load(file)

# Bot-Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} ist online!")

# Dynamischer Runen-Befehl
@bot.command()
async def runes(ctx, champion: str):
    # Daten für den Champion abrufen
    soup = get_champion_runes(champion.lower())  # Champion-Name klein schreiben
    if soup:
        if check_for_errors(soup):
            await ctx.send(f"Keine Daten für {champion} gefunden. Überprüfe den Namen!")
            return
        
        # Runen-Daten extrahieren
        primary = get_primary_runes(soup)
        secondary = get_secondary_runes(soup)

        # Sende die Bilder der primären Runen
        await ctx.send("Primäre Runen:")
        for rune in primary:
            await ctx.send(rune)

        # Sende die Bilder der sekundären Runen
        await ctx.send("Sekundäre Runen:")
        for rune in secondary:
            await ctx.send(rune)

@bot.command()
async def build(ctx, champion: str):
    # Daten für den Champion abrufen
    soup = get_champion_build(champion.lower())  # Champion-Name klein schreiben
    if soup:
        if check_for_errors(soup):
            await ctx.send(f"Keine Daten für {champion} gefunden. Überprüfe den Namen!")
            return
        
        # Build-Daten extrahieren
        build = get_build(soup)

        # Sende die Bilder der Items
        for item in build:
            await ctx.send(item)

# Bot starten
bot.run(config["token"])