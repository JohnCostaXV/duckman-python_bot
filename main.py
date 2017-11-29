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
RANDOM_STATUS = ["!help", "Quack", "1337", "Duck you!", "I'm Batm... eh Duckman!", "Luke, i'm your duck", "!gamble"
                 , "!github"]
USER_GOALS = [80, 90, 100, 110, 120, 130, 140, 150]


reaction_msg_stuff = {"role_msg_id": None, "role_msg_user_id": None, "r_role_msg_id": None, "r_role_msg_user_id": None}

gamble_msg_stuff = {"gamble_msg_id": None, "gamble_msg_user_id": None}

user_timer = {}
user_spam_count = {}


@client.event
async def on_ready():
    print(client.user.name)
    print("================")
    try:
        for server in client.servers:
            for member in server.members:
                db.create_user(member.id, member.name)
                if member.id == "180546607626977280":
                    await client.send_message(member, "Online!")
        choice = random.choice(RANDOM_STATUS)
        await client.change_presence(game=discord.Game(name=choice, type=0))
    except Exception as e:
        print("Error {}".format(e))
    print("100%")


@client.event
async def on_message(message):

    try:
        if time.time() >= user_timer[message.author.id] + 2:
            user_spam_count[message.author.id] = 0
            message_length = len(message.content)
            if message_length > 5:
                add_xp(message.author.id, 1)
            if message_length > 50:
                add_xp(message.author.id, 2)
            if message_length > 150:
                add_xp(message.author.id, 2)

        if time.time() < user_timer[message.author.id] + 2:
            user_spam_count[message.author.id] += 1
            if user_spam_count[message.author.id] >= 4:
                remove_xp(message.author.id, 4)
                await client.send_message(message.author, "Bitte nicht spammen, du bekommst (-XP) fuers spammen!!")
            if user_spam_count[message.author.id] >= 10:
                remove_xp(message.author.id, 6)

    except KeyError:
        add_xp(message.author.id, 2)

    except Exception as e:
        fix_error(message.channel, e)

    author_xp = db.find_user(message.author.id)["xp"]
    author_levels = db.find_user(message.author.id)["levels"]

    try:
        if author_xp >= 10 and "level1" not in author_levels:
            add_level(message.author.id, "level1")

            embed = discord.Embed(
                title="LEVEL UP!!⏫🎉",
                color=BOTCOLOR,
                description="{} is now LEVEL 1!".format(message.author.name)
            )

            await client.send_message(message.channel, embed=embed)

        if author_xp < 10 and "level1" in author_levels:
            remove_level(message.author.id, "level1")

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

        if author_xp < 50 and "level2" in author_levels:
            remove_level(message.author.id, "level2")
            for role in message.author.roles:
                if role.name.lower() == "programmer" or role.name.lower() == "designer" or role.name.lower() == "gamer":
                    await client.remove_roles(message.author, role)

        if author_xp >= 100 and "level3" not in author_levels:
            add_level(message.author.id, "level3")

            embed = discord.Embed(
                title="LEVEL UP!!⏫🎉",
                color=BOTCOLOR,
                description="{} is now LEVEL 3!".format(message.author.name)
            )
            await client.send_message(message.channel, embed=embed)

        if author_xp < 100 and "level3" in author_levels:
            remove_level(message.author.id, "level3")

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

        if author_xp < 200 and "level4" in author_levels:
            remove_level(message.author.id, "level4")

        if author_xp >= 400 and "level5" not in author_levels:
            add_level(message.author.id, "level5")

            embed = discord.Embed(
                title="LEVEL UP!!⏫🎉",
                color=BOTCOLOR,
                description="{} is now LEVEL 5!".format(message.author.name)
            )
            await client.send_message(message.channel, embed=embed)

        if author_xp < 400 and "level5" in author_levels:
            remove_level(message.author.id, "level5")

        if author_xp >= 800 and "level6" not in author_levels:
            add_level(message.author.id, "level6")

            embed = discord.Embed(
                title="LEVEL UP!!⏫🎉",
                color=BOTCOLOR,
                description="{} is now LEVEL 6!".format(message.author.name)
            )
            await client.send_message(message.channel, embed=embed)

        if author_xp < 800 and "level6" in author_levels:
            remove_level(message.author.id, "level6")
    except Exception as e:
        fix_error(message.channel, e)

    if message.content.lower().startswith("!help"):
        embed = discord.Embed(
            title="Current Commands",
            color=BOTCOLOR,
            description="```\n"
                        "- !help\n"
                        "- !role\n"
                        "- !r_role\n"
                        "- !xp\n"
                        "- !lb\n"
                        "- !github\n"
                        "- !ping\n"
                        "- !gamble ~HIER_XP~\n"
                        "- !who\n"
                        "```"
        )

        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!role") and "level2" in author_levels:
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

        reaction_msg_stuff["role_msg_user_id"] = message.author.id
        reaction_msg_stuff["role_msg_id"] = msg.id

    if message.content.lower().startswith("!role") and "level2" not in author_levels:
        await client.send_message(message.channel, "Sorry, du musst mindestens Level 2 sein!")

    if message.content.lower().startswith("!r_role") and "level2" in author_levels:
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

        reaction_msg_stuff["r_role_msg_user_id"] = message.author.id
        reaction_msg_stuff["r_role_msg_id"] = msg.id

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

    if message.content.lower().startswith("!lb"):
        try:
            lb_data_msg = await client.send_message(message.channel, "Sammel Leaderboard Daten")
            leaderboard_str = "```\n"
            data = db.get_all()
            counter = 1
            # lb = list(map(lambda m: (m, get_xp(m.id)), message.server.members))

            lb = list(map(lambda m: (m, data[m.id]["xp"]), message.server.members))
            lb.sort(key=lambda x: x[1], reverse=True)
            for element in lb:
                member = element[0]
                xp = element[1]
                leaderboard_str += f"{counter}. {member.name}: {xp} XP\n"
                if counter == 20:
                    break
                else:
                    counter += 1
            leaderboard_str += "```"
            embed = discord.Embed(
                title="Leaderboard",
                color=BOTCOLOR,
                description=leaderboard_str
            )
            await client.send_message(message.channel, embed=embed)
            await client.delete_message(lb_data_msg)
        except Exception as e:
            await fix_error(message.channel, e)

    if message.content.lower().startswith('!ping'):
        await client.send_message(message.channel, "Pong")

    if message.content.lower().startswith('!who'):
        user_count = len(message.server.members)

        embed = discord.Embed(
            title="Server Members:",
            color=BOTCOLOR,
            description=user_count
        )

        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith('!add_xp') and message.author.id == "180546607626977280":
        text_in = message.content
        text_out = text_in[text_in.find("(") + 1:text_in.find(")")]

        for user in message.mentions:
            try:
                add_xp(user.id, int(text_out))
                await client.send_message(message.channel, "Added {} xp to {}".format(text_out, user.name))
            except:
                client.send_message(message.author, "Failed to add xp to {}".format(user.name))

    if message.content.lower().startswith('!remove_xp') and message.author.id == "180546607626977280":
        text_in = message.content
        text_out = text_in[text_in.find("(") + 1:text_in.find(")")]

        for user in message.mentions:
            try:
                remove_xp(user.id, int(text_out))
                await client.send_message(message.channel, "Removed {} xp from {}".format(text_out, user.name))
            except:
                await client.send_message(message.author, "Failed to remove xp from {}".format(user.name))

    if message.content.lower().startswith('!gamble') and message.channel.id == "378612791751475201":
        try:
            value = int(message.content.lower().replace('!gamble', "").replace(" ", ""))

            if author_xp < value:
                await client.send_message(message.channel, "Sorry, du hast nicht genug XP.")
            if author_xp >= value:
                embed = discord.Embed(
                    title="Gamble Game:",
                    color=BOTCOLOR,
                    description="- 10% Chance = 🐤\n"
                                "- 45% Chance = 🔵\n"
                                "- 45% Chance = 🔴"
                )
                msg = await client.send_message(message.channel, embed=embed)
                await client.add_reaction(msg, "🐤")
                await client.add_reaction(msg, "🔵")
                await client.add_reaction(msg, "🔴")
                await client.add_reaction(msg, "❔")

                gamble_msg_stuff["gamble_msg_id"] = msg.id
                gamble_msg_stuff["gamble_msg_user_id"] = message.author.id
                gamble_msg_stuff[message.author.id] = value
        except ValueError:
            await client.send_message(message.channel, "Bitte benutze nur Zahlen. Example: `!gamble 20`")
        except Exception as e:
            await fix_error(message.channel, e)

    if message.content.lower().startswith('!gamble') and not message.channel.id == "378612791751475201":
        await client.send_message(message.channel, "Bitte gamble nur im #Spam channel. :)")

    user_timer[message.author.id] = time.time()


@client.event
async def on_reaction_add(reaction, user):
    msgid = reaction.message.id
    try:
        # ADD ROLES
        if reaction.emoji == '🐤' and msgid == reaction_msg_stuff["role_msg_id"] and user.id == reaction_msg_stuff["role_msg_user_id"]:
            for role in reaction.message.server.roles:
                if role.name.lower() == "programmer":
                    await client.add_roles(user, role)

        if reaction.emoji == '🎮' and msgid == reaction_msg_stuff["role_msg_id"] and user.id == reaction_msg_stuff["role_msg_user_id"]:
            for role in reaction.message.server.roles:
                if role.name.lower() == "gamer":
                    await client.add_roles(user, role)

        if reaction.emoji == '🎨' and msgid == reaction_msg_stuff["role_msg_id"] and user.id == reaction_msg_stuff["role_msg_user_id"]:
            for role in reaction.message.server.roles:
                if role.name.lower() == "designer":
                    await client.add_roles(user, role)

        # REMOVE ROLES
        if reaction.emoji == '🐤' and msgid == reaction_msg_stuff["r_role_msg_id"] and user.id == reaction_msg_stuff["r_role_msg_user_id"]:
            for role in reaction.message.server.roles:
                if role.name.lower() == "programmer":
                    await client.remove_roles(user, role)

        if reaction.emoji == '🎮' and msgid == reaction_msg_stuff["r_role_msg_id"] and user.id == reaction_msg_stuff["r_role_msg_user_id"]:
            for role in reaction.message.server.roles:
                if role.name.lower() == "gamer":
                    await client.remove_roles(user, role)

        if reaction.emoji == '🎨' and msgid == reaction_msg_stuff["r_role_msg_id"] and user.id == reaction_msg_stuff["r_role_msg_user_id"]:
            for role in reaction.message.server.roles:
                if role.name.lower() == "designer":
                    await client.remove_roles(user, role)

        if reaction.emoji == "🐤" and msgid == gamble_msg_stuff["gamble_msg_id"] and user.id == gamble_msg_stuff["gamble_msg_user_id"]:
            value = gamble_msg_stuff[user.id]
            remove_xp(user.id, value)
            won_value0 = value * 10

            gamble_msg_stuff["gamble_msg_user_id"] = None
            win = random.randint(0, 19)
            if win in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if win in [9, 10, 11, 12, 13, 14, 15, 16, 17]:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if win in [18, 19]:
                await won_gamble(True, reaction.message.channel, reaction.emoji)
                await client.send_message(reaction.message.channel, "You won {} XP!".format(won_value0))
                add_xp(user.id, won_value0)

        if reaction.emoji == "🔵" and msgid == gamble_msg_stuff["gamble_msg_id"] and user.id == gamble_msg_stuff["gamble_msg_user_id"]:
            value = gamble_msg_stuff[user.id]
            remove_xp(user.id, value)
            won_value1 = value * 2

            gamble_msg_stuff["gamble_msg_user_id"] = None
            win = random.randint(0, 19)
            if win in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                await won_gamble(True, reaction.message.channel, reaction.emoji)
                await client.send_message(reaction.message.channel, "You won {} XP!".format(won_value1))
                add_xp(user.id, won_value1)
            if win in [9, 10, 11, 12, 13, 14, 15, 16, 17]:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if win in [18, 19]:
                await won_gamble(False, reaction.message.channel, reaction.emoji)

        if reaction.emoji == "🔴" and msgid == gamble_msg_stuff["gamble_msg_id"] and user.id == gamble_msg_stuff["gamble_msg_user_id"]:
            value = gamble_msg_stuff[user.id]
            remove_xp(user.id, value)
            won_value0 = value * 2

            gamble_msg_stuff["gamble_msg_user_id"] = None
            win = random.randint(0, 19)
            if win in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if win in [9, 10, 11, 12, 13, 14, 15, 16, 17]:
                await won_gamble(True, reaction.message.channel, reaction.emoji)
                await client.send_message(reaction.message.channel, "You won {} XP!".format(won_value0))
                add_xp(user.id, won_value0)
            if win in [18, 19]:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
        if reaction.emoji == '❔' and msgid == gamble_msg_stuff["gamble_msg_id"] and user.id == gamble_msg_stuff["gamble_msg_user_id"]:
            embed = discord.Embed(
                title="Gamble Info",
                color=BOTCOLOR,
                description="🐤 verzehnfacht deine bezahlten XP.\n"
                            "🔵 verdoppelt deine bezahlten XP.\n"
                            "🔴 verdoppelt deine bezahlten XP."
            )
            await client.send_message(reaction.message.channel, embed=embed)
    except Exception as e:
        await fix_error(reaction.message.channel, e)


@client.event
async def on_member_join(member):
    db.create_user(member.id, member.name)
    user_count = len(member.server.members)
    log_channel = discord.Object('317560415699599362')
    general_channel = discord.Object('316177775239102464')
    await client.send_message(log_channel, "Willkomen {} auf unserem Server! 😊".format(member.mention))

    if user_count in USER_GOALS:
        await client.send_message(general_channel, "Der Server hat so eben {} User erreicht 🚀".format(user_count))


async def random_status():
    await client.wait_until_ready()
    while not client.is_closed:
        time = random.randint(3600, 21600)
        await asyncio.sleep(time)
        choice = random.choice(RANDOM_STATUS)
        await client.change_presence(game=discord.Game(name=choice, type=0))


async def fix_error(channel, error):
    embed = discord.Embed(
        title="ERROR",
        color=BOTCOLOR,
        description="Hier ist der Error, versuch ihn zu fixen! ```{}```".format(error)
    )
    embed.add_field(
        name="Hier ist der GitHub Link.",
        value="https://github.com/Grewoss/duckman-python_bot"
    )
    await client.send_message(channel, embed=embed)


async def won_gamble(won: bool, channel, emoji):
    if won:
        embed1 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔵🔵🔴🔵🔴\n🔳🔳🔼🔳🔳")
        embed2 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔵🔴🔵🔴🔴\n🔳🔳🔼🔳🔳")
        embed3 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔴🔵🔴🔴🐤\n🔳🔳🔼🔳🔳")
        embed4 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔵🔴🔴🐤{}\n🔳🔳🔼🔳🔳".format(emoji))
        embed5 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔴🔴🐤{}🔵\n🔳🔳🔼🔳🔳".format(emoji))
        embed6 = discord.Embed(title="YOU WON!", color=BOTCOLOR, description="🔴🐤{}🔵🔴\n🔳🔳🔼🔳🔳".format(emoji))
        gamble_msg = await client.send_message(channel, embed=embed1)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed2)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed3)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed4)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed5)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed6)
    if not won:
        loose_emoji = '🔴'
        if emoji == '🐤':
            ranint = random.randint(0, 1)
            if ranint == 0:
                loose_emoji = '🔵'
            else:
                loose_emoji = '🔴'
        if emoji == '🔴':
            ranint = random.randint(0, 1)
            if ranint == 0:
                loose_emoji = '🔵'
            else:
                loose_emoji = '🐤'
        if emoji == '🔵':
            ranint = random.randint(0, 1)
            if ranint == 0:
                loose_emoji = '🐤'
            else:
                loose_emoji = '🔴'

        embed1 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔵🔴🔵🔵🐤\n🔳🔳🔼🔳🔳")
        embed2 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔴🔵🔵🐤🔵\n🔳🔳🔼🔳🔳")
        embed3 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔵🔵🐤🔵🔴\n🔳🔳🔼🔳🔳")
        embed4 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🔵🐤🔵🔴{}\n🔳🔳🔼🔳🔳".format(loose_emoji))
        embed5 = discord.Embed(title="GAMBLE!", color=BOTCOLOR, description="🐤🔵🔴{}🔵\n🔳🔳🔼🔳🔳".format(loose_emoji))
        embed6 = discord.Embed(title="YOU LOOSE!", color=BOTCOLOR, description="🔵🔴{}🔵🔴\n🔳🔳🔼🔳🔳".format(loose_emoji))
        gamble_msg = await client.send_message(channel, embed=embed1)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed2)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed3)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed4)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed5)
        await asyncio.sleep(0.5)
        await client.edit_message(gamble_msg, embed=embed6)


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


def remove_xp(user_id: int, xp: int):
    try:
        user_data = db.find_user(user_id)
        before_xp = user_data["xp"]
        after_xp = before_xp - xp
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


def remove_level(user_id: int, level: str):
    try:
        levels = db.find_user(user_id)["levels"]
        levels.remove(level)
        db.update_user(user_id, {"levels": levels})
    except:
        pass


client.loop.create_task(random_status())
client.run(BOT_TOKEN)
