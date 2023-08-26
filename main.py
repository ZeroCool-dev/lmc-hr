# import discord
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
import datetime
from datetime import time
import os
import platform
import json
from dotenv import load_dotenv
import locale

locale.setlocale(locale.LC_ALL, '')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
target_channel_id = 1145077091986063420

@bot.event
async def on_ready():
    """
    The code in this event is executed when the bot is ready.
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("Develop By ZeroCool")
    print("-------------------")


@bot.command()
async def capture_messages(ctx, start_date, end_date):
    # Convert the input strings to datetime objects (you might need to adjust the format)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    channel = ctx.channel
    
    await ctx.send(f"Captured messages:\n{captured_messages}")

@bot.command()
async def lmchr(ctx, *args):
    subcommand = args[0] if args else None
    
    if subcommand == 'calculate_salary':
        if len(args) >= 3:
            start_date = (args[1] + ' 00:00:00') if args else None
            end_date   = (args[2] + ' 23:59:00') if args else None
            
            start_date2 = (args[1] + ' 00:00:00') if args else None
            end_date2   = (args[2] + ' 23:59:00') if args else None
            
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_date   = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            
            channel = ctx.channel
            
            messages = []
            data = []
            x = 0
            user = ''
            async for message in channel.history(limit=None, after=start_date, before=end_date):
                if str.__contains__(message.content, 'ON Time'):
                    msg = message.content.split('\n')
                    user = message.author.display_name
                    reactions = message.reactions
                    react = True
                    for reaction in reactions:
                        if reaction.emoji == '✅':
                            react = False
                            break                 
                    temp = []
                    if str.__contains__(message.content, 'ON Time') and react == True:   
                        for a in msg:
                            if len(a) > 0:
                                if str.__contains__(a, 'Tarikh'):
                                    temp.append(a.split(':')[1].strip())
                                    
                                if str.__contains__(a, 'Pangkat'):
                                    temp.append(a.split(':')[1].strip())
                                    
                                if str.__contains__(a, 'ON Time'):
                                    temp.append(a.split(':')[1].strip())
                                    
                                if str.__contains__(a, 'OFF Time'):
                                    temp.append(a.split(':')[1].strip())
                        await message.add_reaction('✅')
                        
                        data.append(json.dumps(temp))
                     

            total_working_salary = 0
            total_ot_salary = 0
            rate = 0
            name = ''
            position = ''
            for staff in data:
                punch_card = json.loads(staff)
                name = user
                position = punch_card[1]
                if str.__contains__(punch_card[1].lower(), 'kp'):
                    rate = 1600 / 60
                if str.__contains__(punch_card[1].lower(), 'tkp'):
                    rate = 1550 / 60
                if str.__contains__(punch_card[1].lower(), 'pa'):
                    rate = 1400 / 60
                if str.__contains__(punch_card[1].lower(), 'spc'):
                    rate = 1350 / 60
                if str.__contains__(punch_card[1].lower(), 'doctor'):
                    rate = 1100 / 60
                if str.__contains__(punch_card[1].lower(), 'nurse'):
                    rate = 850 / 60
                if str.__contains__(punch_card[1].lower(), 'int'):
                    rate = 600 / 60
                
                # CLOCK IN ----------------------------------------------------------------------
                if str.__contains__(punch_card[2], 'AM'):
                    if int(punch_card[2].split('AM')[0].split('.')[0]) >= 1 and int(punch_card[3].split('AM')[0].split('.')[0]) <= 3:
                        a = punch_card[2].replace('.', ':')
                        clock_in_ot = datetime.datetime.strptime(a, "%I:%M %p")
                        clock_in_ot = clock_out_ot + datetime.timedelta(days=1)
                        clock_in    = datetime.datetime.strptime('12:59 AM', "%I:%M %p")
                        clock_in    = clock_in + datetime.timedelta(days=1)
                    else:
                        a = punch_card[2].replace('.', ':')
                        clock_in = datetime.datetime.strptime(a, "%I:%M %p")
                        clock_in = clock_out_ot + datetime.timedelta(days=1)
                else:
                    a = punch_card[2].replace('.', ':')
                    clock_in = datetime.datetime.strptime(a, "%I:%M %p")
                    
                # CLOCK OUT ----------------------------------------------------------------------
                if str.__contains__(punch_card[3], 'AM'):
                    if int(punch_card[3].split('AM')[0].split('.')[0]) >= 1 and int(punch_card[3].split('AM')[0].split('.')[0]) <= 3:
                        a = punch_card[3].replace('.', ':')
                        clock_out_ot = datetime.datetime.strptime(a, "%I:%M %p")
                        clock_out_ot = clock_out_ot + datetime.timedelta(days=1)
                        clock_out    = datetime.datetime.strptime('12:59 AM', "%I:%M %p")
                        clock_out    = clock_out + datetime.timedelta(days=1)
                    else:
                        a = punch_card[3].replace('.', ':')
                        clock_out = datetime.datetime.strptime(a, "%I:%M %p")
                        clock_out = clock_out + datetime.timedelta(days=1)
                else:
                    a = punch_card[3].replace('.', ':')
                    clock_out = datetime.datetime.strptime(a, "%I:%M %p")

                diff = clock_out - clock_in
                minutes = diff.total_seconds() / 60
                total_working_salary += minutes * rate
                
                if 'clock_in_ot' in locals() and 'clock_out_ot' in locals() :
                    diff_ot = clock_out_ot - clock_in_ot
                    minutes_ot = diff_ot.total_seconds() / 60
                    total_ot_salary += minutes_ot * (5000 / 60)
                    
                if 'clock_in_ot' in locals() and 'clock_out_ot' not in locals() :
                    diff_ot = (datetime.datetime.strptime('03:00 AM', "%I:%M %p") + datetime.timedelta(days=1)) - clock_in_ot
                    minutes_ot = diff_ot.total_seconds() / 60
                    total_ot_salary += minutes_ot * (5000 / 60)
                    
                if 'clock_in_ot' not in locals() and 'clock_out_ot' in locals() :
                    diff_ot = clock_out_ot - (datetime.datetime.strptime('01:00 AM', "%I:%M %p") + datetime.timedelta(days=1))
                    minutes_ot = diff_ot.total_seconds() / 60
                    total_ot_salary += minutes_ot * (5000 / 60)                  
                    
            # Bandage Calculation
            channel = bot.get_channel(1144826573141315685)
            dynamic_vars = {}
            total_bandage = 0
            async for message in channel.history(limit=None, after=start_date, before=end_date):
                if message.author.display_name == name:
                    msg = message.content.replace("`", "").split('\n')
                    user = message.author.display_name
                    reactions = message.reactions
                    react = True
                    for reaction in reactions:
                        if reaction.emoji == '✅':
                            react = False
                            break
                    temp = []
                    if str.__contains__(message.content, 'JUMLAH BANDAGE') and react == True:   
                        for a in msg:
                            if len(a) > 0:
                                if str.__contains__(a, 'NAMA'):
                                    d = a.split(':')[1].strip()
                                    if d not in dynamic_vars:
                                        dynamic_vars[d] = 0                                   
                                    
                                if str.__contains__(a, 'JUMLAH BANDAGE'):
                                    total_bandage += int(a.split(':')[1].strip())
                                    
                        await message.add_reaction('✅')
                        
            channel = bot.get_channel(target_channel_id)
            total = total_working_salary + total_ot_salary + (total_bandage * 100)
            if user != '' and position != '': 
                await channel.send(f"```Name         : {name}\nDate         : {start_date2} - {end_date2}\nPosition     : {position}\nDaily Salary : RM {locale.format_string('%.2f', total_working_salary, True)}\nOver Time    : RM {locale.format_string('%.2f', total_ot_salary, True)}\nBandage Sale : RM {locale.format_string('%.2f', (total_bandage * 100), True)} ({total_bandage} Unit)\n\nTOTAL        : RM {locale.format_string('%.2f', total, True)}```")
            await ctx.message.delete()
        else :
            await ctx.send("incomplete")
    elif subcommand == 'bandage':
        if len(args) >= 3:
            start_date = (args[1] + ' 00:00:00') if args else None
            end_date   = (args[2] + ' 23:59:00') if args else None
            
            start_date2 = (args[1] + ' 00:00:00') if args else None
            end_date2   = (args[2] + ' 23:59:00') if args else None
            
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            end_date   = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            
            channel = ctx.channel
            
            dynamic_vars = {}
            async for message in channel.history(limit=None, after=start_date, before=end_date):
                msg = message.content.replace("`", "").split('\n')
                user = message.author.display_name
                reactions = message.reactions
                react = True
                for reaction in reactions:
                    if reaction.emoji == '✅':
                        react = False
                        break
                temp = []
                if str.__contains__(message.content, 'JUMLAH BANDAGE') and react == True:   
                    for a in msg:
                        if len(a) > 0:
                            if str.__contains__(a, 'NAMA'):
                                d = a.split(':')[1].strip()
                                if d not in dynamic_vars:
                                    dynamic_vars[d] = 0                                   
                                
                            if str.__contains__(a, 'JUMLAH BANDAGE'):
                                dynamic_vars[d] += int(a.split(':')[1].strip())
                                
                    await message.add_reaction('✅')
    else:
        await ctx.send("Invalid subcommand. Use '!lmchr function1' or '!lmchr function2'.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!special_command'):
        await message.channel.send("Special command detected!")

    if bot.user.mentioned_in(message):
        query = message.content.replace(bot.user.mention, '').strip()
        response = f"Received query: {query}"
        await message.channel.send(response)

    await bot.process_commands(message)
        
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)

# 30781696113729
# Token = MTE0NDgyNTA2MzMxMzUwNjMwNA.G9LCJg.hdWsRsBSNNVQ9ffgmIUvL8p8L4caToGNKVoOZU
# https://discord.com/api/oauth2/authorize?client_id=1144825063313506304&permissions=30781696113729&scope=bot