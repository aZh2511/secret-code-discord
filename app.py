import asyncpg
from discord.ext import commands

from config import PG_USER, PG_PASS, settings, CHANNEL_ID, DISCORD_LINK, ADMIN_IDS
from db_commands import database


async def run():
    """Connect to db on activation."""
    description = "Secret-code-bot"

    credentials = {"user": PG_USER, "password": PG_PASS, "database": "postgres", "host": "localhost"}
    db = await asyncpg.create_pool(**credentials)

    # Example create table code, you'll probably change it to suit you
    await db.execute("CREATE TABLE IF NOT EXISTS users(id bigint PRIMARY KEY, data text);")

    bot = commands.Bot(command_prefix=settings['prefix'], description=description, db=db)
    try:
        await bot.start(settings['token'])
    except KeyboardInterrupt:
        await db.close()
        await bot.logout()


bot = commands.Bot(command_prefix=settings['prefix'])


# user_id, username
@bot.command()
async def getdrops(ctx: commands.Context):
    """Send secret code or tell how to get."""
    author = ctx.message.author
    user_info = {
        'user_id': author.id,
        'username': str(author)
    }
    whitelist = await database.get_users_id()

    # Private messages
    if not ctx.message.guild:
        # Invite to channel
        if author.id not in whitelist:
            text = f"You must be a member of {DISCORD_LINK}\n{await database.get_text('text1')}"
            await ctx.send(text)
            # Send code
        else:
            secret_code = await database.get_code()
            text = f'Here is your code: {secret_code}\n {await database.get_text("text2")}'
            await ctx.send(text)
    # Channel
    else:
        # check channel id
        if ctx.message.guild.id == CHANNEL_ID:
            await database.add_new_user(user_info)
            text = await database.get_text('text3')
            await ctx.send(text)


@bot.command()
async def admin(ctx: commands.Context):
    """Send admin-panel."""
    if not ctx.author.bot:
        if not ctx.message.guild:
            if ctx.message.author.id in ADMIN_IDS:
                await ctx.send(f"""Welcome to admin-panel!

            Current code: {await database.get_code()}
        To update code send:
            $new_code code  - Where 'code' is new code.

            Current texts:
                id | text
            text1  -  {await database.get_text('text1')}
            text2  -  {await database.get_text('text2')}
            text3  -  {await database.get_text('text3')}
        To update texts:
            $new_text id text

        text1 - when someone tries to get code nor being a member of your channel.
        text2 - when user gets code
        text3 - is when user added for first time
        """)


@bot.command()
async def new_code(ctx: commands.Context):
    """Update secret-code in the db."""
    if not ctx.author.bot:
        if not ctx.message.guild:
            if ctx.message.author.id in ADMIN_IDS:
                try:
                    code = ctx.message.content.split(' ')[1]
                    await database.set_code(code)
                    await ctx.send(f'New code is: {code}')
                except IndexError:
                    await ctx.send('You must provide new code!')


@bot.command()
async def new_text(ctx: commands.Context):
    """Update texts in the db."""
    if not ctx.author.bot:
        if not ctx.message.guild:
            if ctx.message.author.id in ADMIN_IDS:
                try:
                    action = ctx.message.content.split(' ')[1]
                    texts = ctx.message.content.split(' ')[2:]
                    text = ''
                    for i in texts:
                        text += f'{i} '
                    available_ids = ['text1', 'text2', 'text3']
                    if action not in available_ids:
                        await ctx.send(f'You must choose between {available_ids}')
                        return None
                    await database.set_text(text, action)
                    await ctx.send('The text was successfully updated!')
                except IndexError:
                    await ctx.send('You must provide all information!\nExample: $new_text text1 Here is new text!')


bot.run(settings['token'])
