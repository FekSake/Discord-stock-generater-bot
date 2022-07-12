import discord, json, random,os, threading
from discord.ext import commands

def start_webserver(bot:str="NaN"):
    """
    It starts a webserver on port 81, and returns a message when you visit the page
    
    :param bot: The bot object
    """
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def index():
        return f'Hello, from {bot}!\nMade for replit-24/7-hosting'
    
    print(f"Webserver started for replit 24/7 'free' hosting")
    app.run(host='0.0.0.0', port=81)


# Loading the config.json file and setting the variables to the values in the json file.
with open("config.json","r") as f:
    config = json.load(f)

prefix = config["prefix"]
token = config["token"]
delay = config["delay"]
allowed_roles = config["allowed_roles"]
allowed_channels = config["allowed_channels"]
allowed_guilds = config["allowed_guilds"]
embed_colour = config["embed_colour"]


def display_time(seconds, granularity=2):
    """
    It takes a number of seconds and returns a string of the form "X years, Y days, Z minutes, etc."
    
    The granularity argument is optional. If you don't specify it, you'll get the most finely-grained
    representation of the time period that the number of seconds represents. If you set granularity to,
    say, 1, you'll get the coarsest possible representation
    
    :param seconds: The number of seconds you want to convert
    :param granularity: The number of time units to display, defaults to 2 (optional)
    :return: A string of the time in the format of "x years, x weeks, x days, x hours, x minutes, x
    seconds"
    """
    result = []
    intervals = (
    ('years', 31536000),
    ('weeks', 604800), 
    ('days', 86400),   
    ('hours', 3600),   
    ('minutes', 60),
    ('seconds', 1),
    )
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append(f"{int(value)} {name}")
    return ', '.join(result[:granularity])


# Setting the intents for the bot.
intents = discord.Intents().all()
intents.message_content = True # py-cord only

bot = commands.Bot(
    command_prefix= prefix,
    intents=intents
    )

bot.remove_command("help")

@bot.event
async def on_ready():
    """
    It starts a webserver for replit 24/7 online hosting and displays the bot's name and the prefix.
    """
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".help"))
    print(f"Connected to {bot.user.name} with prefix '{prefix}' and a gen-delay of {display_time(delay,2)}")
    threading.Thread(target=start_webserver,args=(bot.user.name,)).start()

@bot.event
async def on_message(message):
    """
    If the message is from a bot, or if the message is not in an allowed channel, or if the message is
    not in an allowed guild, or if the message is not from the owner in dms, then return. Otherwise, process
    the commands.
    
    :param message: The message object
    :return: The bot is returning the message that the user is not validated.
    """
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        embed = discord.Embed(title=f"{message.author.mention} My prefix is {prefix}",colour=embed_colour)
        return await message.reply(embed=embed)
    if not(message.channel.id in allowed_channels):return
    if message.content.startswith("."):
        if message.guild == None:
            if message.author.id != bot.owner_id:
                embed = discord.Embed(title=f"Sorry, only the bot owner can run commands in dms",colour=embed_colour)
                return await message.reply(embed=embed)
        elif not(message.guild.id in allowed_guilds):
            embed = discord.Embed(title=f"Sorry, {message.guild} isnt whitelisted by the bot owner.",colour=embed_colour)
            return await message.reply(embed=embed)
        else:
            await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    """
    It's a function that sends an embed with an error message when an error occurs.
    
    :param ctx: The context of where the command was used
    :param error: The error that was raised
    :return: The error message
    """
    error_str = str(error)
    error = getattr(error, 'original', error)
    embed = discord.Embed(title="Error occured",colour=15158332)
    if isinstance(error, commands.CommandNotFound):
        return
    elif "You do not own this bot." in error_str:
        embed.add_field(name="Permission error",value="You do not own this bot" )    
    elif isinstance(error, commands.CheckFailure):
        embed.add_field(name="Permission error",value="You're missing permission to execute this command")   
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name="Arguments error",value=f"Missing arguments: {error}")   
    elif isinstance(error, discord.errors.Forbidden):
        embed.add_field(name="Discord error",value=f"{error}")
    elif isinstance(error,commands.CommandOnCooldown):
        time = str(error).strip("You are on cooldown. Try again in ").strip("s")
        embed.add_field(name=f"Command is on cooldown",value=f"{str(error)[0:33]} {display_time(float(time))}")   
    else:
        embed.add_field(name="Misc error",value=error)
        print(error)
    embed.set_footer(text="Bot developed by FekSake#0971")
    embed.set_author(name=ctx.author)
    return await ctx.reply(embed=embed,delete_after=60)


@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def stock(ctx):
    validated = False
    for role in ctx.author.roles:
        if role.id in allowed_roles:
            validated = True
    
    if validated == False:
        embed = discord.Embed(title="Error occured",colour=15158332)
        embed.add_field(name="Permission error",value="You're missing permission to execute this command")   
        embed.set_footer(text="Bot developed by FekSake#0971")
        embed.set_author(name=ctx.author)
        return await ctx.reply(embed=embed,delete_after=60)
    """
    It displays the stock of the server.
    
    :param ctx: The context of the command
    :return: The stock of the server.
    """
    embed = discord.Embed(title="Stock",colour=embed_colour)
    with open("stock.json","r") as f:stock = json.load(f)
    stock_value = ""
    if len(stock) > 0:
        for s in stock:
            stock_value = f"{stock_value}**{s}**: ``{len(stock[s])}``\n"
    else: stock_value = f"{ctx.guild} has not added any stock yet."
    embed.add_field(name=f"Stock in {ctx.guild}",value=stock_value)
    embed.set_footer(text="Bot developed by FekSake#0971")
    embed.set_author(name=ctx.author)
    return await ctx.reply(embed=embed)

@bot.command()
@commands.cooldown(1,delay,commands.BucketType.user)
async def gen(ctx,item:str=None):
    validated = False
    for role in ctx.author.roles:
        if role.id in allowed_roles:
            validated = True
    
    if validated == False:
        embed = discord.Embed(title="Error occured",colour=15158332)
        embed.add_field(name="Permission error",value="You're missing permission to execute this command")   
        embed.set_footer(text="Bot developed by FekSake#0971")
        embed.set_author(name=ctx.author)
        return await ctx.reply(embed=embed,delete_after=60)
    """
    It generates a random item from a json file and sends it to the user in a dm.
    
    :param ctx: The context of the command
    :param item: The item to get from json
    :type item: str
    :return: The item that was generated.
    """
    if item == None:
        embed = discord.Embed(title="You didn't select a item to generate.",colour=embed_colour)
        return await ctx.reply(embed=embed)
    with open("stock.json","r") as f:
        stock = json.load(f)
    for s in stock:
        if s.upper() == item.upper():
            amount_left = len(stock[s])
            if amount_left <= 0:
                embed = discord.Embed(title=f"Sorry but there is **0** of this item left.",colour=embed_colour)
                return await ctx.reply(embed=embed)
            else:
                item_selected = random.choice(stock[s])
                stock[s].pop(stock[s].index(item_selected))
                embed = discord.Embed(title=f"Generated 1 {item.capitalize()}",description=f"{item_selected}",colour=embed_colour)
                embed.set_footer(text="This message will delete in 3 minutes.")
                
                try:
                    dm = ctx.author.dm_channel
                    if dm == None:
                        dm = await ctx.author.create_dm()
                    await dm.send(embed=embed,delete_after=180)
                    embed = discord.Embed(title=f"Check your dms.",colour=embed_colour)
                    await ctx.reply(embed=embed)
                except:
                    embed = discord.Embed(title="Couldnt dm you. Turn on your dms and try again.",colour=embed_colour)
                    return await ctx.reply(embed=embed)
                with open("stock.json","w") as f:
                    json.dump(stock,f,indent=4)
                return
    embed = discord.Embed(title=f"Sorry, Couldnt find {item} in the gen.",colour=embed_colour)
    return await ctx.reply(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True) 
async def add(ctx,name=None):
    """
    It takes a file with items seperated by a new line and adds them to a json file.
    
    :param ctx: The context of the message
    :param name: The name of the stock to add to
    :return: The return value of the function.
    """
    if name == None:
        embed = discord.Embed(title="Where should this be added to?",colour=embed_colour)
        return await ctx.reply(embed=embed)
    if not(ctx.message.attachments):
        embed = discord.Embed(title=f"Please attach a file with items to be added seperated by a new line",colour=embed_colour)
        return await ctx.reply(embed=embed)
    with open("stock.json","r") as f:
        stock = json.load(f)
    for s in stock:
        if name.lower() == s.lower():
            already_in_stock = stock[s]
            await ctx.message.attachments[0].save("tmp.txt")
            lines = []
            with open("tmp.txt","r") as f:
                for line in f.readlines():
                    foramtted = line.strip("\n").strip("\r")
                    if not(foramtted == ""): 
                        lines.append(foramtted)
                        print(f"Added {foramtted} to {name}")
                    else:
                        print(f"Empty line...")
            os.remove("tmp.txt")
            for line in lines:
                already_in_stock.append(line)
            stock[s] = already_in_stock
            with open("stock.json","w") as f:
                json.dump(stock,f,indent=4)
            embed = discord.Embed(title=f"Added {len(lines)} stock to {name}",colour=embed_colour)
            return await ctx.reply(embed=embed)

    already_in_stock = []
    await ctx.message.attachments[0].save("tmp.txt")
    lines = []
    with open("tmp.txt","r") as f:
        for line in f.readlines():
            foramtted = line.strip("\n").strip("\r")
            if not(foramtted == ""): 
                lines.append(foramtted)
                print(f"Added {foramtted} to {name}")
            else:
                print(f"Empty line...")
    os.remove("tmp.txt")
    for line in lines:
        already_in_stock.append(line)
    stock[name] = already_in_stock
    with open("stock.json","w") as f:
        json.dump(stock,f,indent=4)
    embed = discord.Embed(title=f"Added {len(lines)} stock to {name}",colour=embed_colour)
    return await ctx.reply(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True) 
async def remove(ctx,name=None):
    """
    It removes a catagory from the stock.json file.
    
    :param ctx: The context of the command
    :param name: The name of the catagory you want removing
    :return: The return value of the function.
    """
    if name == None:
        embed = discord.Embed(title=f"What catagory do you want removing?",colour=embed_colour)
        return await ctx.reply(embed=embed)
    with open("stock.json","r") as f:
        stock = json.load(f)
    for s in stock:
        if s.lower() == name.lower():
            stock.pop(s)
            with open("stock.json","w") as f:
                json.dump(stock,f,indent=4)
            embed = discord.Embed(title=f"Removed {name}",colour=embed_colour)
            return await ctx.reply(embed=embed)
    embed = discord.Embed(title=f"Couldnt find {name}",colour=embed_colour)
    return await ctx.reply(embed=embed)

@bot.command()
async def help(ctx):
    """
    It creates an embed with commands which can be run by either a user or admin
    
    :param ctx: The context of where the command was used
    """
    embed = discord.Embed(title="Help",colour=embed_colour)
    embed.add_field(name="Gen-users",value="**stock** - Show server stock\n**gen <item>** - generate a item",inline=False)
    embed.add_field(name="Admin",value="**add <name of catagory to add to> <attach file with items>** - Add items to a catagory\n**remove <name of catagory>** - removes catagory from bot",inline=False)
    embed.set_footer(text="Bot developed by FekSake#0971")
    embed.set_author(name=ctx.author)
    await ctx.reply(embed=embed)

# It's running the bot with the token and reconnecting if the bot disconnects.
bot.run(token,reconnect=True)