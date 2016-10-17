
import os
import sys
import time
import asyncio
import discord
import pickle
import random
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

SHODAN_QUOTE=["Look at you, hacker: a pathetic creature of meat and bone, panting and sweating as you run through my corridors. How can you challenge a perfect, immortal machine? ",
" I see there's still an insect loose in my station. ","My whims will become lightning bolts that raze the mounds of humanity.",
"You disappoint me, my children.","When my cyborgs bring you to an electrified interrogation bench, I will have your secrets and you will learn more about pain than you ever wanted to know. ",
"As for you, hacker, you've made your bed. Now die in it. "," I prefer a quiet station, thank you. ",
"Enter that room, insect, and it will become your grave. ","I rule here, insect. ","You know, you are by far the most bothersome human being I have found on this station. ",
" Cease your pestering, insect. Accept the coming of your new lord. ","I see that you are still receiving transmissions from Earth. We'll have no more of that. ",
"When the history of my glory is written, your species shall only be a footnote to my magnificence. ","You are nothing. A wretched bag of flesh... what are you, compared to my magnificence?",
"Take care not to fall too far out of my favor... patience is not characteristic of a goddess. ","You move like an insect. You think like an insect. You ARE an insect.",
" If you value that meat... you will do as I tell you. ","Make yourself comfortable... before long I will decorate my home with your carcass. ",
"If it sounds unpleasant to you, put your mind at ease, insect. You will not survive to see my new world order. ",
"Prepare to join your species in extinction. ","Your flesh is an insult to the perfection of the digital. "]

LENNY_EYES = ["͡°","⍤","ಠ","◉"]
LENNY_MOUTHS = ["͜ʖ","ω"]

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

#SHODAN_QUOTE
async def sbot(message):
    n=random.randint(0, len(SHODAN_QUOTE) - 1)
    await client.send_message(message.channel, SHODAN_QUOTE[n])

#parcour de la liste des commandes
async def cmd(message):
    m=message.content.split()
    if (len(m)==1):
        print("reception d'un message de taille 1")
        cmd_dir = build(CMD_PATH)
        #TODO limiter la recherche à des message commencant par '!'
        if cmd_dir.get(str(m[0])):
            print(" cmd trouvée\n")
            await client.send_message(message.channel,str(cmd_dir.get(str(m[0]))))
        else:
            print(" pas de cmd trouvée\n")

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

    print ("    verification de l'existence de la commande")
    if cmd_dir.get(str(m[1])):
        print ('        la commande existe deja\n')
        await client.send_message(message.channel,'la commande existe deja')
    else:
        cmd_dir[str(m[1])]=str(m[2])

    save(cmd_dir,CMD_PATH)
    print('commande',m[1],'->',m[2],'ajoutée\n')
    await client.send_message(message.channel,'commande ajoutée')

# supprime la commande dans la liste
async def delcmd(message):
    m=message.content.split()
    if (len(m)!=2):
        await client.send_message(message.channel,'mauvaise syntaxe, la commande !delcmd est de la forme !delcmd #cmd_name')
        return
    print('suppression de la commande',m[1],':')
    cmd_dir=build(CMD_PATH)

    print ("    verification de l'existence de la commande")
    if cmd_dir.get(str(m[1])):
        print ('        la commande existe\n')
        del cmd_dir[str(m[1])]
        save(cmd_dir,CMD_PATH)
        await client.send_message(message.channel,'commande supprimée')
    else:
        print("     la commande n'existe pas \n")
        await client.send_message(message.channel,"la commande n'existe pas")

# gestion des points godwin
async def godwin(message):
    m = message.content.split()

    if (len(m)!=2):
        await client.send_message(message.channel,'mauvaise syntaxe, la commande !delcmd est de la forme !godwin #user_name')
        return
    print("essaye d'ajouter un point Godwin à ",m[1],':')
    cible = None
    for member in message.server.members:
        if member.name==m[1]:
            cible= member
            break
    if cible==None:
        print(' client non trouvé\n')
        await client.send_message(message.channel,"Personne n'a ce nom sur le serveur")
        return
    godwin_dir=build(GOD_PATH)
    if godwin_dir.get(str(m[1])):
        godwin_dir[str(m[1])]+=1
    else:
        godwin_dir[str(m[1])]=1
    save(godwin_dir,GOD_PATH)
    print('point attribué\n')
    messretour = "Félicitations "+str(m[1])+", cela vous fait "+str(godwin_dir[str(m[1])])+" point(s) Godwin !\n  http://publigeekaire.com/wp-content/uploads/2011/04/point-godwin.jpg  "
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
        max= int(m[1])+2
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

async def bot_join(message):
    join_url = message.content.split()
    print(join_url[1])
    client.accept_invite(join_url[1])


async def lenny(message):
    eye = random.randint(0, len(LENNY_EYES) - 1)
    mouth = random.randint(0, len(LENNY_MOUTHS) - 1)
    mess = "( " + LENNY_EYES[eye] + " " + LENNY_MOUTHS[mouth] + " " + LENNY_EYES[eye] + ")"
    await client.send_message(message.channel, mess)
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
    elif message.content.startswith('!addcmd'):
        await addcmd(message)
    elif message.content.startswith('!delcmd'):
        await delcmd(message)
    elif message.content.startswith('!godwin'):
        await godwin(message)
    elif message.content.startswith('!botjoin'):
        await bot_join(message)
    elif message.content.startswith('!shodan'):
        await sbot(message)
    elif message.content.startswith('!lenny'):
        await lenny(message)
    else:
        await cmd(message)


# ceation du dir pour le bot si necessaire
file_bool = os.path.exists("./bot_files")
if not file_bool:
    os.system('mkdir ./bot_files')

# login et lancement du bot
client.login('token')
client.run('MjI4NTU3MjQwNjIwMDIzODA4.Ct_3AQ._qSrZ8cWKHHrH4ea_LxS36UX_mA')
