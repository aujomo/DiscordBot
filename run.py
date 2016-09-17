
import sys
import discord


# Disables the SSL warning, that is printed to the console.
#import requests.packages.urllib3
#requests.packages.urllib3.disable_warnings()
client = discord.Client()

def fonc_exemple(message):
    client.send_message(message.chanel,"It's a TEST!!!")


#alerte de connection
@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

# switch pour les differentes commandes
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    author = message.author
    if message.content.startswith('exemple'):
        fonc_exemple(message)



# login et lancement du bot

if len(sys.argv)<4 :
    sys.exit("you need to enter your login, pwd and the serv invite")

client.login(sys.argv[1], sys.argv[2])
client.accept_invite(argv[3])
client.run()


