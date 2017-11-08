import discord
import bot_token

client = discord.Client()
BOT_TOKEN = bot_token.bot_token()

BOTCOLOR = 0x547e34

role_msg_id = None
role_msg_user_id = None

r_role_msg_id = None
r_role_msg_user_id = None


@client.event
async def on_ready():
    print(client.user.name)
    print("================")


@client.event
async def on_message(message):

    if message.content.lower().startswith("!help"):
        embed = discord.Embed(
            title="Current Commands",
            color=BOTCOLOR,
            description="- `!help`\n"
                        "- `!role`\n"
                        "- `!r_role`\n"
        )

        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith("!role"):
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

    if message.content.lower().startswith("!r_role"):
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

    if message.content.lower().startswith("!github"):
        embed = discord.Embed(
            title="GitHub",
            color=BOTCOLOR,
            description="https://github.com/Grewoss/duckman-python_bot"
        )
        await client.send_message(message.content, embed=embed)


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

client.run(BOT_TOKEN)
