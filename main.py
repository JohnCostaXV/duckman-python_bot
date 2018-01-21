import discord
import random
import asyncio
import time
import datetime
import sys
try:
    import secret_stuff
except ModuleNotFoundError:
    print("Please create a secret_stuff.py file, go to github "
          "https://github.com/Grewoss/duckman-python_bot/blob/master/secret_stuff.py "
          "to see an example.")
    sys.exit(0)
import database

client = discord.Client()
BOT_TOKEN = secret_stuff.bot_token()
db = database.DataBase()


BOTCOLOR = 0x547e34
RANDOM_STATUS = ["!help", "Quack", "1337", "Duck you!", "I'm Batm... eh Duckman!", "Luke, i'm your duck", "!gamble"
                 , "!github", "gwo.io/", "I like {}".format("Python")]
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
        grewoss = None
        for server in client.servers:
            for member in server.members:
                db.create_user(member.id, member.name)
                if member.id == "180546607626977280":
                    grewoss = member
        choice = random.choice(RANDOM_STATUS)
        await client.change_presence(game=discord.Game(name=choice, type=0))
        await client.send_message(grewoss, "Online!")
    except Exception as e:
        print("Error {}".format(e))
    print("100%")


@client.event
async def on_message(message):

    if not message.author == "377935541028651008":
        if not message.channel.id == "378612791751475201":
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

            except discord.errors.HTTPException:
                pass

            except Exception as e:
                await fix_error(message.channel, e)

    author_xp = db.find_user(message.author.id)["xp"]
    author_levels = get_level(message.author.id)

    try:
        if author_xp >= 10 and author_levels <= 0:
            LEVEL = 1
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 10 and author_levels == 1:
            set_level(message.author.id, 0)
        if author_xp >= 50 and author_levels <= 1:
            LEVEL = 2
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 50 and author_levels == 2:
            set_level(message.author.id, 1)
            for role in message.author.roles:
                if role.name.lower() == "programmer" or role.name.lower() == "designer" or role.name.lower() == "gamer":
                    await client.remove_roles(message.author, role)
        if author_xp >= 100 and author_levels <= 2:
            LEVEL = 3
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 100 and author_levels == 3:
            set_level(message.author.id, 2)
        if author_xp >= 200 and author_levels <= 3:
            LEVEL = 4
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            for role in message.server.roles:
                if role.name.lower() == "active":
                    await client.add_roles(message.author, role)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 200 and author_levels == 4:
            set_level(message.author.id, 3)
        if author_xp >= 400 and author_levels <= 4:
            LEVEL = 5
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 400 and author_levels == 5:
            set_level(message.author.id, 4)
        if author_xp >= 800 and author_levels <= 5:
            LEVEL = 6
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 800 and author_levels == 6:
            set_level(message.author.id, 5)
        if author_xp >= 1100 and author_levels <= 6:
            LEVEL = 7
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 1100 and author_levels == 7:
            set_level(message.author.id, 6)
        if author_xp >= 1500 and author_levels <= 7:
            LEVEL = 8
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 1500 and author_levels == 8:
            set_level(message.author.id, 7)
        if author_xp >= 2000 and author_levels <= 8:
            LEVEL = 9
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 2000 and author_levels == 9:
            set_level(message.author.id, 8)
        if author_xp >= 2500 and author_levels <= 9:
            LEVEL = 10
            set_level(message.author.id, LEVEL)
            embed = generate_embed(message.author, LEVEL)
            await client.send_message(message.channel, embed=embed)
        if author_xp < 2500 and author_levels == 10:
            set_level(message.author.id, 9)

    except discord.errors.HTTPException:
        pass
    except Exception as e:
        await fix_error(message.channel, e)

    if message.content.lower().startswith("!clear_lvl") and message.author.id == "180546607626977280":
        for server in client.servers:
            for member in server.members:
                set_level(member.id, 0)

    if message.content.lower().startswith("!help"):
        embed = discord.Embed(
            title="__**Current Commands**__",
            color=BOTCOLOR,
            description="**> !help**\n"
                        "**> !role**\n"
                        "**> !r_role**\n"
                        "**> !xp**\n"
                        "**> !xp @username @username2 @username3...**\n"
                        "**> !lb**\n"
                        "**> !github**\n"
                        "**> !ping**\n"
                        "**> !gamble ~HIER_XP~**\n"
                        "**> !who**\n"
                        "**> !level**\n"
                        "**> !avg_xp**\n",
            url="https://gwo.io"
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/"
                                "377935541028651008/246f7bd36407fc95cb10c5c77658b42c.png")

        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!role") and author_levels >= 2:
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

    if message.content.lower().startswith("!role") and author_levels < 2:
        await client.send_message(message.channel, "Sorry, du musst mindestens Level 2 sein!")

    if message.content.lower().startswith("!r_role") and author_levels >= 2:
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

    if message.content.lower().startswith("!r_role") and author_levels < 2:
        await client.send_message(message.channel, "Sorry, du musst mindestens Level 2 sein!")

    if message.content.lower().startswith("!github"):
        embed = discord.Embed(
            title="GitHub",
            color=BOTCOLOR,
            description="https://github.com/Grewoss/duckman-python_bot"
        )
        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!xp"):
        if message.content.lower() == "!xp":
            xp = get_xp(message.author.id)
            await client.send_message(message.channel, "Du hast {} XP".format(xp))
        else:
            msg = "```\n"
            for user in message.mentions:
                user_xp = get_xp(user.id)
                msg += "> {} hat {} XP\n".format(user.name, user_xp)
            msg += "```"
            await client.send_message(message.channel, msg)

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
        except discord.errors.HTTPException:
            pass
        except Exception as e:
            await fix_error(message.channel, e)

    if message.content.lower().startswith('!ping'):
        msg_time = message.timestamp.microsecond
        real_time = datetime.datetime.utcnow().microsecond
        ping_ms = str(abs(msg_time - real_time))[:-4]
        await client.send_message(message.channel, "Pong `{ping_ms}ms`".format(ping_ms=ping_ms))

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
            value = abs(int(message.content.lower().replace('!gamble', "").replace(" ", "")))
            gamble_msg_stuff[message.author.id] = value

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

        except ValueError:
            await client.send_message(message.channel, "Bitte benutze nur Zahlen. Example: `!gamble 20`")
        except discord.errors.HTTPException:
            pass
        except Exception as e:
            await fix_error(message.channel, e)

    if message.content.lower().startswith('!gamble') and not message.channel.id == "378612791751475201":
        await client.send_message(message.channel, "Bitte gamble nur im #Spam channel. :)")

    if message.content.lower().startswith('!level'):
        await client.send_message(message.channel, "Du bist Level: `{}`".format(get_level(message.author.id)))

    if message.content.lower().startswith('!avg_xp'):
        user_data = db.get_all()
        user_count = len(message.server.members)
        total_xp = 0
        for member in message.server.members:
            userxp = user_data[member.id]["xp"]
            total_xp += userxp

        sum = total_xp / user_count

        await client.send_message(message.channel, "Der XP durchschnitt aller user betraegt `{}` XP!".format(int(sum)))

    if message.content.lower().startswith('!restart') and message.author.id == "180546607626977280":
        await client.send_message(message.channel, "Restart...")
        await asyncio.sleep(2)
        sys.exit(0)

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
            if win <= 8:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if 9 <= win <= 17:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if win in [18, 19]:
                await won_gamble(True, reaction.message.channel, reaction.emoji)
                await client.send_message(reaction.message.channel, "`{}` won {} XP!".format(user.name, won_value0))
                add_xp(user.id, won_value0)

        if reaction.emoji == "🔵" and msgid == gamble_msg_stuff["gamble_msg_id"] and user.id == gamble_msg_stuff["gamble_msg_user_id"]:
            value = gamble_msg_stuff[user.id]
            remove_xp(user.id, value)
            won_value1 = value * 2

            gamble_msg_stuff["gamble_msg_user_id"] = None
            win = random.randint(0, 19)
            if win <= 8:
                await won_gamble(True, reaction.message.channel, reaction.emoji)
                await client.send_message(reaction.message.channel, "`{}` won {} XP!".format(user.name, won_value1))
                add_xp(user.id, won_value1)
            if 9 <= win <= 17:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if win in [18, 19]:
                await won_gamble(False, reaction.message.channel, reaction.emoji)

        if reaction.emoji == "🔴" and msgid == gamble_msg_stuff["gamble_msg_id"] and user.id == gamble_msg_stuff["gamble_msg_user_id"]:
            value = gamble_msg_stuff[user.id]
            remove_xp(user.id, value)
            won_value0 = value * 2

            gamble_msg_stuff["gamble_msg_user_id"] = None
            win = random.randint(0, 19)
            if win <= 8:
                await won_gamble(False, reaction.message.channel, reaction.emoji)
            if 9 <= win <= 17:
                await won_gamble(True, reaction.message.channel, reaction.emoji)
                await client.send_message(reaction.message.channel, "`{}` won {} XP!".format(user.name, won_value0))
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
    except discord.errors.HTTPException:
        pass
    except Exception as e:
        await fix_error(reaction.message.channel, e)


@client.event
async def on_member_join(member):
    db.create_user(member.id, member.name)
    user_count = len(member.server.members)
    log_channel = discord.Object('317560415699599362')
    general_channel = discord.Object('316177775239102464')
    await client.send_message(log_channel, "Willkommen {} auf unserem Server! 😊".format(member.mention))

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


def set_level(user_id: int, level: int):
    try:
        db.update_user(user_id, {"levels": level})
        return level
    except:
        pass


def get_level(user_id: int):
    try:
        levels = db.find_user(user_id)["levels"]
        return levels
    except:
        pass


def generate_embed(user, level: int):
    embed = discord.Embed(
        title="LEVEL UP!!⏫🎉",
        color=BOTCOLOR,
        description="{} is now LEVEL {}!".format(user.name, level)
    )

    if level == 2:
        embed.add_field(
            name="Rewards:",
            value="- Ability to set your Roles with `!role`.\n"
                  "Available roles: Programmer, Gamer, Designer",
            inline=False
        )

    if level == 4:
        embed.add_field(
            name="Rewards:",
            value="- Active Role",
            inline=False
        )

    return embed


client.loop.create_task(random_status())

try:
    client.run(BOT_TOKEN)
except discord.errors.LoginFailure:
    print(">>>> Please update the Bot Token in secret_stuff.py! <<<<")
    sys.exit(0)
