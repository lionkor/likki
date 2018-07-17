import discord
import random
import asyncio
import os
from likkistorage import LGuild
from discord.ext import commands

bot = commands.Bot(command_prefix="~",
				   description="LBF's pet bot, programmed by @Lion_Kor / Lion#3620",
				   max_messages=10000,
				   pm_help=True)

LG = dict()

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
ch_coc = "code-of-conduct"
lbf = 449671941079564288
tst = 467464876055461900
owner = 346853432365416462
greetings = {
	"hello": "Hello",
	"good morning": "Good morning",
	"good afternoon": "Good afternoon",
	"good night": "Good night",
	"morning": "Good morning",
	"hi": "Hi",
	"i love you likki": "I love you, too"
}

print(key)


@bot.event
async def on_command_error(ctx, error):
	await ctx.send(str(error) + " - Use `~help` " + ctx.author.mention, delete_after=30)
	await log(ctx.guild, "[Command Error] " + str(error))


@bot.command(
	brief="tells you whats big",
	description="responds with an unfunny message with a random persons name"
)
async def whatsbig(ctx):
	"""sends a reply with a random users name"""
	member = random.choice(ctx.guild.members)
	nick = member.nick
	if nick is None:
		nick = member.name
	if member == bot.user:
		await ctx.send("my dick")
		return
	await ctx.send(nick + "'s dick")


@bot.event
async def on_ready():
	print("logged in as")
	print(bot.user.name)
	print(bot.user.id, "\n")
	for g in bot.guilds:
		str_members = []
		for m in g.members:
			str_members.append(str(m))

		LG[str(g)] = LGuild(str(g), str_members)

		mo = g.get_member(owner)
		if mo is not None:

			dm = (await mo.create_dm())
			embed = discord.Embed(title="started",
								  description=str(bot.guilds))
			await dm.send(
				embed=embed
			)
			break


@bot.event
async def on_member_join(member):
	g = member.guild
	s = "[Joined] " + str(member)
	await (await get_channel(g, ch_welcomemessages)).send("Welcome, {0}! Introduce yourself with a name in "
													   "{1} and read the Code of Conduct in {2}. "
													   "You will be assigned a role by an admin once you "
													   "introduce yourself!".format(
		member.mention,
		(await get_channel(g, ch_talk)).mention,
		(await get_channel(g, ch_coc)).mention), delete_after=180)
	await dm_owner(s)
	await log(member.guild, s)


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

@bot.event
async def on_member_remove(member):
	s = "[Left] " + str(member)
	await dm_owner(s)
	await log(member.guild, s)

last_nice = bot.user

@bot.command(
	brief="Shows data recorded by the bot",
	description="Trusted and above only\n"
				"DMs the recorded data. Don't use unless you know what "
				"you're doing."
)
async def data(ctx):
	role = None
	for r in ctx.guild.roles:
		if r.name == "Trusted":
			role = r
	print(str(LG[str(ctx.guild)]))
	if role in ctx.author.roles:
		try:
			dm = (await ctx.author.create_dm())
			await dm.send(
				content=str(LG[str(ctx.guild)])
			)
		except Exception:
			print("OOF")
			pass

	await ctx.message.delete()

@bot.event
async def on_message(message):
	c = str(message.content)
	# message processing
	if message.guild is not None and isinstance(message.channel, discord.TextChannel):
		LG[str(message.guild)].add_one(str(message.author))
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
			return

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
		global last_nice
		if message.channel.name == "nice":
			if message.content != "Nice." or message.author == last_nice:
				await message.delete()
			else:
				last_nice = message.author

		# CUM

		if c.lower().count("cum") >= 1:
			if message.channel.nsfw == False:
				await message.channel.send((await get_channel(message.guild, "nsfw-talk")).mention)
			else:
				for e in message.guild.emojis:
					if e.name == "cum":
						await message.channel.send(str(e))
						break

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
		if str(member) == str(message.author):
			if word.lower() == "hugs ":
				await message.channel.send("oh no, I'll hug you ♡")
				await message.channel.send(bot.user.mention + " hugs " + sender)
			else:
				await message.channel.send("Don't, please :c")
		elif str(member) == str(bot.user):
			if word.lower() == "hugs ":
				await message.channel.send(sender + " ♡")
			else:
				await message.channel.send("Don't... 👀")
		else:
			print(member, "is not", bot.user)
			await message.channel.send(sender + " " + word.lower() + member.mention)
			await message.delete()


@bot.command(brief="gives something, rp style",
			 description="gives something, rp style\n"
						 "name: any name, nickname or mention\n"
						 "item: any text describing or naming "
						 "the item to give")
async def give(ctx, name: str, *, item: str):
	member = get_member_by_name(ctx.guild, name)
	await ctx.send(ctx.author.mention + " gives " + item + " to " + member.mention)


@bot.command(
	brief="automation of the default procedure for new members",
	description="automates the nicknaming and role giving for new members\n"
				"Trusted and above only\n"
				"user: any name, nickname or mention of the user to be promoted\n"
				"nick: new nickname for the user"
)
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


async def dm_owner(message: str):
	for g in bot.guilds:
		mo = g.get_member(owner)
		if mo is not None:
			dm = (await mo.create_dm())
			embed = discord.Embed(title=message)
			await dm.send(
				embed=embed
			)
			break


@bot.command(
	brief="sends a custom dm to a user",
	description="sends a custom dm to a user\n"
				"Trusted and above only\n"
				"user: any name, nickname or mention\n"
				"message: the message to be dm-ed to the user\n"
				"NOTE: Only Lion#3620 can see responses to dms"
)
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


@bot.command(
	brief="sends a message in a channel and mentions a user",
	description="sends a message in a channel and mentions a user\n"
				"Trusted and above only\n"
				"user: any name, nickname or mention of the user that is to be mentioned in the message\n"
				"channel: the channel name that the message should be sent in (example: nsfw-talk)\n"
				"message: the message to be sent"
)
async def mastersay(ctx, user: str, channel: str, *, message: str):
	role = None
	for r in ctx.guild.roles:
		if r.name == "Trusted":
			role = r
	if role in ctx.author.roles:
		try:
			await (await get_channel(ctx.guild, channel)).send(message + " " + get_member_by_name(ctx.guild, user).mention)
		except Exception:
			await log(ctx.guild, "[Failed Command] mastersay")
			pass
	await ctx.message.delete()


@bot.command(
	brief="warns not to spam",
	description="sends an image of spam and says that its disgusting\n"
				"user: any name, nickname or mention"
)
async def spamwarn(ctx, user: str):
	member = get_member_by_name(ctx.guild, user)
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


@bot.command(
	brief="displays basic information about a member",
	description="displays information about a member in the server\n"
				"user: any name, nickname or mention"
)
async def info(ctx, user: str):
	member = get_member_by_name(ctx.guild, user)
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
	embed.add_field(name="Messages since bot recording: ", value=str(LG[str(ctx.guild)].get(str(member)))
	await ctx.send(embed=embed)


@bot.command(
	brief="posts the profile picture of a member",
	description="posts the profile picture of a member as well as the url ot it\n"
				"user: any name, nickname or mention"
)
async def pfp(ctx, user: str):
	member = get_member_by_name(ctx.guild, user)
	try:
		embed = discord.Embed(title="Profile Picture", url=member.avatar_url)
		embed = embed.set_thumbnail(url=member.avatar_url)
		await ctx.send(embed=embed)
	except AttributeError:
		await log(ctx.guild, "[Failed Command] " + str(ctx.author) + ": " + str(ctx.message.content))

@bot.command(
	brief="deletes an amount of messages by a specific user from a channel",
	description="deletes an amount of messages by a specific user from a channel\n"
				"user: any name, nickname or mention\n"
				"limit: maximum amount of messages to be removed\n"
				"NOTE: please note that this will take effect in the channel the command has been"
				"issued in"
)
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
