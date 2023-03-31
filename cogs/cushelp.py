import nextcord
from nextcord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping, ctx):
        embed = nextcord.Embed(title="Bot Commands", color=0x00FF00)
        for cog in mapping:
            if cog:
                cog_commands = await self.filter_commands(mapping[cog], sort=True)
                if cog_commands:
                    command_list = "\n".join(f"`{ctx.prefix}{cmd.name}`" for cmd in cog_commands)
                    embed.add_field(name=cog.qualified_name, value=command_list, inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog, ctx):
        embed = nextcord.Embed(title=f"{cog.qualified_name} Commands", color=0x00FF00)
        cog_commands = await self.filter_commands(cog.get_commands(), sort=True)
        command_list = "\n".join(f"`{ctx.prefix}{cmd.name}`" for cmd in cog_commands)
        embed.description = command_list

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command, ctx):
        embed = nextcord.Embed(title=f"`{ctx.prefix}{command.name}`", color=0x00FF00)
        embed.description = command.help or "No help provided."

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def command_callback(self, ctx, *, command=None):
        if command is None:
            return await self.send_bot_help(self.get_bot_mapping(), ctx)

        maybe_cog = self.context.bot.get_cog(command)
        if maybe_cog:
            return await self.send_cog_help(maybe_cog, ctx)

        maybe_command = self.context.bot.get_command(command)
        if maybe_command:
            return await self.send_command_help(maybe_command, ctx)

        await self.send_error_message(self.command_not_found(command))

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        # Restore original help command when cog is unloaded
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(CustomHelp(bot))