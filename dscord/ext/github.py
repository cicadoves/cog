from os import remove
from typing import List
from urllib.request import urlretrieve

from discord.ext import commands

from dscord.func import Db, code_wrap

base_url = 'https://raw.githubusercontent.com/'
db = Db('path')


async def extlist(ctx):
    logs = code_wrap('\n'.join(db.keys()))
    for log in logs: await ctx.send(log)


def basename(path: str) -> str:
    base = path.split('/')[-1]
    name = base.split('.')[0]
    return base, name


def extLoad(bot: commands.Bot, path: str):
    base, name = basename(path)
    url = base_url + path
    urlretrieve(url, base)
    try: bot.load_extension(name)
    except commands.ExtensionAlreadyLoaded:
        bot.reload_extension(name)
    finally: remove(base)


def extsLoad():
    for path in db.keys():
        try: extLoad(path)
        except Exception as e: print(e)


class GithubExt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('ghload', brief='path: [owner/repo/branch/filepath]')
    async def extsLoad(self, ctx, *paths):
        for path in paths:
            extLoad(self.bot, path)
            _, ext = basename(path)
            db.write(path, ext)
        await extlist(ctx)

    @commands.command('ghexts', brief='List exts')
    async def extsList(self, ctx):
        await extlist(ctx)

    @commands.command('ghreld', brief='Reload all exts')
    async def extsReload(self, ctx):
        extsLoad()
        await ctx.send('Done')
    
    @commands.command('ghunld', brief='Unload exts')
    async def extsUnload(self, ctx, *exts):
        for ext in exts:
            db.erase(str(ext))
            self.bot.unload_extension(ext)
        await extlist(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        extsLoad()


def setup(bot):
    bot.add_cog(GithubExt(bot))
