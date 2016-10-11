
import os
import sys
import time
import asyncio
import discord
import pickle
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
GOD_PATH='./bot_files/ptgodwin.pkl'

"""-------------gestion de la base de donnée---------------"""

def save(dict, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(dict, f, pickle.HIGHEST_PROTOCOL)

def open_dir(file_path):
    file_bool = os.path.isfile(file_path)
    if file_bool:
        with open(file_path, 'rb') as f:

            return pickle.load(f)
    else:
        return None

def build(file_path):
    path_bool = os.path.isfile(file_path)
    if not path_bool:
        data_dict = {}
    else:
        data_dict = open_dir(file_path)
    return data_dict


"""----------------gestion des commandes-------------------"""

#parcour de la liste des commandes
async def cmd(message):
    m=message.content.split()
    if (len(m)==1):
        print("reception d'un message de taille 1")
        cmd_dir = build(CMD_PATH)
        #TODO limiter la recherche à des message commencant par '!'
        if cmd_dir.get(str(m[0])):
            print(" cmd trouvée")
            await client.send_message(message.channel,str(cmd_dir.get(str(m[0]))))
        else:
            print(" pas de cmd trouvée")

async def addcmd(message):
    m=message.content.split()
    #TODO mettre dans m[2] tout le message
    if (len(m)<3):
        await client.send_message(message.channel,'mauvaise syntaxe,la commande !addcmd est de la forme !addcmd #cmd_name # cmd_message')
        return
    print (m[2])
    m[2]= ' '.join(m[2:])
    print('ajout de la commande ',m[1],'->',m[2],':' )
    # TODO verification de la syntaxe des commandes
    cmd_dir= build(CMD_PATH)

    print ("    verification de l'existance de la commande")
    if cmd_dir.get(str(m[1])):
        print ('        la commande existe deja')
        await client.send_message(message.channel,'la commande existe deja')
    else:
        cmd_dir[str(m[1])]=str(m[2])

    save(cmd_dir,CMD_PATH)
    print('commande',m[1],'->',m[2],'ajoutée')
    await client.send_message(message.channel,'commande ajoutée')

# supprime la commande dans la liste
async def delcmd(message):
    m=message.content.split()
    if (len(m)!=2):
        await client.send_message(message.channel,'mauvaise syntaxe, la commande !delcmd est de la forme !delcmd #cmd_name')
        return
    print('suppression de la commande',m[1],':')
    cmd_dir=build(CMD_PATH)

    print ("    verification de l'existance de la commande")
    if cmd_dir.get(str(m[1])):
        print ('        la commande existe')
        del cmd_dir[str(m[1])]
        save(cmd_dir,CMD_PATH)
        await client.send_message(message.channel,'commande supprimée')
    else:
        print("     la commande n'existe pas ")
        await client.send_message(message.channel,"la commande n'existe pas")

# gestion des points godwin
async def godwin(message):
    m = message.content.split()

    if (len(m)!=2):
        await client.send_message(message.channel,'mauvaise syntaxe, la commande !delcmd est de la forme !godwin #user_name')
        return
    print("essail d'ajouter un point Godwin à ",m[1],':')
    cible = None
    for member in message.server.members:
        if member.name==m[1]:
            cible= member
            break
    if cible==None:
        print(' client non trouvé')
        await client.send_message(message.channel,"Personne n'a ce nom sur le serveur")
        return
    godwin_dir=build(GOD_PATH)
    if godwin_dir.get(str(m[1])):
        godwin_dir[str(m[1])]+=1
    else:
        godwin_dir[str(m[1])]=1
    save(godwin_dir,GOD_PATH)
    print('point attribué')
    messretour = "Félicitation "+str(m[1]+" cela vous fait "+str(godwin_dir[str(m[1])])+" points Godwin!\n  http://publigeekaire.com/wp-content/uploads/2011/04/point-godwin.jpg  "
    await client.send_message(message.channel,messretour)


# supprime les n derniers messages (et l'appel à la fonction)
#TODO limiter les message que l'on peut supprimer
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
    if message.content.startswith('!delcmd'):
        await delcmd(message)
    if message.content.startswith('!godwin'):
        await godwin(message)
    else:
        await cmd(message)


# ceation du dir pour le bot si necessaire
file_bool = os.path.exists("./bot_files")
if not file_bool:
    os.system('mkdir ./bot_files')

# login et lancement du bot
client.login('token')
client.run('MjI4NTU3MjQwNjIwMDIzODA4.CtEWMg.xvkO6IlHuhduLqYw7WmOBUtjjHs')
