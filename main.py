# Importing files
import asyncio
from discord.ext import commands
import random
import json
import discord
from webserver import keep_alive

def get_prefix(bot, ctx):
    with open(r"prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(ctx.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
#bot.remove_command('help')

mainshop = [{"name": "Stick", "price": 1, "description": "Playing"},
            {"name": "BubbleGum", "price": 10, "description": "Eating"},
            {"name": "Watch", "price": 100, "description": "Time"},
            {"name": "Laptop", "price": 1000, "description": "Working"},
            {"name": "Phone", "price": 10000, "description": "Messaging"},
            {"name": "Xbox", "price": 10000, "description": "Gaming"}]


@bot.event
async def on_ready():
    print('Token = Connected')
    print('Economy = Connected')

async def ch_pr():
    await bot.wait_until_ready()


    while not bot.is_closed():
        status = ["++help", f"In {len(list(bot.guilds))} servers"]
        statuses = random.choice(status)

        await bot.change_presence(activity=discord.Game(name=statuses))

        await asyncio.sleep(2)

bot.loop.create_task(ch_pr())


@bot.command()
@commands.is_owner()
async def reset(ctx, member: discord.Member):

    if ctx.message.author.id == 733324089334431826:
        user = member

        await open_account(member)

        users = await get_bank_data()

        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0

        await ctx.channel.send(f'{ctx.author.mention} reset {member.mention}')

    with open('bank.json', 'w') as f:
        json.dump(users, f)


'''@bot.command()
async def auto(ctx):
    user = ctx.author

    await open_account(ctx.author)

    users = await get_bank_data()

    earnings = random.randrange(1000, 10000)

    await ctx.channel.send(f'{ctx.author.mention} Command activated\nEnding in about 5 minutes to 10 minutes')

    for i in range(20):
        print(i)
        await asyncio.sleep(1)
        users[str(user.id)]['wallet'] += earnings

    await ctx.channel.send(f'{ctx.author.mention} Command completed')

    with open('bank.json', 'w') as f:
        json.dump(users, f)
'''

@bot.command()
async def money(ctx):
    mll = discord.Embed(
        title='Support', description='List of Commands', color=discord.Color.dark_green())
    mll.add_field(name='Leaderboard [number (default = 1)]', value='Shows top ranked user based on their <a:IBEgetMoney:780141666261663755>', inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Sell <item> <amount>', value='Sell an item and earn some <a:IBEgetMoney:780141666261663755>', inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Buy <item> <amount>', value='Buy an item buy it will cost you <a:IBEgetMoney:780141666261663755>!', inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Shop <item> <amount>', value='Shows buyable items with <a:IBEgetMoney:780141666261663755>!', inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Beg (no field needed)', value='See if someone will donate <a:IBEgetMoney:780141666261663755> to you!', inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Deposit <amount>', value="Deposit all that <a:IBEgetMoney:780141666261663755> you've beed holding for a while", inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Rob <user>', value='Feeling greedy? Steal some <a:IBEgetMoney:780141666261663755> from another person.', inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Withdraw <amount>', value='Got no <a:IBEgetMoney:780141666261663755> in your wallet? Withdraw some!', inline=False)
    mll.add_field(name='----------------------------------', value='Next Command', inline=False)
    mll.add_field(name='Auto (no field needed)', value='Collects <a:IBEgetMoney:780141666261663755> without any commands!', inline=False)
    mll.add_field(name='----------------------------------', value='Help Section', inline=False)
    mll.set_thumbnail(url=f'{ctx.author.avatar_url}')
    mll.set_author(name=f'Hello {ctx.author.name}')
    mll.add_field(
        name='Help', value='[] = not required, <> = required, () = note', inline=False)
    mll.set_footer(text=f'Emoji shown = Currency used for commands')

    await ctx.channel.send(embed=mll)


@bot.command(aliases=["lb"])
async def leaderboard(ctx, x=1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"Top {x} Richest People", description="This is decided on the basis of raw money in the bank and wallet", color=discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = bot.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


@bot.command()
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1] == 3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.9 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price*amount

    users = await get_bank_data()

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("bank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]


@bot.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.message.author)

    res = await buy_this(ctx.message.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.channel.send("That Object isn't in the store")
            return
        if res[1] == 2:
            await ctx.channel.send(f"You don't have enough money to buy {amount} {item}")
            return

    await ctx.channel.send(f"You just bought {amount} {item}, enjoy!")


@bot.command()
async def bag(ctx):
    await open_account(ctx.message.author)

    users = await get_bank_data()

    try:
        bag = users[str(ctx.author.id)]['bag']
    except:
        bag = []

    bag_embed = discord.Embed(title='Bag', color=discord.Color.dark_green())
    for item in bag:
        name = item['item']
        amount = item["amount"]
        bag_embed.add_field(name=f"{name}", value=f'{amount}')

    await ctx.channel.send(embed=bag_embed)


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()

    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amount = thing["amount"]
                new_amount = old_amount + amount
                users[str(user.id)]["bag"][index]['amount'] = new_amount
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open('bank.json', 'w') as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


@bot.command()
async def shop(ctx):
    shop = discord.Embed(
        title='Shop', description='List of buyable items', color=discord.Color.dark_green())

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        shop.add_field(
            name=f'{name}', value=f'{price} :moneybag: | {desc}', inline=True)

    await ctx.channel.send(embed=shop)


@bot.command()
async def balance(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    wallet_amount = users[str(ctx.author.id)]['wallet']
    bank_amount = users[str(ctx.author.id)]['bank']

    bal = discord.Embed(
        title=f"{ctx.author.name}'s balance", colour=discord.Color.dark_green())
    bal.add_field(name='Wallet balance:', value=wallet_amount, inline=True)
    bal.add_field(name='Bank balance:', value=bank_amount, inline=True)

    await ctx.channel.send(embed=bal)


@bot.command()
async def beg(ctx):
    user = ctx.author

    await open_account(ctx.author)

    users = await get_bank_data()

    earnings = random.randrange(101)

    fine = random.randrange(500)

    c1 = f'You found {earnings} :moneybag: on the ground'

    c2 = f"You found {earnings} :moneybag: in a bin"

    c3 = f'You were caught stealing {earnings} :moneybag: from a wallet\nThe police have given you a fine of {fine} :moneybag:'

    pos = [c1, c2, c3]

    await ctx.channel.send(random.choice(pos))

    if c1:
        users[str(user.id)]['wallet'] += earnings

    if c3:
        users[str(user.id)]['wallet'] -= fine

    with open('bank.json', 'w') as f:
        json.dump(users, f)


@bot.command()
async def work(ctx):
    job1 = 'Policeman'
    job2 = 'Builder'

    job1_image = ':police_officer:'
    job2_image = ':construction_worker:'

    job1_earnings = random.randrange(5000, 10000)
    job2_earnings = random.randrange(10000, 15000)

    salary = discord.Embed(
        title='Job offer 1', description='React with 👍', color=discord.Color.dark_green())
    salary1 = discord.Embed(
        title='Job offer 2', description='React with 👍', color=discord.Color.dark_green())

    salary.add_field(name=f'{job1}', value=f'{job1_image}', inline=False)
    salary1.add_field(name=f'{job2}', value=f'{job2_image}', inline=False)

    channel = ctx.message.channel

    await channel.send(embed=salary)
    await channel.send(embed=salary1)

    await open_account(ctx.author)

    users = await get_bank_data()

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == '👍'

    try:
        await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await asyncio.sleep(1)
        await channel.send('Your employer was busy and had to go')
    else:
        await asyncio.sleep(1)
        await channel.send(f'Well done! You earned `{job1_earnings}` :moneybag: .Your employer = `The local Police Force`')
        users[str(ctx.author.id)]['wallet'] += job1_earnings

    try:
        await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await asyncio.sleep(1)
        await channel.send('Your employer was busy and had to go')
    else:
        await asyncio.sleep(1)
        await channel.send(f'Well done! You earned `{job2_earnings}` :moneybag: .Your employer = `The local Construction Team`')
        users[str(ctx.author.id)]['wallet'] += job2_earnings

    with open('bank.json', 'w') as f:
        json.dump(users, f)


@bot.command()
async def withdraw(ctx, amount=None):
    await open_account(ctx.message.author)
    if amount == None:
        await ctx.send('Please enter the amount!')
        return

    b = await update_bank(ctx.message.author)

    amount = int(amount)
    if amount > b[1]:
        await ctx.send("You don't have that much money!")
        return
    if amount < 0:
        await ctx.send("Amount must be above 0!")
        return

    await update_bank(ctx.message.author, amount)
    await update_bank(ctx.message.author, -1 * amount, 'bank')

    await ctx.send(f"You withdrew {amount} :moneybag: from your Bank")


@bot.command()
async def deposit(ctx, amount=None):
    await open_account(ctx.message.author)
    if amount == None:
        await ctx.send('Please enter the amount!')
        return

    b = await update_bank(ctx.message.author)

    amount = int(amount)
    if amount > b[0]:
        await ctx.send("You don't have that much money!")
        return
    if amount < 0:
        await ctx.send("Amount must be above 0!")
        return

    await update_bank(ctx.message.author, -1 * amount)
    await update_bank(ctx.message.author, amount, 'bank')

    await ctx.send(f"You deposited {amount} :moneybag: to your Bank")


@bot.command()
async def transfer(ctx, member: discord.Member, amount=None):
    await open_account(ctx.message.author)
    await open_account(member)
    if amount == None:
        await ctx.send('Please enter the amount!')
        return

    b = await update_bank(ctx.message.author)
    if amount == 'all':
        amount = b[0]

    amount = int(amount)
    if amount > b[1]:
        await ctx.send("You don't have that much money!")
        return
    if amount < 0:
        await ctx.send("Amount must be above 0!")
        return

    await update_bank(ctx.message.author, -1 * amount, 'bank')
    await update_bank(member, amount, 'bank')

    await ctx.send(f"You donated {amount} :moneybag: to {member.mention}")


@bot.command()
async def slots(ctx, amount=None):
    await open_account(ctx.message.author)
    if amount == None:
        await ctx.send('Please enter the amount!')
        return

    b = await update_bank(ctx.message.author)

    amount = int(amount)
    if amount > b[0]:
        await ctx.send("You don't have that much money!")
        return
    if amount < 0:
        await ctx.send("Amount must be above 0!")
        return

    final = []
    for i in range(3):
        print(i)
        options = [":money_with_wings:", ":x:", ":money_with_wings:"]
        a = random.choice(options)

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[1] or final[1] == final[2]:
        await update_bank(ctx.message.author, 2 * amount)
        await ctx.send('You won `2x` the amount of money!')
    else:
        await update_bank(ctx.message.author, -1 * amount)
        await ctx.send('You lost the same amount of money that you gambled!')


@bot.command()
async def rob(ctx, member: discord.Member):
    await open_account(ctx.message.author)
    await open_account(member)

    b = await update_bank(member)

    if b[0] < 100:
        await ctx.send(f"This member is not worth robbing!")
        return

    earnings = random.randrange(0, b[0])

    await update_bank(ctx.message.author, earnings)
    await update_bank(member, -1 * earnings, 'bank')

    await ctx.send(f"You robbed {member.mention} and received {earnings} :moneybag: into your wallet!")


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0

    with open('bank.json', 'w') as f:
        json.dump(users, f)
        return True


async def get_bank_data():
    with open('bank.json', 'r') as f:
        users = json.load(f)
        return users


async def update_bank(user, change=0, mode='wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('bank.json', 'w') as f:
        json.dump(users, f)

    b = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return b


def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]



@bot.event
async def on_guild_join(guild):
    with open(r"prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '++'

    with open(r"prefixes.json", "w") as f:
        json.dump(prefixes, f)


@bot.command(name='changeprefix', aliases=['prefix'], description='<original prefix>changeprefix <new prefix>')
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open(r"prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open(r"prefixes.json", "w") as f:
        json.dump(prefixes, f)

    await ctx.channel.send(f'The prefix was changed to {prefix}')

@bot.event
async def on_message(msg):
    try:

        if msg.mentions[0] == bot.user:

            with open(r"prefixes.json", "r") as f:
                prefixes = json.load(f)

            pre = prefixes[str(msg.guild.id)]

            await msg.channel.send(f'My prefix for this server is ***`{pre}`***')
            bot.process_commands(msg)

    except:
        pass
        await bot.process_commands(msg)

# Running code via token
keep_alive()

# extensions = ['Help']#, 'Moderation', 'Owner']

# if __name__ == '__main__':
#     for ext in extensions:
#         bot.load_extension(ext)
#         print(f'Connected to local file => {ext}')

Task = open(r"Token.txt", "r")
Value = Task.read()
Task.close()

bot.run(Value)
