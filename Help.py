from discord.ext import commands
import discord
import math

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been reloaded!')
        
    @commands.command(name='help', aliases=['h', 'commands'], description='A list of commands!')
    async def help(self, ctx, cog="1"):
        helpEmbed = discord.Embed(title="Help Command", color=0xff0000)
        helpEmbed.add_field(name='Support Server:', value='https://discord.gg/H489j6h85P', inline=False)
        helpEmbed.set_thumbnail(url=ctx.author.avatar_url)
        
        cogs = [c for c in self.bot.cogs.keys()]
        
        totalPages = math.ceil(len(cogs) / 4)
        
        cog = int(cog)
        if cog > totalPages or cog < 1:
            await ctx.send(f'Invalid page number: `{cog}`.\nPlease choose from `{totalPages}` pages\nAlternatively, use `help` to see the first page!')
            return
        
        helpEmbed.set_footer(text=f'<> = Required, [] = Optional, Page {cog} of {totalPages}')
        
        neededCogs = []
        for i in range(4):
            x = i + (int(cog) - 1) * 4
            try:
                neededCogs.append(cogs[x])
            except IndexError:
                pass

        for cog in neededCogs:
            commandList = ''
            for command in self.bot.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                
                elif command.parent != None:
                    continue
                
                commandList += f"**{command.name}** - *{command.description}*\n"
            commandList += "\n"
            
            helpEmbed.add_field(name=cog, value=commandList, inline=False)
            
        await ctx.send(embed=helpEmbed)
    

def setup(bot):
    bot.add_cog(Help(bot))
