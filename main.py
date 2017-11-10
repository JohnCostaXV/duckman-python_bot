import discord
import secret_stuff
import database
import random
import asyncio
import time

client = discord.Client()
BOT_TOKEN = secret_stuff.bot_token()
db = database.DataBase()

BOTCOLOR = 0x547e34
RANDOM_STATUS = ["!help", "Quack", "1337", "Duck you!"]
USER_GOALS = [90, 100, 110, 120, 130, 140, 150]

role_msg_id = None
role_msg_user_id = None

r_role_msg_id = None
r_role_msg_user_id = None

user_timer = {}


@client.event
async def on_ready():
    print(client.user.name)
    print("================")
    for server in client.servers:
        for member in server.members:
            db.create_user(member.id, member.name)
    print("100%")


@client.event
async def on_message(message):

    try:
        if time.time() >= user_timer[message.author.id] + 2:
            add_xp(message.author.id, 2)
    except KeyError:
        add_xp(message.author.id, 2)

    author_xp = db.find_user(message.author.id)["xp"]
    author_levels = db.find_user(message.author.id)["levels"]

    if author_xp >= 10 and "level1" not in author_levels:
        add_level(message.author.id, "level1")

        embed = discord.Embed(
            title="LEVEL UP!!⏫🎉",
            color=BOTCOLOR,
            description="{} is now LEVEL 1!".format(message.author.name)
        )

        await client.send_message(message.channel, embed=embed)

    if author_xp >= 50 and "level2" not in author_levels:
        add_level(message.author.id, "level2")

        embed = discord.Embed(
            title="LEVEL UP!!⏫🎉",
            color=BOTCOLOR,
            description="{} is now LEVEL 2!".format(message.author.name)
        )
        embed.add_field(
            name="Rewards:",
            value="- Ability to set your Roles with `!role`.\n"
                  "Available roles: Programmer, Gamer, Designer",
            inline=False
        )

        await client.send_message(message.channel, embed=embed)

    if author_xp >= 100 and "level3" not in author_levels:
        add_level(message.author.id, "level3")

        embed = discord.Embed(
            title="LEVEL UP!!⏫🎉",
            color=BOTCOLOR,
            description="{} is now LEVEL 3!".format(message.author.name)
        )
        await client.send_message(message.channel, embed=embed)

    if author_xp >= 200 and "level4" not in author_levels:
        add_level(message.author.id, "level4")

        for role in message.server.roles:
            if role.name.lower() == "active":
                await client.add_roles(message.author, role)

        embed = discord.Embed(
            title="LEVEL UP!!⏫🎉",
            color=BOTCOLOR,
            description="{} is now LEVEL 4!".format(message.author.name)
        )
        embed.add_field(
            name="Rewards:",
            value="- Active Role",
            inline=False
        )
        await client.send_message(message.channel, embed=embed)

    if author_xp >= 400 and "level4" not in author_levels:
        add_level(message.author.id, "level4")

        embed = discord.Embed(
            title="LEVEL UP!!⏫🎉",
            color=BOTCOLOR,
            description="{} is now LEVEL 4!".format(message.author.name)
        )
        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!help"):
        embed = discord.Embed(
            title="Current Commands",
            color=BOTCOLOR,
            description="- `!help`\n"
                        "- `!role`\n"
                        "- `!r_role`\n"
                        "- `!xp`\n"
                        "- `!lb`\n"
                        "- `!github`\n"
        )

        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!role") and "level2" in author_levels:
        global role_msg_id
        global role_msg_user_id

        embed = discord.Embed(
            title="Available Roles:",
            color=BOTCOLOR,
            description="- Programmer = 🐤\n"
                        "- Gamer = 🎮\n"
                        "- Designer = 🎨"
        )
        msg = await client.send_message(message.channel, embed=embed)
        await client.add_reaction(msg, "🐤")
        await client.add_reaction(msg, "🎮")
        await client.add_reaction(msg, "🎨")

        role_msg_user_id = message.author.id
        role_msg_id = msg.id

    if message.content.lower().startswith("!role") and "level2" not in author_levels:
        await client.send_message(message.channel, "Sorry, du musst mindestens Level 2 sein!")

    if message.content.lower().startswith("!r_role") and "level2" in author_levels:
        global r_role_msg_id
        global r_role_msg_user_id

        embed = discord.Embed(
            title="Remove Role:",
            color=BOTCOLOR,
            description="- Programmer = 🐤\n"
                        "- Gamer = 🎮\n"
                        "- Designer = 🎨"
        )
        msg = await client.send_message(message.channel, embed=embed)
        await client.add_reaction(msg, "🐤")
        await client.add_reaction(msg, "🎮")
        await client.add_reaction(msg, "🎨")

        r_role_msg_user_id = message.author.id
        r_role_msg_id = msg.id

    if message.content.lower().startswith("!r_role") and "level2" not in author_levels:
        await client.send_message(message.channel, "Sorry, du musst mindestens Level 2 sein!")

    if message.content.lower().startswith("!github"):
        embed = discord.Embed(
            title="GitHub",
            color=BOTCOLOR,
            description="https://github.com/Grewoss/duckman-python_bot"
        )
        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!xp"):
        xp = get_xp(message.author.id)
        await client.send_message(message.channel, "Du hast {} XP".format(xp))

    user_timer[message.author.id] = time.time()
    
    if message.content.lower().startswith("!lb"):
        msg = "Leaderboard:```\n"
        
        counter = 1
        lb = list(map(lambda m: (m, get_xp(m.id)), message.server.members))
        lb = lb.sort(key=lambda x: x[1], reverse=True)
        
        for element in lb:
            member = element[0]
            xp = element[1]
            msg += f"{counter}. {member.name}: {xp} XP\n"
            
            if counter == 20:
                break
            else:
                counter += 1
        
        msg += "```"
        await client.send_message(message.channel, msg)


@client.event
async def on_reaction_add(reaction, user):
    msgid = reaction.message.id

    # ADD ROLES
    if reaction.emoji == '🐤' and msgid == role_msg_id and user.id == role_msg_user_id:
        for role in reaction.message.server.roles:
            if role.name.lower() == "programmer":
                await client.add_roles(user, role)

    if reaction.emoji == '🎮' and msgid == role_msg_id and user.id == role_msg_user_id:
        for role in reaction.message.server.roles:
            if role.name.lower() == "gamer":
                await client.add_roles(user, role)

    if reaction.emoji == '🎨' and msgid == role_msg_id and user.id == role_msg_user_id:
        for role in reaction.message.server.roles:
            if role.name.lower() == "designer":
                await client.add_roles(user, role)

    # REMOVE ROLES
    if reaction.emoji == '🐤' and msgid == r_role_msg_id and user.id == r_role_msg_user_id:
        for role in reaction.message.server.roles:
            if role.name.lower() == "programmer":
                await client.remove_roles(user, role)

    if reaction.emoji == '🎮' and msgid == r_role_msg_id and user.id == r_role_msg_user_id:
        for role in reaction.message.server.roles:
            if role.name.lower() == "gamer":
                await client.remove_roles(user, role)

    if reaction.emoji == '🎨' and msgid == r_role_msg_id and user.id == r_role_msg_user_id:
        for role in reaction.message.server.roles:
            if role.name.lower() == "designer":
                await client.remove_roles(user, role)


@client.event
async def on_member_join(member):
    db.create_user(member.id, member.name)
    user_count = 0
    log_channel = discord.Object('317560415699599362')
    general_channel = discord.Object('316177775239102464')
    await client.send_message(log_channel, "Willkomen {} auf unserem Server! 😊".format(member.mention))

    for user in member.server:
        user_count += 1

    if user_count in USER_GOALS:
        await client.send_message(general_channel, "Der Server hat so eben {} User erreicht 🚀".format(user_count))


async def random_status():
    await client.wait_until_ready()
    while not client.is_closed:
        time = random.randint(3600, 21600)
        await asyncio.sleep(time)
        choice = random.choice(RANDOM_STATUS)
        await client.change_presence(game=discord.Game(name=choice, type=0))


def add_xp(user_id: int, xp: int):
    try:
        user_data = db.find_user(user_id)
        before_xp = user_data["xp"]
        after_xp = before_xp + xp
        db.update_user(user_id, {"xp": after_xp})
        return after_xp
    except:
        db.update_user(user_id, {"xp": xp})
        return xp


def get_xp(user_id: int):
    try:
        user_data = db.find_user(user_id)
        user_xp = user_data["xp"]
        return user_xp
    except:
        return 0


def add_level(user_id: int, level: str):
    try:
        levels = db.find_user(user_id)["levels"]
        levels.append(level)
        db.update_user(user_id, {"levels": levels})
    except:
        pass

client.loop.create_task(random_status())
client.run(BOT_TOKEN)
