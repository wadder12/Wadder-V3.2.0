
# good rules!


import nextcord

def setup(bot):
    @bot.slash_command(name="rules", description="Send server rules to a specified channel")
    async def send_rules(interaction: nextcord.Interaction):
        # Check if user is an admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("You do not have permission to use this command.")
            return
        
        
         # Prompt the user to enter the channel name
        await interaction.response.send_message(content='Please enter the name of the channel you want to send the rules to:')

        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        try:
            channel_name = await bot.wait_for('message', check=check, timeout=60)
        except nextcord.TimeoutError:
            await interaction.send("You took too long to respond.")
            return

        await interaction.send('Please enter the rules, one by one. Type `done` when you are finished.')

        rules = []
        while True:
            try:
                rule_message = await bot.wait_for('message', check=check, timeout=60)
            except nextcord.TimeoutError:
                await interaction.send('You took too long to respond.')
                return

            if rule_message.content.lower() == 'done':
                break

            rules.append(rule_message.content)

        channel = nextcord.utils.get(interaction.guild.channels, name=channel_name.content)

        if channel is None:
            await interaction.send('Channel not found.')
            return

        # Send an embed with the title "Server Rules" and a book icon
        intro_embed = nextcord.Embed(description="📖 Server Rules")
        await channel.send(embed=intro_embed)

        # Send each rule in a separate embed
        for i, rule in enumerate(rules):
            embed = nextcord.Embed(title=f'Rule {i+1}:')
            embed.description = rule
            await channel.send(embed=embed)

        await interaction.send('Rules sent to ' + channel_name.content + '.')