from discord.ext import commands
import discord

bot = commands.Bot(command_prefix='?', case_insensitive=True)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} Cog has been reloaded!')

    @commands.command(name='clear', aliases=['purge'], description='?clear <amount>')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx):
        '''Deletes Messages in current Text Channel'''
        amount = 100
        await ctx.channel.purge(limit=amount)
        
    @commands.command(name='kick', aliases=['k'], description='?kick <user> <reason>')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        '''Kick a member from current guild'''
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}. Reason = {reason}')
        
    @commands.command(name='ban', aliases=['b'], description='?ban <user> <reason>')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        '''Ban a member from current guild'''
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}. Reason = {reason}')
        
    @commands.command(name='unban', aliases=['ub'], description='?unban <user>')
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        '''Unban a member from current guild'''
        banned_users = await ctx.guild.bans()
        member_name, member_descriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if (user.name, user.discriminator) == (member_name, member_descriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                
    @commands.command(name='addrole', aliases=['+role'], description='?addrole <role> <user>')
    @commands.has_permissions(administrator=True)
    async def addrole(self, ctx, role : discord.Role, user : discord.Member):
        '''Add a role to a member'''
        await user.add_roles(role)
        em = discord.Embed(title='Added Role', color=0xff0000)
        em.add_field(name='Role:', value=role.mention)
        em.add_field(name='User:', value=user.mention)
        await ctx.send(embed=em)
        #await ctx.send(f'Successfully gave {role.mention} to {user.mention}!')
        
    @commands.command(name='removerole', aliases=['-role'], description='?removerole <role> <user>')
    @commands.has_permissions(administrator=True)
    async def removerole(self, ctx, role : discord.Role, user : discord.Member):
        '''Remove a role from a member'''
        await user.remove_roles(role)
        em = discord.Embed(title='Removed Role', color=0xff0000)
        em.add_field(name='Role:', value=role.mention)
        em.add_field(name='User:', value=user.mention)
        await ctx.send(embed=em)
        #await ctx.send(f'Successfully removed {role.mention} from {user.mention}!')
                
def setup(bot):
    bot.add_cog(Moderation(bot))
