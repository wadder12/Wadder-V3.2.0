
# might need to fix this a lot!!!


import nextcord


def setup(bot):
    @bot.slash_command(description="Track when a user creates an invite to the server")
    async def invitetracker(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        """
        Track when a user creates an invite to the server.
        """
        invites = await interaction.guild.invites()
        num_invites = len(invites)

        async def on_invite_create(invite):
            nonlocal num_invites
            num_invites += 1
            embed = nextcord.Embed(title="New Invite Created", description=f"{invite.inviter} created invite {invite.code}. Total invites: {num_invites}", color=0x00ff00)
            if channel:
                await channel.send(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)

        bot.add_listener(on_invite_create, name='on_invite_create')

        if channel:
            embed = nextcord.Embed(title="Invite Tracker Started", description=f"Alert messages will be sent to {channel.mention}. Total invites: {num_invites}", color=0x00ff00)
            await interaction.response.send_message(embed=embed)
        else:
            embed = nextcord.Embed(title="Invite Tracker Started", description=f"Total invites: {num_invites}", color=0x00ff00)
            await interaction.response.send_message(embed=embed)