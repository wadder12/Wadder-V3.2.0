import nextcord
from nextcord.ext import commands
import os



# User data storage
user_data = {}

# Experience points needed for each level
LEVELS = [5, 15, 30, 50, 75, 105, 140, 180, 225, 275]

async def update_data(user):
    if user not in user_data:
        user_data[user] = {}
        user_data[user]["experience"] = 0
        user_data[user]["level"] = 0

async def add_experience(user):
    user_data[user]["experience"] += 1
    level = user_data[user]["level"]
    
    if user_data[user]["experience"] >= LEVELS[level]:
        user_data[user]["level"] += 1
        return True
    return False

def setup(bot):
    @bot.command(name="level")
    async def level(ctx: commands.Context):
        user_id = ctx.author.id

        await update_data(user_id)
        level = user_data[user_id]["level"]
        experience = user_data[user_id]["experience"]

        embed = nextcord.Embed(title=f"{ctx.author.name}'s Level & Experience",
                            description=f"Level: {level}\nExperience: {experience}/{LEVELS[level]}")
        await ctx.send(embed=embed)
        
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
        
        user_id = message.author.id
        await update_data(user_id)
        level_up = await add_experience(user_id)

        if level_up:
            await message.channel.send(f"Congratulations {message.author.mention}, you've reached level {user_data[user_id]['level']}!")

        await bot.process_commands(message)