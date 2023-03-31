import os
import json
from datetime import datetime

import nextcord
from nextcord.ext import commands


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_data = {}
        self.data_file = "birthday_data.json"
        self.load_birthday_data()

    def load_birthday_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.birthday_data = json.load(f)
        else:
            self.birthday_data = {}
            self.save_birthday_data()  # Create the JSON file

    def save_birthday_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.birthday_data, f)

    def get_birthday(self, user_id):
        return self.birthday_data.get(str(user_id), None)

    def update_birthday(self, user_id, birthday):  # Renamed method
        self.birthday_data[str(user_id)] = birthday.strftime("%Y-%m-%d")
        self.save_birthday_data()
    
    
    
    def set_birthday(self, user_id, birthday):
        self.birthday_data[str(user_id)] = birthday.strftime("%Y-%m-%d")
        self.save_birthday_data()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return

        if not self.get_birthday(member.id):
            await member.send("Welcome to the server! 🎉 If you'd like to receive the special birthday role on your birthday, please enter your birthdate in the MM/DD/YYYY format. Rest assured, Wadder does not store any information about your birthday. 🎂")

            def check(m):
                return m.author == member and m.channel.type == nextcord.ChannelType.private

            try:
                message = await self.bot.wait_for("message", check=check, timeout=500)
                birthday = datetime.strptime(message.content, "%m/%d/%Y")
                self.set_birthday(member.id, birthday)
                await member.send("Thank you, your birthday has been set!")
            except nextcord.errors.TimeoutError:
                await member.send("Sorry, you didn't respond in time. Please set your birthday later using the command `set_birthday`.")

    @commands.command()
    async def set_birthday(self, ctx, birthday: str):
        try:
            birthday_date = datetime.strptime(birthday, "%m/%d/%Y")
        except ValueError:
            await ctx.send("Invalid date format. Please use the format `MM/DD/YYYY`.")
            return

        self.update_birthday(ctx.author.id, birthday_date)  # Updated method call
        await ctx.send("Your birthday has been set!")

    @commands.command()
    async def check_birthday(self, ctx, user: nextcord.Member = None):
        if not user:
            user = ctx.author

        birthday = self.get_birthday(user.id)
        if not birthday:
            await ctx.send(f"{user.display_name} hasn't set their birthday yet.")
            return

        birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
        today = datetime.utcnow().date()

        if birthday_date.month == today.month and birthday_date.day == today.day:
            await ctx.send(f"Happy birthday, {user.mention}!")
        else:
            await ctx.send(f"{user.display_name}'s birthday is on {birthday_date.strftime('%B %d')}.")

def setup(bot):
    bot.add_cog(Birthday(bot))