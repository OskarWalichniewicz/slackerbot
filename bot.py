import discord
from discord.ext import commands
import os
import random
from datetime import date, datetime, timedelta
import json
from github import Github


segmentQuotes = ['Imma Kamehameha yo ass if you don\'t behave kids!',
    'We fucking invented it you swine!']
awyQuotes = ['MONSTRUJM',
    'GOUVERMANT IS LYING TO HER',
    'btw srecna nova srpska nova bato sve najlepse :heart: !',
    'biopolar or smth',
    'he\'s even civilizaed citizen of UK man\nhe be probably at queen\'s house drinkin\' da tea like a true boss',
    'bobbsy\'s opinion is much more better than some lame ass test',
    'SO NOT ALL SERBS ARE MOLESTERS ? lIKE THAT MONSTRUM',
    'ONLY DELEAR IS DRUG DEALER',
    'BOBSY I WILL PROTEC YOU',
    'seggy do you wanna se magic ?',
    'sorry i aint no gae',
    'my bad is empty',
    'when i was in highschool there was this caffe called Omerta i was there 24/7 and there were always chicks calling me psychologist and comming to talk to me about their problems for me to help them',
    'DONI',
    'PUSTA ULICKA CRNJE S PRAZNICJNJE VECER KURWAAAAA',
    'cunt you are only calling me bcs you need support',
    'my rank 1 supporting skills are not for everyone',
    'dont worry cringe is having new definition with that cute girl stalking me\nshe wrote a roman to me ABOUT HER STORIES ON GEOGRAPHY TOURNAMENT\nand i was like left speechless after that',
    'cringe is back :unamused:',
    'ofc no i suck so much',
    'I CHOSE YOU SHATAN UDACHI',
    'i installed it yesterday and im allready regreting',
    'fuck me',
    'i raped the motherfucking rat',
    'another shitty day incoming,fuck this "winter" i want spring and summer',
    'well you are a traitor fu',
    'that\'s what happens when you play in whorde',
    'nono dont only look at hot girls dont make same mistakes like i did i watched boobs and arse and i am not rly happy with my love life you know',
    'with heroin you sleep like a baby to',
    '1 is becoming alcoholic second is becoming romantic',
    'next step is most important you talk with her and you hug her if she is not resisting it means she is all yours\nyou know like you sit close to her and listen to her and you face her and listen to her carefully you hug her after some time you take her even closer to ya and you kiss her',
    '= if you dont fking kiss her\ni will kill you',
    'im your man i can make you a fking don juan arogant bastard or a lovely dovely romeo',
    'you will show your love with singing',
    'i will teach them the lesson dont be magicni',
    'next time i will open their heads for beign pussys',
    'to manny of magicni\'s in this world',
    'https://www.youtube.com/watch?v=nK7arpkUg4Q',
    'but actually she was not that ugly but you know i wanted long and stable relationship you know and after 4 months of trying to make that happen and see my mistake i just stoped giving fuck so i just groped mangulica you know',
    'best new year ever ahh,drinking,nice atmosphere and all that gud shit you know\nmangulica was there to make it even better',
    'mangulica=a sort of pig you know',
    'NONO my ex was drunk\nbig boob girl was sober as fuck\ni mean she even remembered my name and come to stalk me on instagram you know\nbut rly eybrows like a god damn mangulica',
    'do i seem like i care ? I cared enough she didnt appriceti it so fk her',
    'you can become a real man and real bruda if you are guided by me',
    'and new horizons of that flat chick with big boobs opened for me on new year\'s celebration you know\ni can feel them even 9 days later',
    'real man when break up with 1st gf listen to this shit,They dont treat that they will cut their veins right',
    'your Serbian is better than Vuk Karagic\'s and he like invented Serbian alphabet and half of our words you know\ni never heard him speaking it bcs he lived few ceuntries back but i ensure you you are better',
    'you must eat',
    'drugs and alcohol can\'t rly be a source of your hapiness or pleasure in life',
    'if  somone would kill this creature and like cook him,half of ethiopia would be fed',
    'euforija na krevetu moja teritorija',
    'my mother would sent me to white monastery so those bald guys would hit me with shovel in the head',
    'well it\'s probably either because you are to weak atm xD (no ofense just the way it is) or you were not breathing correctly',
    'you must get pust your limits but also sometimes you must be beware of them',
    'like it matters who started it\'s like kids in kindergarden HE STARTED nono HE DID',
    'windof change>every other scorpion song',
    'you are lazes all the time',
    'omg you lier\nyou are bigger traitor and lyier than melanie\ni cant belive it',
    'kokoska mount !',
    'cene if you want i will avange you and i will commit a genocid against fking kobolds',
    'you need to learn how to hold your inner kurwa in ma polish bruda you know\ncontrol it\nunleash it only on wylder and ignios',
    'you betreyd me\ni am not your aprrentice anymore',
    'nono i cant be podanik tame you can only be podanik tame you are lier i am not',
    'i am to pissed of to deal with traitors as well',
    'you start with pushing it down as much as you can\nand you slowly break it down',
    'now you \'re yellow',
    'i will just remind you that for pedophile you can even get 8 years',
    'i am sorry cene for listening to your singing or talking to you\ni wont do it anymore\nso please forgive my sins',
    'at least it\'s better than that fking jala brat fag',
    'lol why would you keep thing like that from your mom',
    'i invented gas methods\nyou cunt',
    'ok you wanna solve it ? I will solve this right now i litteraly DONT GIVE A FK if you belive me or not LITTERALY 0 FK GIVEN when you understand that 2nd thing to understand is THAT I DONT GIVE A FK TO LIE TO YOU AS WELL litterally once again 0 FK GIVEN I DONT CARE TO GIVE YOU FALSE HOPE OR WHHATEVER,so now when SOLVED THIS into SIMPLE POINTS i hope you understand it now',
    'you push it down as much as possible until you can put yourself down',
    'breathing is the key thing to reaching high stamina',
    'i had bleads on the guy\nAND CENE USED BLIND ON HIM\nand he says it\'s my fault',
    'im going with Vule to deal with some 13 years old bastards who were bullying his 7 yo sister',
    'when you are at pause\nyou inhale with mouth  and exhale with nose\nthat way you are making your blood preasure stable',
    'just listen to the mighty awy i can make you either like Dwayne Rock or just definiton',
    'cant gass d furherer',
    'bend your bacck ?',
    'like it\'s MOST IMPORTANT RULE you must get enough of Proteins and hydrats\nugljeni hidrati',
    'eating is idk\nbiggest source of hapiness in this world',
    'pushups=triceps,chest and back',
    'start doing pull ups as well it\'s not rly smart idea to have triceps while biceps is non existent',
    'father of my best friend with a broken leg litteraly destroyed leg opened the head of 3 officers\n1 of them had 9 head surgerys to keep his head in place\nwell now he is serving for that',
    'nono we will make to much colors it will be like a rainbow\nwe are not homosexual',
    'WHY DOES EVERY MIDGET HAVE SO MUCH ANGER BUILT UP INSIDE THEM',
    'you must breathe',
    'how can you not bee in mood to eat',
    'I LOVE YOU TO MAN\nYOU ARE MY MAN',
    'HS is a game for junkies proven',
    'you know cene we have kkinda friend who is 36 years old spent 90% of his adulthood in prison they call him litteraly ROW',
    'PIGS HUNTING AN PIG\nSINGLE PIG WINS',
    'i am getting orgasams as i eat it,love it so much man',
    'vanilla pudding mmm',
    'you must win her,dont fail me',
    'wait how do you even spell puding on english',
    'you remember ashelyn ? Retardin from slackers whom /gquited bcs of me and raged so much and sent me 1000 gold with mail saying "HERE THIS IS FOR YOUR CANCER I HOPE YOUR WHOLE FAMILY DIES FROM IT YOU FAGGOT"',
    'i left the wow to watch cowboy bebop',
    'sing boku no pico theme',
    'my condolences man :/',
    'ah so good went to both of my grandparantes eated like an animal and earned 30 euros',
    'you have to fail before you manage to complish something',
    'i love myself to',
    'one day i will master the grammar',
    'i dont eat tablets anymore',
    'you were even more cryinger than normally :smile:',
    'you\'re the beast man\nwulferin\nwulf wulf\nwait how the fk is that even writen\nwulferin\nwulverin * guy with claws\nWOLVERINE\ni knew it was something wulf wolf wolv wulv wulf or similar',
    'rasta wont put his dick into that nice hole anymore,poor guy :/',
    'i remember when i was playing guitar this was my 1st metallica song\ni was so proud of myself\nat that time',
    'WHAT IVE FELT WHAT IVE KNOWN TURN THE PAGES, TURN THE STONE COULD YOU BE THERE CAUSE IM THE ONE WHO WAITS THE ONE WHO WAITS FOR YOU',
    'when i broke up with my first gf i was like OMG I WILL BE DEPRESED NOW you know so i listened to unforgiven 2 and whoaring streets',
    'andrenalin boost 101%',
    'do you know that rasta and ana nikolic broke up\nthey will devorse',
    'shame they have small number of sungs',
    'dont you fk with me',
    'well im guitarist which got inspared by thresh metal and nu metal duo of Malakian and that RATM guy',
    'MY COK CAN WALK RIGHT THROUG THE DOOR',
    'cene the master mathematitian',
    'shut up fossil you be like 70 centuries +',
    'https://prnt.sc/hwzx35',
    'MY COOK IS MUCH BIGGER THAN YOURS',
    'ehmm @Cene the Kokoska  you dont mind hitler emoji ?',
    'you really added fking porn bot',
    'piratebay is your friend',
    'DANI BOI IS PENSION GOIN AIGHT ?',
    'lol im poor as well i give you gold i be even more poor',
    'fk you kole you are NEOBRAZOVAN',
    'seggy should be on sucidial hotline in USA',
    'you could cap with your best friend Ignios and be rogue mage cancer comp',
    'lol if he is a cancer if you dont give a fk if it does not matter then why bothering to talk with him why bothering to display  fake feeling or idk what to him',
    'now that we saw picture of your cook can we see your ass to',
    'oh my grammar was so good in this sentance that i cant understand it either',
    'you are becoming like those sluts poping ases so they could like whoar you know',
    'i was playing the guitar for 6 years and i was verry talanted and i had long fingers so i had very good starter but in the end stoped that',
    'my father was metalhead for whole his life so when i was born he thought me to be metalhead as well i was',
    'you thought me to be abetter person so dont remind me of ma bad sides',
    'Magicni became soad fun because of me to\ntho he was mainstream fuck\nhe was all like TOXICITYYYY CHOP SUEEY IM BADASS NOW',
    'you know cene you could do a duet with kole\nsing to titanum or something',
    'emotinal rollercoster he was writing about his father which spent 90% of his life in prisons',
    'first time i was insulting somone with so many bad words and i never felt even 1% bad for it',
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
    'well yeh but i allready got permad few times and few 6 month bans so i have 2 alts HE HE',
    'the fking guy could make a movie about teletubbies and super mario and make it to be epic and best out there',
    'tho that system for banning is to retarded\nlike sure i tell ppl to go and buy artifical arms on ebay and brain cells\nsure i tell them that they are grass eating animals and dumb motherfuckers\nbut all the time toxic ppl are like "AA FUCK YOUR MOM,AAA WISH YOU CANCER FOR YOUR FAMILY AAAA KILL YOURSELF"\ni never insulted anyones family or smth i just tell ppl that they are dumb fucks\nand mostly those toxic ppl above get triggered and report me and i get banned they do not\nit\'s stuipid\ni mean telling somone that he is dumb is a fact not so much of an insult like wishing him and his family misfortune',
    'Awy is not savage\ncene we Serbs are maybe poor\nbut we aint no mongoloids',
    'Fuck it why would i buy shadowlands when i can go on facebook and build up ma goddamn farm on farmvile\nor play that tower climb\nshit',
    'why are league pl players becoming even stuipider\nyou guys are becoming more mentally disabled then us Serbs',
    'hmmm this morring pigeon flied into my room',
    'he had some avatar on dsicord of SS army or somethig,pretty good behaivour of an staff member gj warlame',
    'that retard was saying in a room full of people that Hitler was verry smart man and that they should let him exterminate gypsies and Serbs and jews\nthen he said something about ma momma\nso i said that it\'s not his fault for being degenerate\nand that it\'s his mother\'s fault for releasing such a disgusting thing in this world',
    'but yeh it is wat it is',
    'Once i found reasonable polish player and he told me this "i no spik ing, i pl"',
    'when you see retarded imbecile you can\'t really try to reason with him',
    'I JUST SAID "fuck off degenerates"\nand bem riot gave me a big NONO for that',
    'ya all must admit that your lifes would be borring without ma ass im such a good guy for making it so colorfull for you',
    'HELLO YOU SLACKERS',
    'BETRAYEEEEEER',
    'deni d betreyer',
    'when i saw fotage of that guy explaining that\nactually that cocksucker\ni knew that it is the end for wow',
    'DENI ANSWER ME\nDENI\nBETRAYER\nCOME ON\nCOME DENI BOI',
    'COME TO YA BRUDA',
    'OUR BOI DANI WAS IN HOMO RELATIONSHIP WITH WYLDER',
    'DRUNK CENE SCREAMING AT GIRLS ON STREET\nMAKE THEM RUNAWAY\nHAHAHAHAHHA',
    'cmone Dani dont be a asshole',
    'you are from Netherland\nand you are DAni\npretending to be female\nyou gay\naint ya\nbusted',
    'cmone Dani dont be a asshole',
    'Dranerys you can always be the leader of the pack again\nthe ledear of mongoloids',
    'legends never change ma bruda\neven when i get old like 60 years old i\'ll tell ma grandchildren yo you little shits\nsit down let the grandpapa tell ya few stories',
    'there aint medicine for me',
    'everything is pretty everything is nice so peacfull',
    'jk im kinda peacfull atm im starting to look at the world with difrent eyes ya know',
    'im having fking trial next week for fking "MASS" injuries\nor heavy idk how is it in english fking law\ndamn motherfuckers they never learn',
    'i had girlfriend for fking 6 months after dozens of one night stands hi hi hi',
    'im MMA boxer dude and  had 2 year course of russian system\nkung fu is like biggest lie after aikido they fking tell the kids they can disarm a pistol with fking one finger\nand stuipid parents send their children there and then they wonder why the fk they end in fking hospital\nstuipid cocksucker\ns',
    'he like just started streaming\nthere were only like 300-400 ppl online and i just told him the truth\nthat he sucks so much and that pilav is the BEST !\nand he kinda got triggered\nam even amazed he managed to read my msg',
    'rank 1 rogue\nself proclaimed actually',
    'just toma kicked us bcs we act like children from her kindergarden\nand mel approved tha\nt',
    'we are reasembling SLACKERS\nbut we will find original name like TRU BRUDAS',
    'lol segment\nsuch a undusrtandable person\nis my bruda from italia',
    'I GOTTA THINK OF A FUTURE\ni must be responsoble man once in my life',
    'and you get to ride with stinky grandmas\nwho took bath last time in 1944 before the end of WWII',
    'actually it\'s my ex so she would greet us with some sharp item but ok',
    'cene one day we will go on slackers tour i wil collect like 200 euros f or gas\nAND WE WILL GO TO SPAIN\nNETHERLANDS\nITALY\nPOLAND\nCOLLECTING ALL DA SLACKERS\nTHEN WE WILL GO TO BULGARIA AND HANG OUT WITH OUR BFF WYLDER AS WELL\nTHEN VISIT KASPI IN GERMANY\nTHAT IS MY MASTER PLAN HAAAAAAAAAAAAAAAAAAAAA',
    'we were like OH WE ARE BORRED LETS GO TO SOME FKD UP VILLAGE AND DRINK A COFFE',
    'cene you are having some badass kokoska on avatar',
    'Slackers dieded the moment me cene and akcent left it\nand seggy',
    'are you still having that BF who is like 10 ranks lower than cene and still beating him in HS',
    'oh yes she is also very pretty until she starts talking',
    'whorde AH even worser shit than aliances',
    'whanna come to aliance side now ? i wasnt there the othger day',
    'i havent heard your angelic voice in years\ni mean ages',
    'Happy Valentines day',
    'im leveling ma invisible cancer',
    'why are you not playing anymore,we must rape whorde for the bruda segment',
    'psst dranerys i just watched klip it goes like "TANK YOU FUKING BRAINLLES BITCH" and then some serbian swears',
    'fk spotify\nwindows media player ftw',
    'if i hang up on my gf to talk witth you she will think that im banging some whore',
    'you know till like 14:00 pm there was litteraly 0 work i was chilling with  da boss drinking Rakija smoking cigars all that good shit we were chilling',
    'you hear that russian bois\njust got out of pussy screaming CYKA BLYAT RUSH B I FUCKED YUR MUM',
    '[14:52:32] Restodude has defeated Echøzeus in a duel\nonce again i am releasing justice for cene',
    'you bycile riding people are negative',
    'damn it was my friends birthday i got destroyed,holy shit she was hot af\ni wont drink anyomre !',
    'contradicting\nwhat does that mean\nmel you have to use simple words here\nyou know\nim SLAV MAN',
    'we are slavs\nwe only do slav squats\nand drink vodka\nwe dont use complicated words',
    'i think kohai will get mad\ni changed her nickname to Alcoholic',
    'we were going around with shovels from like 4 AM till 7AM iand it was summer so we was like fk it let\'s go and chill somewhere',
    'once we got drunk at his house  you know and he was like SOMONE KILLED MY CAT WE HAVE TO AVANGE YOKI so first we dug grave for the cat burried her it took us about 2 hrs to dig hole of 50 cm bcs we were destroyed and then we were runing around with shovels trying to find the killer of Yoki',
    'YO CENE AFTER KOKOSKA\nARE YOU READY TO MEET GOLUB ?',
    'actually there is one guy in background who was arested 1st when he was 11 bcs he hited a professor multiple times with chair',
    'i would love so much to be in that dirty classrom with graphitis\ncuz if we break something none will realase it and we wouldnt pay for dmg',
    'do you want to see recording of me badmouthing Serbian gouvermant',
    'im always bald like a real serbian bruda',
    'im a creative hguy',
    'HE HE\nIM WEJSTAD\ni hold up for whole 19 days without gfetting destrjoedd',
    'yo cene didnt we spit onj him in bg\'s ?',
    'if only me and cene were officers we would made the bestest guild of all times',
    'btw wtf is this kreature thing',
    'one of the biggest was that my ex I MEAN SHE AINT EX ANYMORE  was saying sorry to me and apologized we made up,and she even forget the fact that i basicly cheated on her with that big boob girl',
    'a lot of strange things is happeining recently',
    'holy shit some girl from our hood is 16 yo and had sex with 29 years old guy,damn he could get a big jailtime',
    'that fagot lost ?',
    'no problemo',
    'my top 3 movies 1. Godfather 2. AMerican HIstory X 3.Leon the professional',
    'Amsterdam=legalized=Good',
    'btw cene stfu you have no basis to say bad things about Serbia ,when in poland it\'s normal for 10 yo girls to have sex',
    'if that fagot lose i will find him',
    'well excuse me for beign a poor country',
    'that should be national treassure of serbia\nmy existance shuld actually',
    'why would you cry you lost nothing litteraly\nconfession cant lead to any loss\neither you will win,and get the girl\nor you will just get rejected and get back to what you were',
    'i wanna cry rn cuz maths is fking cancer',
    'fking idiot of a profesor managed to make us write 11 pages A5 format about Bipolar junction transistor and then another 5 about his characteristics',
    'This is Serbia,it\'s the country when there are much of high school dealers',
    'ok im out for coffe gotta make an pause from studying\neven tho i didnt touched a book',
    'stuipid bastard he is anoying as fuck',
    'fking school officer (police officer) there was some fight yesterday in school and HE BROUGHT ME TO TALK LIKE 1ST i was the 1st one to get interogated and i was not even involved,he was like YO I KNOW YOU WERE THERE,and im like giving him negative answers for 10 minutes and then he was like BUT YOU KNOW WHO WAS THERE THEN,and i told him that even if i did know i would definitly tell him (even tho i ofc knew who was fighting with who) and stuipid pig failed for that trick and lket me go',
    'police officer are becoming stuipider every single day,it\'s just getting easier and easier to fk \'em over',
    'oh polish families are best ones,they exchange roles you know,first she gets the beating and then he gets it',
    'i sound like alcoholic who beats his wife on daily basis and im uneducated junkie and my voice SOUNDS LIKE IM 40 wtf ?',
    'you know the most important thing is that i was feeling good at that moment :3',
    'nono i dont look like myself here,i look like an drug addict',
    'it was like summer 2k16 his sister gave a birth so he was happy af becoming an uncle you know and he took at least 10 liters of some prestige shit\'s like some pretty expensive vodka and somethings from his grandfather who is a well known doctor so well',
    'you were a real gangsta since young age ma friend',
    'YO CENE IM PARTYMAKER',
    'im a crazy serbian motherfucker\nwhatt else do you want to find out\nand im serbian junkie bruda',
    'i mean i am totally against violence on girls n women ofc but damn son this junkies are worser than serbain reaility shows',
    'it feels so strange when somone says DS because DS=speed on our slangs speed like white powder of magic',
    'later is non existent the only thing that is real is presence remember that',
    'but idk orochimaru seemd like a nice guy idk why he suddenly started spitting on us i mean yeh we focused him but only cuz he was like only healer in horde for 2 weeks streight',
    'polish brudas are the best brudas,there were 2 of them premading they sucked so hard,losing our game but it was a funny expirience we agreed to spam KURWA to enemy jungler bcs he was titled from start and he started crying and left the game after 20 minutes of spaming KURWA KURWA PIERDOLE PIERDOLE',
    'this mel is such a spy she is spying on our talks here 24/7 100%\nshe even said hi to you,but didn\'t give a fk to congrats me on getting a job and getting one step close to  being mature',
    'btw cene what a day that ex of mine said hello to me on facebook and at same time even that big boob girl from new year lol :joy:',
    'sneaky kokoska',
    'seggy perfering some big tits',
    'ma boi dran\nDeny\nyou gotta alot to learn',
    'Dany boi is bnoi\nhe aint no woman',
    'i went for a dreds ma man',
    'it is time for some quaility getting nude and begging for gold',
    'seggy can i dance in some town like SW half nude for gold ?',
    'im good guy',
    'jhingis khan the betrayer of innocent',
    'awy and cenelia the innocent ones honestly',
    '†\nmoment of silence for our fallen brother',
    'DONT LET ONIONS DISTRACT YOU',
    'tits may be small but i can still make some monney wqith \'em',
    'ye it deffinilty sound retarded as fuck',
    'i need no book for ma wisdom\ni hgold it all in ma brain',
    'HA HAH A',
    'you sucsefuly became a gypsy',
    'ya can both be betrayers never enough of those in world anyways',
    'we will lie and say you\'re a good person',
    'how good of a guy i am i even lie for your benefit',
    'this is comunism we are all equal i am just a little bit more equal then ya al',
    'he became a foking nigga',
    'POLISH LIVES MATTERS',
    'gladiator idk if i rly weanna play thank',
    'in kurwaland they say kurwa not sorry',
    'we did better than your poor ass',
    'shadap',
    'i would be the best raid leader of all times if only i didnt hate 90% of the guild the other 10% were you guys',
    'DANI CMONE BE ON MY SIDE ONCE YOU KNOW I AK RIGHT',
    'you had autism before you met me\ni could only possibly affect it in possitve way\nlike getting rid of it for ya poor ass',
    'how autistic can somone get i wonder always',
    'holy fokin shit',
    'big dick impaler commin\' through',
    'FUCK IGNIOS !!!!',
    'i drink apple juice only',
    'universe can\'t even comperhand that much of sheer goodness',
    'im the wisest of us all',
    'HIT IT VERY HARD AND HIT IT LIKE YOU MEAN IT',
    'awy the greatest leader of all after our mighty pack leader ofc',
    'what does it mean "Mangia merde e morte" it does not sound friendly at all',
    'actually when monney is in play, i do 100 calculations per mili second',
    'remeberness',
    'yes segment is friendly and helpfull\nif you are maria teresa segment is like 3 of dem bitches',
    'i am f riendly',
    'awys chamber sounds missleading',
    'everyone always hated cene except me',
    'dw cene i\'ll throw bricks at your haters like a tru good bruda',
    'Kohai is like tyler1 an autism with good heart',
    'THIS S HIT MADE MY DAY',
    'why do you hate such a kind and good person that will always tell you truth in your face ? So you can take 1st step to accepting yourself as you really arte',
    'even ma momma  dont have no expectations from me',
    'im the one who is ruining kragujevac\'s reputation',
    'yo ma man the impaler',
    'but it\'s okay we shouldn\'t look down to much on a midgets',
    'imagine beign a midget and then  get stamped on by 1.94 115kgs awy',
    'well ofc if you are true slav you get your sentance prolonged every now and then',
    'that\'s so romantic',
    'next time mix VINJAK and POKER http://prntscr.com/hz8vo0 ',
    '@Cene the Kokoska  ya alive ?',
    'this one is just for you,this is how tru serbs looks like,carrying machetes and drinking vodka vodka\nhttps://image.prntscr.com/image/llvyhI-RTXK7aK-HMGVidA.png ',
    'https://image.prntscr.com/image/yOEamt6ZTIypMNXKWQIBHg.png',
    'https://media.discordapp.net/attachments/364712407601512450/753312543488999631/Screenshot_1504.png?width=689&height=515',
    'https://media.discordapp.net/attachments/364712407601512450/719636503676059668/Screenshot_1469.png?width=931&height=515',
    'https://media.discordapp.net/attachments/364712407601512450/719636518758777003/Screenshot_1470.png',
    'https://image.prntscr.com/image/JdO52xtyQy2vyTMXzfAtPA.png']

def save_to_github(file_name):
    g = Github("OskarWalichniewicz", str(os.environ['GITHUB_PASSWORD']))
    repo = g.get_repo("OskarWalichniewicz/slackerbot")
    contents = repo.get_contents("variables.json")
    repo.update_file(contents.path, "az wrote something", file_name, contents.sha)

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print("Bot ready")

@client.event
async def on_message(message):
    if message.author.id == int(os.environ['AZ_DISCORD_ID']):
        year = message.created_at.year
        month = message.created_at.month
        day = message.created_at.day
        hour = message.created_at.hour
        minute = message.created_at.minute
        second = message.created_at.second
        new_time = {'year' : year,
        'month': month,
        'day': day,
        'hour': hour,
        'minute': minute,
        'second': second}
        with open('variables.json', 'w') as f:
            f.truncate()
            json.dump(new_time, f)

        save_to_github(str(new_time))
    await client.process_commands(message)


@client.command()
async def awy(ctx):
    rolled_quote_awy = random.choice(awyQuotes)
    if rolled_quote_awy.startswith('http'):
        await ctx.send(rolled_quote_awy)
    else:
        await ctx.send('Awy once said: "{}".'.format(rolled_quote_awy))

@client.command()
async def akcent(ctx):
    await ctx.send('https://prnt.sc/udv05c')

@client.command()
async def stonelia(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/709413405131407380/Screenshot_794.png?width=686&height=515')

@client.command()
async def stonement(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/753284032036470824/unknown.png?width=728&height=515')

@client.command()
async def pam(ctx):
    await ctx.send('https://media.discordapp.net/attachments/364712407601512450/752975692966264902/Screenshot_797.png?width=684&height=515')

@client.command()
async def dran(ctx):
    dran =['Dran is still a betrayer.',
    'Dran still does not have mats.']
    await ctx.send(random.choice(dran))

@client.command()
async def segment(ctx):
    rolled_quote_segment = random.choice(segmentQuotes)
    if rolled_quote_segment.startswith('http'):
        await ctx.send(rolled_quote_segment)
    else:
        await ctx.send('Segment once said: "{}".'.format(rolled_quote_segment))

@client.command()
async def ignios(ctx):
    await ctx.send('Fuck Ignios')

@client.command()
async def pupinka(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/364712407601512450/399218303739887617/WoWScrnShot_010618_160818.jpg')

@client.command()
async def az(ctx):
    with open('variables.json') as json_data:
        json_dict = json.load(json_data)
        az_date = datetime(json_dict["year"],
        json_dict["month"],
        json_dict["day"],
        json_dict["hour"],
        json_dict["minute"],
        json_dict["second"])

    curr_date = datetime.now() + timedelta(hours = 2) # adding 2 hours cuz timezone
    print(curr_date)

    diff = curr_date - az_date
    diff_days = diff.days
    diff_hours = (diff.seconds // 3600)
    diff_minutes = (diff.seconds // 60) % 60
    diff_seconds = diff.seconds - diff_hours * 3600 - diff_minutes * 60

    if diff_days > 0:
        outp = "Az died {} days, {} hours, {} minutes, {} seconds ago".format(diff_days, diff_hours, diff_minutes, diff_seconds)
    else:
        if diff_hours > 0:
            outp = "Az died {} hours, {} minutes, {} seconds ago".format(diff_hours, diff_minutes, diff_seconds)
        else:
            if diff_minutes > 0:
                outp = "Az died {} minutes, {} seconds ago".format(diff_minutes, diff_seconds)
            else:
                if diff_seconds > 0:
                    outp = "Az died {} seconds ago".format(diff_seconds)


    if diff_days == 1:
        outp = outp.replace("days", "day")
    if diff_hours == 1:
        outp = outp.replace("hours", "hour")
    if diff_minutes == 1:
        outp = outp.replace("minutes", "minute")
    if diff_seconds == 1:
        outp = outp.replace("seconds", "second")

    await ctx.send(outp)


client.run(os.environ['DISCORD_TOKEN']) #token