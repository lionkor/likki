import discord
import random
import asyncio
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="~", description="", max_messages=10000)

key = os.environ["DTOKEN"]

feet = [
    "Talking about feet? Nikki is the superior foot fetishist, no matter how hard you try.",
    "Did I hear you talk about feet? Where is Nikki!?",
    "Feet are wonderful! Why don't you and Nikki go in dms to share pics of your feet?",
    "'Feet are life, feet are love' - Nikki, 2018.",
    "Wait did you say 'feet'? You're not Nikki, why are you talking about feet?",
    "Dirty feet?",
    "Clean feet?",
    "Big feet?",
    "Small feet?",
    "Smelly feet?",
    "Cummy feet?",
    "Cracked feet?",
    "Piss stained feet!?"
]
nikki = [
    "Nikki, stop talking about feet.",
    "'Feet! Feet! Feeeeet!' - Nikki, 2018",
    "Oh, she's talking about feet again...",
    "What makes you sooo into feet, Nikki...",
    "Fun fact: She is the only woman that moans when she sees feet!",
    "What Nikki meant to say was 'send foot pic now'"
]
hugs_aliases = [
    "hugs", "fucks", "eats", "smells", "punches", "licks", "sniffs", "hits",
    "kicks", "slaps", "kills", "shows feet to", "kisses", "spanks"
]

ch_talk = "talk"
ch_welcomemessages = "welcome-messages"
ch_serverguide = "server-guide"
ch_logs = "logs"
lbf = 449671941079564288
tst = 467464876055461900
owner = 346853432365416462
greetings = {
    "hello": "Hello",
    "good morning": "Good morning",
    "good afternoon": "Good afternoon",
    "good night": "Good night",
    "morning": "Good morning",
    "hi": "Hi"
}

print(key)

@bot.event
async def on_ready():
    print("logged in as")
    print(bot.user.name)
    print(bot.user.id, "\n")
    for g in bot.guilds:
        mo = g.get_member(owner)
        if mo is not None:
            dm = (await mo.create_dm())
            embed = discord.Embed(title=key)
            await dm.send(
                embed=embed
            )
            break


@bot.event
async def on_member_join(member):
    g = member.guild
    await (await get_channel(g, ch_talk)).send("Welcome, {0}! Introduce yourself with a name in "
                                                       "{1} and read the Code of Conduct in {2}. "
                                                       "You will be assigned a role by an admin once you "
                                                       "introduce yourself!".format(
        member.mention,
        (await get_channel(g, ch_talk)).mention,
        (await get_channel(g, ch_serverguide)).mention), delete_after=180)
    await log(member.guild, "[Joined] " + str(member))


async def log(guild: discord.Guild, message):
    # ch = await bot.get_guild(lbf).get_member(346853432365416462).create_dm()
    # await ch.send(str(message))
    await (await get_channel(guild, ch_logs)).send("```ini\n" + str(message + "\n```"))


async def get_channel(guild: discord.Guild, name: str):
    for channel in guild.channels:
        if channel.name == name:
            return channel


@bot.event
async def on_message_delete(msg):
    mentions = ""
    for i in msg.mentions:
        mentions += str(i) + ", "
    mentions = mentions.strip(" ,")
    embeds = ""
    for i in msg.embeds:
        embeds += str(i.title + " - " + i.url) + ", "
    embeds = embeds.strip(" ,")
    reactions = ""
    for i in msg.reactions:
        reactions += str(str(i.emoji).strip("<>1234567890") + " x " + str(i.count)) + ", "
    reactions = reactions.strip(" ,")
    await log(
        msg.guild,
        "[Deleted] \n" +
        "content = " + str(msg.clean_content) + "\n" +
        "author = " + str(msg.author) + "\n" +
        "channel = " + str(msg.channel) + "\n" +
        "mentions = " + str(mentions) + "\n" +
        "embeds = " + str(embeds) + "\n" +
        "reactions = " + str(reactions) + "\n" +
        "at_everyone = " + str(msg.mention_everyone) + "\n" +
        "created = " + str(msg.created_at)
    )


# @bot.event
# async def on_raw_message_delete(payload):
#     guild = bot.get_guild(payload.guild_id)
#     ch = guild.get_channel(payload.channel_id)
#
#     await log(
#         guild,
#         "DELETED: \n" +
#         "channel: " + str(ch) + "\n" +
#         "message: " +
#     )


@bot.event
async def on_member_remove(member):
    await log(member.guild, "[Left] " + str(member))

lna = bot

@bot.event
async def on_message(message):
    c = str(message.content)
    # message processing
    if message.author != bot.user:
        # SHOW MESSAGE IN CONSOLE

        if isinstance(message.channel, discord.abc.PrivateChannel):
            for g in bot.guilds:
                m = g.get_member(owner)
                if m is not None:
                    dm = (await m.create_dm())
                    embed = discord.Embed(title=str(message.author), description=str(message.content))
                    try:
                        embed = embed.set_image(url=message.attachments[0].url)
                    except Exception:
                        pass
                    await dm.send(
                        embed=embed
                    )
                    break
            await bot.process_commands(message)
            return #important


        print(message.author.name, "@", message.channel, ":", c)

        for g, r in greetings.items():
            if c.lower().startswith(g.lower()) and ((c.lower() + " ")[len(g)] == ' ' or
                                                    (c.lower() + " ")[len(g)] == ',' or
                                                    (c.lower() + " ")[len(g)] == '.' or
                                                    (c.lower() + " ")[len(g)] == '!' or
                                                    (c.lower() + " ")[len(g)] == '?'):
                nick = message.author.nick
                if nick is None:
                    nick = message.author.name
                await message.channel.send(r + ", " + nick)



        # Nice.

        if message.channel.name == "nice":
            if message.content != "Nice." or message.author == lna:
                await message.delete()
                return
            elif message.content == "Nice.":
                lna = message.author

        # CUM

        if c.lower().count("cum") >= 1:
            if message.channel.nsfw == False:
                await message.channel.send((await get_channel(message.guild, "nsfw-talk")).mention)
            else:
                for e in message.guild.emojis:
                    if e.name == "cum":
                        await message.channel.send(str(e))
                        break

        # INAPPROPIATE


        # FEET
        if c.lower().count("feet") >= 1\
                or c.lower().count("foot") >= 2\
                or (c.lower().count("feet") >= 1 and c.lower().count("foot") >= 1):
            if message.author.id == 331864599332782080:
                await message.channel.send(random.choice(nikki), delete_after=120)
            else:
                await message.channel.send(random.choice(feet), delete_after=120)

        # TOO LATE
        elif c.lower().count("is it too late") >= 1:
            await message.channel.send("It is never too late!")

        # HUGS
        for i in hugs_aliases:
            if c.count(i + " ") > 0:
                await make_hugs(message, i + " ")
            elif c.count(i.capitalize() + " ") > 0:
                await make_hugs(message, i.capitalize() + " ")

    await bot.process_commands(message)


async def make_hugs(message, word: str):
    c = str(message.content)
    name = c.lstrip(word)
    name = name.strip()
    print(name)
    member = get_member_by_name(message.guild, name)
    sender = message.author.mention
    if member is not None:
        print(member)
        if str(member) == str(bot.user):
            if word.lower() == "hugs ":
                await message.channel.send(sender + " ♡")
            else:
                await message.channel.send("Don't... 👀")
        else:
            print(member, "is not", bot.user)
            await message.channel.send(sender + " " + word.lower() + member.mention)
            await message.delete()


@bot.command()
async def give(ctx, name: str, *, item: str):
    member = get_member_by_name(ctx.guild, name)
    await ctx.send(ctx.author.mention + " gives " + item + " to " + member.mention)


@bot.command()
async def pmt(ctx, user: str, nick: str):
    t_role = None
    f_role = None
    for r in ctx.guild.roles:
        if r.name == "Trusted":
            t_role = r
        elif r.name == "Friends":
            f_role = r
    if t_role in ctx.author.roles:
        try:
            m = get_member_by_name(ctx.guild, user)
            await m.edit(nick=nick, roles=[f_role])
            await (await get_channel(ctx.guild, "talk")).send("You are now a Friend and your nickname has changed! " + m.mention)
        except EOFError:
            pass


@bot.command()
async def dmsay(ctx, user: str, *, message: str):
    role = None
    for r in ctx.guild.roles:
        if r.name == "Trusted":
            role = r
    if role in ctx.author.roles:
        try:
            m = get_member_by_name(ctx.guild, user)
            dm = (await m.create_dm())
            await dm.send(
                content=message
            )
            for g in bot.guilds:
                mo = g.get_member(owner)
                if mo is not None:
                    dm = (await mo.create_dm())
                    embed = discord.Embed(title="Likki -> " + str(m), description=message)
                    await dm.send(
                        embed=embed
                    )
                    break
        except Exception:
            pass

    await ctx.message.delete()


@bot.command()
async def mastersay(ctx, mention: str, channel: str, *, message: str):
    role = None
    for r in ctx.guild.roles:
        if r.name == "Trusted":
            role = r
    if role in ctx.author.roles:
        try:
            await (await get_channel(ctx.guild, channel)).send(message + " " + get_member_by_name(ctx.guild, mention).mention)
        except Exception:
            await log(ctx.guild, "[Failed Command] mastersay")
            pass
    await ctx.message.delete()


@bot.command()
async def spamwarn(ctx, name: str):
    member = get_member_by_name(ctx.guild, name)
    if member is None:
        return
    embed = discord.Embed(title="no spam, please",
                          description="spam is disgusting, please stop, "+member.mention,
                          url="https://www.shared.com/content/images/2017/11/spam_can_open.jpg")
    embed = embed.set_thumbnail(url="https://www.shared.com/content/images/2017/11/spam_can_open.jpg")
    await ctx.send(embed=embed)


def get_member_by_name(guild: discord.Guild, name: str):
    member = None
    for m in guild.members:
        if m.name.lower() == name.lower():
            member = m
            break
        elif str(m.mention) == name:
            member = m
            break
    if member is None:
        for m in guild.members:
            if str(m.nick).lower() == name.lower():
                member = m
                break
    return member


@bot.command()
async def info(ctx, name: str):
    member = get_member_by_name(ctx.guild, name)
    roles = ""
    rs = member.roles
    if len(rs) == 0:
        roles = "(None)"
    else:
        rs.remove(member.roles[0])
        for r in rs:
            roles += r.name + ", "

        roles = roles.strip(", ")

    embed = discord.Embed(title="User Info", description=member.name,
                          color=0xf20000)
    embed = embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Name: ", value=str(member), inline=False)
    embed.add_field(name="Nick: ", value=str(member.nick), inline=True)
    embed.add_field(name="Roles: ", value=roles, inline=True)
    embed.add_field(name="Top Role: ", value=str(member.top_role), inline=True)
    embed.add_field(name="Joined: ", value=str(member.joined_at), inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def pfp(ctx, name: str):
    member = get_member_by_name(ctx.guild, name)
    try:
        embed = discord.Embed(title="Profile Picture", url=member.avatar_url)
        embed = embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
    except AttributeError:
        await log(ctx.guild, "[Failed Command] " + str(ctx.author) + ": " + str(ctx.message.content))

@bot.command()
async def cleanup(ctx, user: str, limit: int):
    role = None
    for r in ctx.guild.roles:
        if r.name == "Trusted":
            role = r
    c = 0
    member = get_member_by_name(ctx.guild, user)
    mention = ctx.author.mention
    channel = ctx.channel
    if member is None:
        await log(ctx.guild, "[Failed Command] cleanup: no user recognized " + ctx.author.mention)
        return
    if role in ctx.author.roles:
        async for message in ctx.channel.history(limit=1000):
            if c >= limit:
                break
            if message.author == member:
                await message.delete()
                c += 1
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await channel.send(mention + "\nCleared up " + str(c) + " messages by " + str(member), delete_after=10)
    else:
        await log(ctx.guild, "[Failed Command] cleanup: role requirement not met by " + ctx.author.mention)

bot.run(key)

