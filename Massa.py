import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '+')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="To angry complains"))
    print('Ready to fight!')

@client.command(description='Poistaa viestejä, mutta tarvitset oikeudet.')
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    
@client.command(description='Botin ping- millisekuntteina.')
async def ping(ctx):
    await ctx.send(f'Delay {round(client.latency * 1000)}ms, sanoitko mua hitaaksi?!')

@client.command(description='Jos et ole admin, älä edes huomio tätä komentoa.')
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
  await member.kick(reason=reason)

@client.command(description='Super salainen ase- käytä varoen!')
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
  await member.ban(reason=reason)

@client.command(description='Mykistää tietyn henkilön.')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name='Mykistetty')

  if not mutedRole:
    mutedRole = await guild.create_role(name='Mykistetty')

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_messages=False)
  
  await member.add_roles(mutedRole, reason=reason)
  await ctx.send(f'Mykistetty {member.mention} syystä {reason}')
  await member.send(f'Sinut mykistettiin palvelimella {guild.name} syystä {reason}')

  @bot.command(description='Poistaa mykistyksen.')
  @commands.has_permissions(manage_messages=True)
  async def unmute(ctx, member: discord.Member):
     mutedRole = discord.utils.get(ctx.guild.roles, name='Mykistetty')
  
  await member.remove_roles(mutedRole)
  await ctx.send(f'Mykistys poistettu {member.mention}')
  await member.send(f'Sinut mykistyksesi poistettiin palvelimella {guild.name}')

@client.command(description='Kertoo viimeisimmän lisätyn asian.')
async def päivitys(ctx):
  await ctx.send('Mykistys -vielä kesken 3.3.2021')

@client.command()
async def quit(ctx):
    await ctx.send("Sammutetaan botti.")
    return await client.logout() # tämä vain sulkee botin.

TOKEN = os.environ['TOKEN']

client.run(TOKEN)

