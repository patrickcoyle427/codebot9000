'''
CODEBOT9000 - Written by Patrick Coyle

Bot written to pass out MTG Arena codes on the Alternate Universes Discord
Server. This bot was written specificially to do that, as such to use this
on your server you will need to change any IDs for the AU server. I have labeled
anything that would need to change to do this check the __init__.

'''

from discord import Intents, Client
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from discord.ext.commands import Context

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import asyncio

PREFIX = '!'
OWNER_IDS = [450433098811703317]
COGS = ['codez']
# Finds and returns the name of all the cogs in the cog folder

class Ready(object):

    # gets cog commands ready to be used

    def __init__(self):

        for cog in COGS:

            setattr(self, cog, False)

    def ready_up(self, cog):

        setattr(self, cog, True)
        print(f'{cog} cog ready')

    def all_ready(self):

        return all ([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    
    def __init__(self):

        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()

        self.already_messaged = {}
        # holds the names of users when they get a code
        
        self.guild = None
        # Guild ID, this is set in on_ready
        
        self.scheduler = AsyncIOScheduler()

        self.target_channel = 693209843674382436
        # IDs of the channels the bot will be active in

        self.code_monkey = None
        # Person who will get the updates about what codes have been given out
        # This is set in on ready
        
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, help_command=None, intents=Intents.all())
        
    def setup(self):

        for cog in COGS:

            self.load_extension(f'lib.cogs.{cog}')
            print(f' {cog} cog loaded')

        print('setup complete')

    def run(self, VERSION):
        
        self.VERSION = VERSION

        print('running setup...')
        self.setup()

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            
            self.TOKEN = tf.read()

            print('Bot has launched!')
            
            super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send('Not ready for commands yet! Please wait a few seconds!')
        
    async def on_connect(self):
        
        print('Bot connected to discord!')

    async def on_disconnect(self):
        
        print('Bot disconnected')

    async def on_error(self, err, *args, **kwargs):
        
        if err == 'on_command_error':

            await args[0].send('Something went wrong.')

        await args[0].send('An error occured')

        raise

    async def on_command_error(self, ctx, exc):
        
        if isinstance(exc, CommandNotFound):

            pass

        if isinstance(exc, CommandOnCooldown):

            await ctx.reply(f'That command is on cooldown. Try again in {exc.retry_after:,.2f} seconds.')

        elif hasattr(exec, 'original'):

            raise exc.original

        else:

            raise exc

    async def on_ready(self):
        
        if not self.ready:

            while not self.cogs_ready.all_ready():
                await asyncio.sleep(0.5)

            self.guild = bot.get_guild(690715890433392682)
            # Set the server ID here

            self.code_moneky = self.guild.get_member(450433098811703317)
            # Set name of code manager here  

            self.ready = True

            print('Bot ready!')

        else:
            print('Bot reconnected!')

    async def on_message(self, message):
        
        if not message.author.bot:

            await self.process_commands(message)


bot = Bot()
