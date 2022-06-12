from discord.ext.commands import Bot
import discord
import csv
import sys, os 
from math import floor
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


TOKEN = "OTg1MzI0MDA3NzM1ODQ4OTYx.G_hLjv.wJJdfYVdt7VBdPh4Xgd2tuJMbaVYeRaGuxTcCw"

bot = Bot("!")
def damagecalc(atkstat, power, defstat, HP, effectiveness, stab, itemboost):
    if stab:
        stabval = 1.5
    else:
        stabval = 1
    damagelow = floor(floor(floor((2*20+2)*atkstat*power)/defstat)/50+2)*stabval*effectiveness*85/100 * itemboost
    damagehigh = floor(floor(floor((2*20+2)*atkstat*power)/defstat)/50+2)*stabval*effectiveness* itemboost
    damagelow = damagelow/HP * 100
    damagehigh = damagehigh/HP * 100
    return (str(damagelow)+ "% to " + str(damagehigh) + "%")

def damagecalcsupp(name, form, move, evs, ivs, nature, aitem, name2, form2, ev2, iv2, ev3, iv3, nature2, ditem, weather, weather2):
    if form == "//":
        form = " "
    if aitem == "//":
        aitem = " "
    if form2 == "//":
        aitem = " "
    if ditem == "//":
        aitem = " "
    typespec = ["Black Belt", "Black Glasses", "Charcoal", "Dragon Fang", "Hard Stone", "Magnet", "Metal Coat", "Miracle Seed", "Mystic Water", "Never-Melt Ice", "Poison Barb", "Sharp Beak", "Silk Scarf", "Silver Powder", "Soft Sand", "Spell Tag", "Twisted Spoon", "Soul Dew", "Adamant Orb", "Lustrous Orb", "Griseous Orb"]
    with open(resource_path("moveList.csv"), 'r') as f:
        reader = csv.reader(f)
        basepower = 0
        typemove = ""
        sidemove = ""
        for row in reader:
            if row[1] == (" " + move):
                basepower = int(row[5])
                typemove = row[2]
                sidemove = row[3]

    with open(resource_path("Pokemon.csv"), 'r') as f:
        reader = csv.reader(f)
        atkstat = 0
        defstat = 0
        for row in reader:
            if row[1] == name and row[2] == form:
                owntype = row[3]
                owntype2 = row[4]
                if sidemove == " Physical":
                    atkstat = int(row[7])
                if sidemove == " Special":
                    atkstat = int(row[9])
            if row[1] == name2 and row[2] == form2:
                HP = int(row[6])
                othertype = row[3]
                othertype2 = row[4]
                if sidemove == " Physical":
                    defstat = int(row[8])
                if sidemove == " Special":
                    defstat = int(row[10])



    if (" " + owntype) == typemove or (" " + owntype2) == typemove:
        stab = True
    else:
        stab = False

    trueatk = ((atkstat * 2 + ivs + (evs/4)) +5)
    truedef = ((defstat * 2 + iv2 + (ev2/4)) +5)
    trueHP = (HP * 2 + iv3 + (ev3/4)) + 10 + 100
    itemboost = 1
    if aitem == "Life Orb":
        itemboost = 1.3
    if aitem in typespec or aitem == "Expert Belt":
        itemboost = 1.2
    if aitem == "Muscle Band" or aitem == "Wise Glasses":
        itemboost = 1.1
    if aitem == "Choice Band" or aitem == "Choice Specs":
        trueatk *= 1.5
    if ditem == "Eviolite" or ditem == "Assault Vest":
        truedef *= 1.5
    if aitem == "Light Ball" and name == "Pikachu":
        trueatk *= 2
    if aitem == "Toxic Orb" or aitem == "Flame Orb" and move == "Facade":
        basepower *= 2
    if aitem == "Normal Gem" and typemove == " Normal":
        basepower *= 1.3
    if nature == "Plus":
        trueatk *= 1.1
    if nature == "Minus":
        trueatk *= 0.9
    if nature2 == "Plus":
        truedef *= 1.1
    if nature2 == "Minus":
        truedef *= 0.9
    if weather == "Yes" or weather == "yes":
        basepower *= 1.5
    if weather2 == "Yes" or weather2 == "yes":
        basepower *= 0.5
    with open(resource_path("chart.csv"), 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        index = rows[0].index(othertype)
        index3 = rows[0].index(typemove[1:])
        if (othertype2 != " "):
            index2 = rows[0].index(othertype2)
            effectiveness = float(rows[index3][index]) * float(rows[index3][index2])
        else:
            effectiveness = float(rows[index3][index])
                
    return damagecalc(trueatk, basepower, truedef, trueHP, effectiveness, stab, itemboost)


@bot.event
async def on_ready():
    print(f'{bot.user} successfully logged in!')

@bot.event
async def on_message(message):
    # Make sure the Bot doesn't respond to it's own messages
    if message.author == bot.user: 
        return
    
    if message.content == 'hello':
        await message.channel.send(f'Hi {message.author}')
    if message.content == 'bye':
        await message.channel.send(f'Goodbye {message.author}')

    await bot.process_commands(message)



@bot.command()
async def calc(ctx):
    def check(m): return m.author == ctx.author and m.channel == ctx.channel
    await ctx.send('Enter attacker Pokemon name(no forms included): ', delete_after=45.0)
    name = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter form name: (put a double slash if no form): ', delete_after=45.0)
    form = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter move name: ', delete_after=45.0)
    move = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant attack EVs: ', delete_after=45.0)
    evs = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant attack IVs: ', delete_after=45.0)
    ivs = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant held item on attacker: (put a double slash if no item): ', delete_after=45.0)
    aitem = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter defender Pokemon name(no forms included): ', delete_after=45.0)
    name2 = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter form name: (put a double slash if no form): ', delete_after=45.0)
    form2 = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant defense EVs: ', delete_after=45.0)
    ev2 = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant defense IVs: ', delete_after=45.0)
    iv2 = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant HP EVs: ', delete_after=45.0)
    ev3 = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant HP IVs: ', delete_after=45.0)
    iv3 = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter relevant held item on defender: (put a double slash if no item): ', delete_after=45.0)
    ditem = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter if attacking nature is Plus, Minus, or Neutral: ', delete_after=45.0)
    nature = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Enter if defending nature is Plus, Minus, or Neutral: ', delete_after=45.0)
    nature2 = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Is weather boosting this attack? ', delete_after=45.0)
    weatherboost = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send('Is weather weakening this attack? ', delete_after=45.0)
    weatherreduc = await bot.wait_for('message', check=check, timeout=None)
    await ctx.send(damagecalcsupp(name.content, form.content, move.content, int(evs.content), int(ivs.content), nature.content, aitem.content, name2.content, form2.content, int(ev2.content), int(iv2.content), int(ev3.content), int(iv3.content), nature2.content, ditem.content, weatherboost.content, weatherreduc.content))




bot.run(TOKEN)