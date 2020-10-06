import discord
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.info = {
            "name": "Owner",
            "desc": "Owner-only commands",
            "authors": "Jordy19",
            "version": "1.0"
        }

    @commands.command(
        name='list',
        description='Lists all the available commands and plugins.',
    )
    async def plugin_list(self, ctx, *args):
        if not args:
            cog_list = []
            embed = discord.Embed(title='Available Plugins', color=0xffd800)
            for cog in self.bot.cogs:
                cog_text = f"{cog} ({len(self.bot.cogs[cog].get_commands())})"
                cog_list.append(cog_text)
                # cogs.append(cog_text)
            print(cog_list)
            embed.add_field(name='\u200b', value="\n".join(cog_list), inline=False)
            embed.set_footer(text="Use !list <plugin name> to see their commands.")       
            await ctx.send(embed=embed)
        else:
            cog = args[0].title()
            commands = []
            if cog in self.bot.cogs.keys():
                cog_commands = self.bot.get_cog(cog).get_commands()
                embed = discord.Embed(title='{} - Plugin Commands'.format(cog), color=0xffd800)

                for cmd in cog_commands:
                    # commands.append(cmd.name)
                    embed.add_field(name=cmd.name, value=cmd.description, inline=False)
                embed.set_footer(text=f"There are {len(cog_commands)} command(s) available.")
                await ctx.send(embed=embed)
                # await ctx.send(", ".join(commands))

                
    @commands.command(
        description='Plugin management, for all sub-commands type !plugin list',
    )
    @commands.is_owner()
    async def plugin(self, ctx, *args):
        if not args:
            await self.plugin_help(ctx, *args)
        elif args[0] == "list":
            await self.list(ctx, *args)
        elif args[0] == "load":
            await self.load(ctx, *args)
        elif args[0] == "unload":
            await self.unload(ctx, *args)
        elif args[0] == "reload":
            await self.reload(ctx, *args)
        else:
            await self.plugin_help(ctx, *args)

    async def list(self, ctx, *args):
        """Plugin List"""
        await ctx.send(f"**Loaded plugins:** {', '.join(self.bot.plugin_list['loaded'])}")

    async def load(self, ctx, *args):
        try:
            args[1]
        except IndexError:
            await ctx.send("Error, this command requires parameters: <plugin name>")
        else:
            name = args[1].title()
            if name in self.bot.plugin_list['loaded']:
                await ctx.send(f"Error, the plugin `{name}` is already loaded!")
            else:
                self.bot.plugin.load(args[1])
                await ctx.send(f"Plugin `{name}` has been loaded!")


    async def unload(self, ctx, *args):
        try:
            args[1]
        except IndexError:
            await ctx.send("Error, this command requires parameters: <plugin name>")
        else:
            name = args[1].title()
            try:
                self.bot.plugin.unload(name)
            except discord.ext.commands.errors.ExtensionFailed as r:
                await ctx.send(f"Errror: {r}")
            else:
                await ctx.send(f"Unloaded {name}!")

    async def reload(self, ctx, *args):
        try:
            args[1]
        except IndexError:
            await ctx.send("Error, this command requires parameters: <plugin name>")
        else:
            plugin_path = f"plugins.{args[1]}.plugin"
            try:
                self.bot.reload_extension(plugin_path)
            except discord.ext.commands.errors.ExtensionFailed as r:
                await ctx.send(f"Errror: {r}")
            else:
                await ctx.send(f"Reloaded {args[1]}!")

    async def plugin_help(self, ctx, *args):
        """Bots Help"""
        commands = [
            ["!list", " ", "Lists all the plugins that are loaded."],
            ["!reload", "<plugin>", "Reloads the plugin specified."],
            ["!load", "<plugin>", "Loads the plugin specified."],
            ["!unload", "<plugin>", "Unloads the plugin specified."]
        ]
        embed = discord.Embed(title='Help Commands for Plugin Management', color=0xffd800)
        for command in commands:
            embed.add_field(name='\u200b', value=f"""**{command[0]}** {command[1]}
                *{command[2]}*""", inline=False)
        embed.set_footer(text=f"There are {len(commands)} commands available.")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Owner(bot))