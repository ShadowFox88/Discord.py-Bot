from discord.ext import commands
import random

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been reloaded!')
        
    @commands.command(name='open-Discord', description='---')
    @commands.is_owner()
    async def path(self, ctx):
        await ctx.channel.send('''
        ```📁Discord
    - 📰 main.py
    - 📰 Help.py
    - 📰 Moderation.py
    - 📰 Owner.py
    - 📄 Token.txt
    - 💻 prefixes.json```''')
    
    @commands.command(name='open-main', description='---')
    @commands.is_owner()
    async def path2(self, ctx):
        await ctx.channel.send(f'''```Path = Discord/main\n\n\nContents:\n\nEconomy\nGiveaway\nPrefix```''')
        
    @commands.command(name='open-Help', description='---')
    @commands.is_owner()
    async def path3(self, ctx):
        await ctx.channel.send(f'''```Path = Discord/Help\n\n\nContents:\n\nHelp\nCog```''')
        
    @commands.command(name='client-Moderation', description='---')
    @commands.is_owner()
    async def path4(self, ctx):
        await ctx.channel.send(f'''```Path = Discord/Moderation\n\n\nContents:\n\nKick\nBan\nClear\nUnban\nCog```''')
        
    @commands.command(name='open-Owner', description='---')
    @commands.is_owner()
    async def path5(self, ctx):
        await ctx.channel.send(f'''```Path = Discord/Owner\n\n\nContents:\n\nOwner commands```''')
        
    @commands.command(name='open-Token', description='---')
    @commands.is_owner()
    async def path6(self, ctx):
        await ctx.channel.send(f'''```Path = Discord/Token\n\n\nContents:\n\nToken```''')
        
    @commands.command(name='open-Prefixes', description='---')
    @commands.is_owner()
    async def path7(self, ctx):
        await ctx.channel.send(f'''```Path = Discord/Prefixes\n\n\nContents:\n\nPrefixes```''')
        
    @commands.command(name='open-run-main', description='---')
    @commands.is_owner()
    async def path8(self, ctx):
        possibleErrors = ['Process finished with exit code 0', 'Error: ~ ctx ~ is not defined - line 457', 'Error: ~ message ~ is not defined - line 139', 'Bot Reloaded']
        outcome = random.choice(possibleErrors)
        await ctx.channel.send(f'''```Path = Discord/main (terminal)\n\n\nRunning...\n\n{outcome}```''')
        
def setup(bot):
    bot.add_cog(Owner(bot))
