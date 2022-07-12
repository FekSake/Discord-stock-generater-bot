# Discord-stock-generater-bot

❓ What is this? ❓

This is a bot similar to "Gen" bot, 
You can add stock to diffrent catagories and allow users to get items.
You can limit the guilds, channels and roles which can be used in the gen.
To add or remove catagoies you need administrator permissions.

❓ How to setup the bot ❓

First, You have to create a bot. If you already have a bot you can ignore these steps.

  ❓ How to make a bot ❓

  1. Make sure you have a discord account and head over to https://discord.com/developers/applications and login.
  2. After logging in press on "New Application", Add a name and click "Create"
  3. After creating your application, Press on the "Bot" tab on the left and "Add Bot"
  4. You can add a description and name for the bot.
  5. Press reset Token and copy the text which appears. Do not share this with anyone as it is your bots authenication token and others will be able to controll your bot with it.
  6. Scroll down to Privileged Gateway Intents and enable MESSAGE CONTENT INTENT (This is required if you are using py-cord instead of discord.py)
  7. Click on OAuth2 and then URL Generator and choose Bot in the scopes menu, In bot permissions to make it easier just select Administrator and open the Generated URL.
  8. Invite your bot to your server and done.

  ❓ How to setup the bot ❓

  1. Download and open the code either in a text editor such as Notepad or VSC or upload to replit and navigate to config.json
  2. Replace the Token Goes Here text with your bots token.
  3. If you wish you can edit the embed colour, prefix and delay.
  4. Get your guilds ID by right clicking on the logo and click Copy ID, (Must have developer mode enabled in Advanced settings) and paste it into the allowed_guilds array
  5. Do the same forthe channels and roles you want to be able to use the bot.
  6. After this is complete. Run main.py and the bot should come online. It will also create a Flask localhost website for users running in replit so they can have a free 24/7 host ()
  7. Your bot should now be online.
  
  ❓ How to add stock ❓

  1. Make sure you have the items in a text file seperated by a new line
  2. Either DM the bot (owner only) or use a text channel where it is allowed, ".add " followed by the name of the catagory. For example ".add spotify" and attach the file with the items
  3. It should now be added into stock.json where you can manually edit items.

  ❓ How to remove stock ❓

  1. To remove stock first do .stock and find the name of the catagory
  2. Afterwards either DM the bot (owner only) or use a text channel where it is allowed, ".remove " followed by the name of the catagory.
  3. The catagory should now be removed.

  ❓ How to get item ❓
  
  1. First make sure you are in a allowed guild/channel and have the needed roles
  2. type ".stock" and find a item in stock
  3. type ".gen " followed by the name of the item. The bot then will DM you the item you requested. Be quick it deleted the message after 3 minutes!


This was a small bot my freind asked me to make, If there are any bugs or improvements you want me to add, Open a issue or pull request. Thanks!
