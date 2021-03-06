# Wikipedia plugin for vTox 

import discord
from discord.ext import commands

import wikipedia

class Wikipedia(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.info = {
            "name": "Wikipedia",
            "desc": "Wikipedia by the wikipedia module.",
            "authors": "Jordy19",
            "version": "1.0"
        }

    @commands.command(
        pass_context=True,
        description='Fetch wikipedia articles.',
    )
    async def wiki(self, ctx, *args):
        if not args:
            await ctx.send("Error, this command requires an parameter: <article name>")
        else:
            suggestions = []
            try:
                article = wikipedia.page(" ".join(args))
            except wikipedia.exceptions.DisambiguationError as r:
                embed = discord.Embed(title='Wikipedia Search Suggestions', color=0xffd800)
                for suggestion in r.options:
                    suggestions.append(f"`{suggestion}`\n")
                embed.add_field(name='\u200b', value="".join(suggestions), inline=True)
                embed.set_footer(text=f"There are **{len(r.options)}** suggestions.")
                await ctx.send(embed=embed)
            except wikipedia.exceptions.WikipediaException as e:
                await ctx.send(f"Error, {e}")
            else:
                summary = wikipedia.summary(article.title, sentences=5)
                await ctx.send(summary)
                await ctx.send(f"{article.url}")

def setup(bot):
    bot.add_cog(Wikipedia(bot))