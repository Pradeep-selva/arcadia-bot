# ARCADIA DISCORD BOT
* This is a server specific discord bot written in python using the discord.py library, which wraps the discord API. 

* It takes care of server needs from verifying new users to temporarily banning them and also has some fun commands for server interactions. 
    
* There is also no shortage of utility functions like checking server stats regarding message counts and emote logging.
* The prefix is '+'.

## List of cogs
### Moderation
* This contains commands and event listeners for server moderation.
* These include verifying a user, temporarily banning a user and more!
### Stats
* This provides features to log daily message counts and emote usage to give a general overview of the server
### Utilities
* This provides users various utilities like, searching for a google image, viewing a codeforces profile, getting an anime summary, translating a foreign text to english and so on.
### Custom
* This holds commands that enable users to create their own custom commands to use in servers.
* Listing, updating and deleting these commands is also possible.
### RPS
* This holds commands to enable users to play rock, paper, scissors 1v1 and their score gets logged to a database which they can view.
### Fun
* This has a wide range of fun commands for server interactions.


## Dependencies
Dependencies can be found in `requirements.txt`

## Other
#### Database
Firebase
#### APIs used
* Google custom search API
* Bing image search API
* Google Translate API
* Codeforces API
* AniDB API
* Tatsumaki API
## License
[MIT](https://choosealicense.com/licenses/mit/)