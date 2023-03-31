

import nextcord


def setup(bot):
    @bot.slash_command()
    async def verifyrules2(interaction: nextcord.Interaction):
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) == '✅'

        # Create the embed for the rules
        rules_embed = nextcord.Embed(title="Server Rules", description="Please read and follow the rules below:")

        # Prompt the user to input the rules one by one
        await interaction.response.send_message('Please input the rules one by one. Type "quit" to finish:')
        rules = []
        while True:
            rule = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
            if rule.content.lower() == 'quit':
                break
            rules.append(rule.content)

        # Add the rules to the embed
        for i, rule in enumerate(rules):
            rules_embed.add_field(name=f"Rule {i+1}", value=rule, inline=False)

        # Prompt the user to specify the channel to send the rules to
        await interaction.followup.send('Please specify the channel to send the rules to (mention the channel):')
        channel_input = await bot.wait_for('message', check=lambda m: m.author == interaction.user and m.channel_mentions)
        channel = channel_input.channel_mentions[0]


        # Prompt the user to specify the role to assign to verified users
        await interaction.followup.send('Please specify the role to assign to verified users:')
        role_input = await bot.wait_for('message', check=lambda m: m.author == interaction.user)
        role_name = role_input.content
        print(f'Role name: {role_name}')
        role = nextcord.utils.get(interaction.guild.roles, name=role_name)
        print(f'Role: {role}')

        # Send the rules as an embed to the specified channel
        rules_message = await channel.send(embed=rules_embed)

        # Add the verification check mark
        await rules_message.add_reaction('✅')
        await interaction.followup.send(f'The rules have been sent to {channel.mention}. React with ✅ on the rules message to gain access to other areas of the Discord server.')

        # Wait for the user to react to the rules message
        reaction, user = await bot.wait_for('reaction_add', check=check)
        await user.add_roles(role)
        await interaction.followup.send(f'{user.mention} has been verified and now has access to other areas of the server.')