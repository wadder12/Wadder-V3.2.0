

import nextcord


def setup(bot):
    @bot.slash_command(
    name='advertise_you',
    description='Advertise your server in a linked channel.'
)
    async def advertise_server(interaction: nextcord.Interaction, message: str):
        """
        Advertise the user's server in a linked channel.

        Args:
        - message (str): The advertisement message to send to the linked channel.
        """
        # Check if the user has permission to use this command
        if not interaction.channel.permissions_for(interaction.user).administrator:
            return await interaction.response.send_message('You must be an administrator to use this command.')

        # Retrieve the main server and the advertisement channel
        main_server = bot.get_guild(850958118049677312)
        ad_channel = main_server.get_channel(1024442696527523891) # change to avd channel 

        # Create the invite link with server icon and join button
        invite_link = await interaction.channel.create_invite(
            max_age=0,
            max_uses=0,
            unique=True,
            reason='Server advertisement invite'
        )
        invite_embed = nextcord.Embed(
            title='Join Our Server!',
            url=invite_link.url,
            description=f'Click the "Join" button below to join our server!\n{message}',
            color=nextcord.Color.blurple()
        )
        invite_embed.set_thumbnail(url=interaction.guild.icon.url)
        invite_embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
        invite_embed.set_footer(text='Server Advertisement Invite')

        # Send the advertisement message and the invite link to the advertisement channel
        await ad_channel.send(embed=invite_embed)

        # Send a confirmation message to the user
        await interaction.response.send_message('Your advertisement has been sent to the linked channel.')