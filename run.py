
import os
import sys
import time
import asyncio
import discord
from discord.ext import commands
from xml.sax.saxutils import escape
from xml.sax.saxutils import unescape

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

"""async def fonc_exemple(message):
    print("test\n")
    msg = 'Hello {0.author.mention}'.format(message)
    await client.send_message(message.channel,msg)"""

CMD_PATH='./bot_files/cmd.pkl'

"""-------------gestion de la base de donnée---------------"""


"""----------------gestion des commandes-------------------"""

# supprime les n derniers messages (et l'appel à la fonction)
async def clear(message):
    all_messages = client.messages
    target_channel = message.channel
    
    counter=1
    m=message.content.split()
    print(message.author,' supprime les ',m[1],' derniers messages\n')
    try:
        max= int(m[1])+3
    except Exception:
        await client.send_message(message.channel, 'vous devez entrer un int. exemple !clear 9')
    if(max > 10):
        max = 12

    for message_step in reversed(list(all_messages)):
        if (message_step.channel == target_channel ):
            
            if(counter>=max):
                print('\n')
                return
            await client.delete_message(message_step)
            if(counter  == 1):
                print(' supression de la commande')
            elif(counter <= max -1):
                print(' supression du message n°',max-counter)
            counter = counter+1


#ajoute une commande à la liste des commandes du bot TODO
async def addcmd(message):
    m=message.content.split()
    
    if (len(m)!=3):
        await client.send_message(message.channel,'mauvaise syntaxe,la commande !addcmd est de la forme !addcmd #cmd_name # cmd_message')
        return
    
    print('ajout de la commande ',m[1],'->',m[2],':' )



# switch pour les differentes commandes
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    author = message.author
    """if message.content.startswith('!test'):
        await fonc_exemple(message)"""
    if message.content.startswith('!clear'):
        await clear(message)
    if message.content.startswith('!addcmd'):
        await addcmd(message)

# ceation du dir pour le bot si necessaire
file_bool = os.path.exists("./bot_files")
if not file_bool:
    os.system('mkdir ./bot_files')

# login et lancement du bot
client.login('token')
client.run('MjI4NTU3MjQwNjIwMDIzODA4.CtEWMg.xvkO6IlHuhduLqYw7WmOBUtjjHs')


