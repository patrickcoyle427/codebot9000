from discord import Member
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown 
from discord.utils import get

from datetime import datetime

import csv

class Codez(Cog):

    def __init__(self, bot):

        self.bot = bot
        self.authorized_users = (450433098811703317,)
        # User IDs of anyone who has access to these bot commands.
        # Add discord User IDs here to grant access
        
    @command(name='codes')
    async def pass_out_codes(self, ctx, filename):

        # reads a csv of codes
        # iterates over list and dms codes to people who post images in the chat
        # saves a list of codes that were given
        # when finished, gives the user a new csv with all the used codes removed from it.
        # uses datetime to write when the last time a code was given, if was less than 5 days ago,
        # the post is passed

        blacklist = (733115855596159036,
                     733124808434384947,
                     733156872378646611,
                     718418078479679490,
                     683296799854952595,
                     733170081776795678)
        #put the discord ID of users that you wish to skip over in this tuple

        code_list = []

        today = datetime.now()

        date_range = 4
        # Check this many days back when sending codes, so as not to send codes to people from the prior week.

        target_channel = self.bot.get_channel(self.bot.target_channel)
        # Set in the __init__ file

        all_messages = await target_channel.history(limit=200).flatten()

        only_attachments = [message for message in all_messages if len(message.attachments) > 0 and message.author.id not in blacklist]
        # Only send codes to those who uploaded a picture, and only those not on the blacklist

        only_in_date_range = [message for message in only_attachments if message.created_at.day >= (today.day - date_range)]
        # Filters out older messages, if any

        with open(f'{filename}', newline='') as codes:

            codereader = csv.reader(codes, delimiter=',')

            codes_pt1 = list(codereader)

            for row in codes_pt1:

                for pre_split in row:

                    split_up = pre_split.split()

                    code_list.extend(split_up)
                    
        code_len = len(code_list)
        user_len = len(only_in_date_range)

        both = zip(only_in_date_range, code_list)

        more_p_then_c = len(only_in_date_range) > len(code_list)
        # checks if there are more messages to send codes to than codes to be sent

        for message, code in both:

            to_dm = message.author

            msgd_already = self.bot.already_messaged.get(to_dm, False)

            if msgd_already != True:

                await to_dm.send('Thanks for being a part of the AU Discord Server! Here is your code for MTG Arena! If there is a problem with your code, please message Pat and he will help you!')
                await to_dm.send(f'{code}')

                self.bot.already_messaged[to_dm] = True

        to_send = []

        if more_p_then_c:

            remaining_users = people[code_len:]

            await ctx.reply(f'Here are the users that did not receive codes for {filename}:')

            for user in remaining_users:

                to_send.append(user)

                if len(to_send) > 5:

                    await ctx.reply(f'{to_send}')

                    to_send.clear()

            if len(to_send) > 0:

                await ctx.reply(f'{to_send}')

        else:

            remaining_codes = code_list[user_len:]

            await ctx.reply(f'Here are the unused codes for {filename}:')

            for code in remaining_codes:

                to_send.append(code)

                if len(to_send) > 10:

                    await ctx.reply(f'{to_send}')
                    to_send.clear()

                    # This is to get around the discord message limitation when there are too many users or codes left.

            if len(to_send) > 0:

                await ctx.reply(f'{to_send}')

        await self.bot.target_channel.send('I have passed out this week\'s arena codes! Thank you all for participating!')
        
    @Cog.listener()
    async def on_ready(self):

        if not self.bot.ready:

            self.bot.cogs_ready.ready_up('codez')

def setup(bot):

    bot.add_cog(Codez(bot))
