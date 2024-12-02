from discord import Intents, app_commands, Interaction, Message
from discord.ext import commands
from typing import Final
import os
from dotenv import load_dotenv
from database import checkstreak, get
import datetime

#streak_keyword: sets the word that must be typed in a channel to update the streak
#OPTIONAL: streak_time sets the time for a streak keyword to be effective. Use 24 hour format, if none type None

streak_keyword = "KEYWORD"
streak_time = None

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
now = datetime.datetime.now()

# Set up intents and bot
intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

# Register commands
streak_group = app_commands.Group(name="streak", description="Commands related to streaks")

@streak_group.command(name="current", description="Type a username to view their current streak!") #DONE
async def streak(interaction: Interaction, username: str):
    c = get(username, 1)
    if c != None:
        if c == 1: await interaction.response.send_message(str(username) + "'s current streak is " + str(c) + " day!")
        else: await interaction.response.send_message(str(username) + "'s current streak is " + str(c) + " days!")
    else:
        await interaction.response.send_message(str(username)+" has not set up streaks yet.")

@streak_group.command(name="leaders", description="See the top 3 streaks!") #DONEDONEDONE!!!
async def top_streaks(interaction: Interaction):
    fName, fHigh, sName, sHigh, tName, tHigh = get(None, 2)
    message = "**🏆 Streak Leaders! 🏆**\n\n"
    if len(fName) > 1:
        message += "🥇: **"
        for x in range (len(fName)):
            if x != len(fName)-1:
                message += fName[x] + ", "
            else:
                message += "and " + fName[x]
        message+= "** have a streak of **" + str(fHigh[0]) + "** days!"
    elif len(fName) == 1:
        message += "🥇: **" + fName[0] + "** with a streak of **" + str(fHigh[0]) + "** days! \n"
    if len(sName) > 1:
        message += "🥈: **"
        for x in range (len(sName)):
            if x != len(sName)-1:
                message += sName[x] + ", "
            else:
                message += "and " + sName[x]
        message+= "** have a streak of **" + str(sHigh[0]) + "** days!"
    elif len(sName) == 1:
        message += "🥈: **" + sName[0] + "** with a streak of **" + str(sHigh[0]) + "** days! \n"
    if len(tName) > 1:
        message += "🥉: **"
        for x in range (len(tName)):
            if x != len(tName)-1:
                message += tName[x] + ", "
            else:
                message += "and " + tName[x]
        message+= "** have a streak of **" + str(tHigh[0]) + "** days!"
    elif len(tName) == 1:
       message += "🥉: **" + tName[0] + "** with a streak of **" + str(tHigh[0]) + "** days! \n"
    await interaction.response.send_message(message)

@streak_group.command(name="best", description="Type a username to see their best streak!") #DONE
async def streak_best(interaction: Interaction, username: str):
    c= get(username, 3)

    if c != None:
        if c == 1: 
            await interaction.response.send_message(str(username) + "'s best streak is " + str(c) + " day!")
        else: 
            await interaction.response.send_message(str(username) + "'s best streak is " + str(c) + " days!")
    else:
        await interaction.response.send_message(str(username)+" has not set up streaks yet.")

@streak_group.command(name="all-time", description="See the all-time high streak for the server!") #DONE
async def streak_high(interaction: Interaction):
    high, indices, names = get(None, 4)
    if len(indices) == 1:
        await interaction.response.send_message(names[0] + " has the server record of " + str(high) +" days!")
    else:
        users = []
        if len(indices) == 2:
             await interaction.response.send_message(names[0] + " and "+ names[1] + " share the server record of " + str(high) + " days!")
        else:
            for x in range(len(indices)):
                users.append(names[indices[x-1]])
            name = ', '.join(users)
            await interaction.response.send_message(name + " share the server record of " + str(high) + " days!")
        
@streak_group.command(name="info", description="Type a username to view all info!") #DONE
async def streak(interaction: Interaction, username: str):
    c = get(username, 5)
    if c != None:
        current, best, timestamp = c
        await interaction.response.send_message(username + " has a current streak of " + str(current) + ", a best streak of " + str(best) + ", and their last streak update was on " + str(timestamp) + ".")
    else:
        await interaction.response.send_message(username + " has not set up streaks yet.")

# Add the command group to the bot's command tree
bot.tree.add_command(streak_group)

@bot.event
async def on_message(message: Message):
    if streak_time != None:
        if now.strftime("%H:%M") == streak_time:
            if message.author == bot.user: # Prevent the bot from responding to itself
                return
            if message.content.lower() == streak_keyword: # Check for streak keyword
                checkstreak(str(message.author))
    else:
        if message.author == bot.user: # Prevent the bot from responding to itself
                return
        if message.content.lower() == streak_keyword: # Check for streak keyword
                checkstreak(str(message.author))

# Sync the commands globally
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running')
    try:
        synced = await bot.tree.sync()  # Sync commands globally
        print(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Run the bot
def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
