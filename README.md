# Discord Streaks
 Discord bot that has various commands useful in keeping streaks for servers. Stores information safely in a SQLite database. 100% written in Python.
 
**Commands:**
- **/streak current:** Displays the current streak of a user
- **/streak leaders:** Displays the server's top 3 current streaks
- **/streak best:** Displays the all-time best streak of a user
- **/streak all-time:** Displays the server's top 3 best streaks
- **/streak info:** Displays the database info for a user

**Usage:**
If using for your own server, create a new application at [https://discord.com/developers/applications](url). Under bot, give the bot access to read message history, use slash commands, and send messages. Create a file called .env and create a variable titled "DISCORD_TOKEN." This variable will store your Discord token ID. Once done, copy the install link in the developer portal to add the bot to your server.

**Hosting:**
Using Railway or Render are two great options to host the bot.

**Storage Information:**
All data is stored in a file that will automatically be created called "streaks.db". This is an SQLite3 file that stores the following information: username, current streak, best streak, and last update.

**Known Bugs:**
- Streak doesn't break until it is checked again by calling the streak keyword

