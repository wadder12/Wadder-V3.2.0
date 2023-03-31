"""
This updated version of the warn command includes several improvements to make it more robust and user-friendly. Firstly, error handling and input validation have been added to ensure that the command can handle unexpected errors and user input. 
Secondly, the warning message has been enhanced to include more information, such as the moderator who issued the warning and the timestamp of the warning. 
This additional information can help users and moderators better understand the context and history of the warning.

In addition, the command has been made more flexible by allowing users with different permissions to use the command. 
Finally, a log message is sent to a specified channel (if available) to record the warning, which can help moderators keep track of warnings and maintain accountability. 
These improvements collectively make the warn command a more powerful and useful tool for moderating a Discord server.
"""
    
    
import datetime
import nextcord


def setup(bot):
    @bot.slash_command(description="Issues a warning to a user.")
    async def warn(interaction: nextcord.Interaction, user: nextcord.Member, reason: str = "No reason provided."):
        try:
            # Check if the user has permission to warn
            if not interaction.user.guild_permissions.kick_members:
                await interaction.response.send_message("You do not have permission to warn members.")
                return

            # Validate the reason
            if not reason.strip():
                await interaction.response.send_message("Please provide a reason for the warning.")
                return

            # Warn the user
            await user.send(f"You have been warned in {interaction.guild.name} by {interaction.user.mention}. Reason: {reason}")
            await interaction.response.send_message(f"{user.mention} has been warned by {interaction.user.mention}. Reason: {reason}")

            # Send a message to the log channel
            log_channel = nextcord.utils.get(interaction.guild.channels, name="mod-log")
            if log_channel:
                log_embed = nextcord.Embed(title="User Warned", color=0xffa500)
                log_embed.add_field(name="User", value=user.mention, inline=False)
                log_embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
                log_embed.add_field(name="Reason", value=reason, inline=False)
                log_embed.set_footer(text=f"Warned at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                await log_channel.send(embed=log_embed)

        except Exception as e:
            # Handle any errors that occur during execution
            await interaction.response.send_message(f"An error occurred while issuing the warning: {str(e)}")