import discord
from discord.ext import commands
import os
import random


client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot ready")

@client.command()
async def awy(ctx):
    awyQuotes = ['MONSTRUJM',
    'biopolar or smth',
    'im such a god of english language',
    'sign of asking',
    'i am "CHAOTIC EVIL"',
    'i do not classify myserlf as good person',
    'she is prettending to be villian like i was to make that lesbo realise her true sexual envoirment',
    'why you  heff to be so mad at me all the time',
    'IM MMATURE',
    'i would gladly be  at the bottom if we talkin some bigass latina chick',
    'satan himself will get borred of trying to tourment me',
    'but you be pullin some Merlin shit summoning excalibuyrs worry not',
    'CENE YOU ARE MARIA TERESA',
    'well ye i cheated on her but like cmone she has allready girlfriend if i find another one to throw asidewhy shodln\'t i 2000 iq decision making',
    'she left me saying that i am d og shit',
    'sh was bisexual and hed lesbian girlfriend',
    'Is brnabic fokin tranvestit ?',
    'like ma useless old men says "everyone washappy with pay checks in communism now they talk shit"',
    'O PARTIGANOOOO,PORTAMI VIAAAAAA',
    'i even got called by ma girl friend a "man whore "',
    'we\'ll invite our boi Dran to gather up mats',
    'looks like i have to educate you',
    'it\'s better strategy than telling  them that they are single atomed  ameba only for them to go from 0/5 to 0/10',
    'did you treshtalck me',
    'you can\'t determine who\'s a selfish scumbag and who\'s selfless good guy if you only try to se good in them',
    'well i always try to see the worst in people first,that way you get much more realistic vision of them and don\'t get hopes up for them to in the end dissapoint you',
    'seggy is understanding how the world is functioning',
    'poland seems like a rational and family friendly country',
    'oh in Serbia violence is only way of solving things like gypsy steals your byciyle what would you do ?\nask him to return  it ? FUCK NO\ncall the police ? EVEN MORE FUCK NO\nYou go and get your shit bag',
    'who\'d have thought that retarded child predator Protein that was fanatic about fking hide n seek on neltharion would become administrator after his daddy doanted big money and he licked the asses of other admins',
    'mel always comming by when you mention "the betrayer"',
    'in Serbia we get into psyhical alteracation with peeps like that aka we break their legs',
    'you always start with beer and league then you finish with rakija save the best for the end',
    'hee did he sad bad things to about ma momma and told me that he is going to stab me in the dark\nso i beat him\nand told him that he\'s gonna be  the one who gets stabbed\nso he shit himself and reported me\nthey even wanted to give me house prison with a fking shit on leg\ni had to go to bank to get credit for a motherfucking lawyer\ndamn pussys',
    'yo know in serbia we have a tradition where when there is female singer you give her monney for song\nbut it\'s like 5 to 10 eruos\nbut i was like pushing 50 euros into her tits',
    'well yeh but i allready got permad few times and few 6 month bans so i have 2 alts\nHE HE',
    'the fking guy could make a movie about teletubbies and super mario and make it to be epic and best out there',
    'tho that system for banning is to retarded\nlike sure i tell ppl to go and buy artifical arms on ebay and brain cells\nsure i tell them that they are grass eating animals and dumb motherfuckers\nbut all the time toxic ppl are like "AA FUCK YOUR MOM,AAA WISH YOU CANCER FOR YOUR FAMILY AAAA KILL YOURSELF"\ni never insulted anyones family or smth i just tell ppl that they are dumb fucks\nand mostly those toxic ppl above get triggered and report me and i get banned they do not\nit\'s stuipid\ni mean telling somone that he is dumb is a fact not so much of an insult like wishing him and his family misfortune',
    'Awy is not savage\ncene we Serbs are maybe poor\nbut we aint no mongoloids',
    'Fuck it why would i buy shadowlands when i can go on facebook and build up ma goddamn farm on farmvile\nor play that tower climb\nshit',
    'why are league pl players becoming even stuipider\nyou guys are becoming more mentally disabled then us Serbs',
    'hmmm this morring pigeon flied into my room\n',
    'he had some avatar on dsicord of SS army or somethig,pretty good behaivour of an staff member gj warlame',
    'that retard was saying in a room full of people that Hitler was verry smart man and that they should let him exterminate gypsies and Serbs and jews\nthen he said something about ma momma\nso i said that it\'s not his fault for being degenerate\nand that it\'s his mother\'s fault for releasing such a disgusting thing in this world',
    'but yeh it is wat it is',
    'Once i found reasonable polish player and he told me this "i no spik ing, i pl"',
    'when you see retarded imbecile you can\'t really try to reason with him',
    'I JUST SAID "fuck off degenerates"\nand bem riot gave me a big NONO for that',
    'this one is just for you,this is how tru serbs looks like,carrying machetes and drinking vodka vodka\nhttps://image.prntscr.com/image/llvyhI-RTXK7aK-HMGVidA.png',
    'https://image.prntscr.com/image/yOEamt6ZTIypMNXKWQIBHg.png'
    'https://media.discordapp.net/attachments/364712407601512450/719636503676059668/Screenshot_1469.png?width=931&height=515',
    'https://media.discordapp.net/attachments/364712407601512450/719636518758777003/Screenshot_1470.png']
    rolled_quote = random.choice(awyQuotes)
    if rolled_quote.startswith('http'):
        await ctx.send('rolled_quote')
    else:
        await ctx.send('Awy once said: "{}".'.format(rolled_quote))

@client.command()
async def akcent(ctx):
    await ctx.send('https://prnt.sc/udv05c')

@client.command()
async def stonelia(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/709413405131407380/Screenshot_794.png?width=686&height=515')

@client.command()
async def pempem(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/752975692966264902/Screenshot_797.png?width=684&height=515')

client.run(os.environ['DISCORD_TOKEN']) #token