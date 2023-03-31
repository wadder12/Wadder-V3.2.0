import nextcord
from nextcord.ext import commands

# needs some work on the roles!

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_messages = {}

    @commands.group(name="reactionrole")
    async def reactionrole(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid command. Use /reactionrole create to create a new reaction role message.")

    @reactionrole.command(name="create")
    async def create_reaction_role(self, ctx):
        # Ask the user for the channel where the reaction role message will be posted
        await ctx.send("Please provide the ID or mention of the channel where the reaction role message will be posted:")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        response = await self.bot.wait_for("message", check=check)
        try:
            channel = await commands.TextChannelConverter().convert(ctx, response.content)
        except commands.errors.ChannelNotFound:
            await ctx.send("Invalid channel. Please try again.")
            return

        # Ask the user for the message content
        await ctx.send("Please provide the content for the reaction role message:")
        response = await self.bot.wait_for("message", check=check)
        content = response.content

        # Ask the user for the reactions and roles
        reaction_roles = {}
        while True:
            await ctx.send("Please provide the emoji and role for the reaction role (e.g. :thumbsup: @Role):")
            response = await self.bot.wait_for("message", check=check)
            if response.content.lower() == "done":
                break
            try:
                emoji, role = response.content.split(" ", 1)
                emoji = await commands.EmojiConverter().convert(ctx, emoji)
                role = await commands.RoleConverter().convert(ctx, role)
                reaction_roles[emoji] = role
            except (commands.errors.EmojiNotFound, commands.errors.RoleNotFound, ValueError):
                await ctx.send("Invalid emoji or role. Please try again.")

        # Send the reaction role message
        message = await channel.send(content)
        for emoji in reaction_roles:
            await message.add_reaction(emoji)

        # Save the message and roles to the dictionary
        self.role_messages[message.id] = reaction_roles

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if the reaction is on a reaction role message
        if payload.message_id not in self.role_messages:
            return

        # Get the role for the reaction and add it to the user
        reaction_roles = self.role_messages[payload.message_id]
        if payload.emoji in reaction_roles:
            guild = self.bot.get_guild(payload.guild_id)
            role = reaction_roles[payload.emoji]
            member = guild.get_member(payload.user_id)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Check if the reaction is on a reaction role message
        if payload.message_id not in self.role_messages:
            return

        # Get the role for the reaction and remove it from the user
        reaction_roles = self.role_messages[payload.message_id]
        if payload.emoji in reaction_roles:
            guild = self.bot.get_guild(payload.guild_id)
            role = reaction_roles[payload.emoji]
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)

def setup(bot):
    bot.add_cog(ReactionRoles(bot))