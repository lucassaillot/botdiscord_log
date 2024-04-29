# Librairies et paramètres
import discord
import os
from dotenv import load_dotenv
import pytz
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
paris_timezone = pytz.timezone('Europe/Paris')

load_dotenv()
bot = discord.Bot(intents=discord.Intents.all())

# Message quand bot en ligne
@bot.event
async def on_ready():
    print('En ligne')

# Couleurs embed
hex_color_message_delete = 0xff0000
rgb_color_message_delete = ((hex_color_message_delete >> 16) & 0xFF, (hex_color_message_delete >> 8) & 0xFF, hex_color_message_delete & 0xFF)
hex_color_message_edit = 0xff6200
rgb_color_message_edit = ((hex_color_message_edit >> 16) & 0xFF, (hex_color_message_edit >> 8) & 0xFF, hex_color_message_edit & 0xFF)


# ID salon log
logs_channel_id = 969300560253689906

# Quand message supprimé envoyer dans le salon log
@bot.event
async def on_message_delete(message):
    logs_channel = bot.get_channel(logs_channel_id)
    
# vérifier si message système ou message bot pas faire de logs
    if message.is_system():
        return
    
    if message.author == bot.user:
        return

# récupérer infos du message supprimé
    username = message.author.name
    display_name = message.author.display_name
    user_id = message.author.id
    name = f"{display_name} ({username})"
    local_time = message.created_at.astimezone(paris_timezone)
    date = local_time.strftime("%A %d %B %Y")
    date_2 = local_time.strftime("%Hh%M")
    date_footer = local_time.strftime("%d/%m/%Y %Hh%M")

# créer l'embed
    embed = discord.Embed(
        description=f"Message de {message.author.mention} supprimé dans <#{message.channel.id}>:",
        color=discord.Color.from_rgb(*rgb_color_message_delete)
    )


    embed.set_author(name=name, icon_url=message.author.avatar.url)
    
    content = message.content if message.content else "Contenu du message vide"
    embed.add_field(name="Contenu du message", value=content, inline=False)
    embed.add_field(name="Date", value=f"{date} à {date_2}", inline=False)
    embed.add_field(name="ID", value=f"```js\nUtilisateur = {user_id}\n```")
    embed.set_footer(text=f"{bot.user.name} • {date_footer}", icon_url=bot.user.avatar.url)

# envoyer dans le salon log
    await logs_channel.send(embed=embed)


# vérifier si message édité, si oui envoyer le message d'avant et d'après dans log
@bot.event
async def on_message_edit(message_before, message_after):
    if message_after.is_system():
        return
    if message_after.author == bot.user:
        return
    
    logs_channel = bot.get_channel(logs_channel_id)
    username = message_after.author.name
    display_name = message_after.author.display_name
    user_id = message_after.author.id
    name = f"{display_name} ({username})"
    channel_id = message_after.channel.id
    guild_id = message_after.guild.id
    message_id = message_after.id
    local_time = message_after.created_at.astimezone(paris_timezone)
    date = local_time.strftime("%A %d %B %Y")
    date_2 = local_time.strftime("%Hh%M")
    date_footer = local_time.strftime("%d/%m/%Y %Hh%M")

# créer l'embed
    embed = discord.Embed(
        description=f"Message de {message_after.author.mention} édité dans <#{message_after.channel.id}>:",
        color=discord.Color.from_rgb(*rgb_color_message_edit)
    )

    embed.set_author(name=name, icon_url=message_after.author.avatar.url)
    
    embed.add_field(name="Message original", value=message_before.content, inline=False)
    embed.add_field(name="Message édité", value=message_after.content, inline=False)
    embed.add_field(name="Date", value=f"{date} à {date_2}", inline=False)
    embed.add_field(name="Lien du message", value=f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}", inline=False)
    embed.add_field(name="ID", value=f"```js\nUtilisateur = {user_id}\n```")
    embed.set_footer(text=f"{bot.user.name} • {date_footer}", icon_url=bot.user.avatar.url)

# envoyer dans le salon log
    await logs_channel.send(embed=embed)



# lancer le bot
bot.run(os.getenv('TOKEN'))