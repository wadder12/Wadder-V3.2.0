import json
import os

import nextcord
from nextcord.ext import commands

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = {}
        self.data_file = "leveling_data.json"
        self.vip_points = 50000
        self.vip_role_name = "VIP"
        self.load_level_data()

    def load_level_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.levels = json.load(f)
            print("Leveling data loaded successfully!")
        else:
            print("Leveling data file not found. Creating a new one.")
            self.save_level_data()

    def save_level_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.levels, f)
        print("Leveling data saved successfully!")

    def get_user_level(self, user_id):
        return self.levels.get(str(user_id), 0)

    def add_user_xp(self, user_id, xp):
        current_xp, current_level = self.levels.get(str(user_id), (0, 0))
        new_xp = current_xp + xp
        new_level = self.calculate_level(new_xp)
        self.levels[str(user_id)] = (new_xp, new_level)
        self.save_level_data()

        if new_level > current_level:
            return True
        else:
            return False

    def calculate_level(self, xp):
        return xp // 400

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        leveled_up = self.add_user_xp(message.author.id, 5)
        user_level = self.get_user_level(message.author.id)

        if leveled_up:
            embed = nextcord.Embed(title="Level Up!", description=f"{message.author.mention}, you've reached level {user_level}!", color=0x00FF00)
            await message.channel.send(embed=embed, ephemeral=True)

            if user_level * 400 == self.vip_points:
                vip_role = nextcord.utils.get(message.guild.roles, name=self.vip_role_name)
                if not vip_role:
                    vip_role = await message.guild.create_role(name=self.vip_role_name)
                await message.author.add_roles(vip_role)
                await message.channel.send(f"{message.author.mention} has been granted the {vip_role.name} role!", ephemeral=True)

    @commands.command()
    async def showlevel(self, ctx, user: nextcord.Member = None):
        if not user:
            user = ctx.author

        xp, level = self.levels.get(str(user.id), (0, 0))

        embed = nextcord.Embed(title=f"{user.display_name}'s Level", color=0x00ff00)
        embed.add_field(name="Level", value=level)
        embed.add_field(name="XP", value=xp)
        await ctx.send(embed=embed)    
        
def setup(bot):
    bot.add_cog(Leveling(bot))   
    
    
    #    Now the leveling system sends an embed when the user levels up, and users gain a level every 400 points. Additionally, the bot assigns the VIP role to users who reach 50,000 points. If the VIP role does not exist, the bot will create it. 