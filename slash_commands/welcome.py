# welcome works like it pose to!

import nextcord



def setup(bot):
    @bot.slash_command(name='welcomer', description='Sets up welcome and leave channels.')
    async def setup(interaction: nextcord.Interaction, welcome_message: str, leave_message: str):
        guild = interaction.guild
        welcome_channel = await guild.create_text_channel('🎉welcome')
        leave_channel = await guild.create_text_channel('👋leave')

        async def send_embed(channel, title, color, user, message):
            embed = nextcord.Embed(title=title, color=color)
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="Message", value=message)
            await channel.send(embed=embed)

        async def on_member_join(member):
            settings = load_settings(member.guild.id)
            welcome_channel = member.guild.get_channel(settings['welcome_channel'])
            if welcome_channel:
                welcome_msg = f"🎉 {settings['welcome_message']} {member.mention}"
                await send_embed(welcome_channel, f"{member.name} joined the server", 0x00FF00, member, welcome_msg)

        async def on_member_remove(member):
            settings = load_settings(member.guild.id)
            leave_channel = member.guild.get_channel(settings['leave_channel'])
            if leave_channel:
                leave_msg = f"👋 {settings['leave_message']} {member.mention}"
                await send_embed(leave_channel, f"{member.name} left the server", 0xFF0000, member, leave_msg)

        def load_settings(guild_id):
            with open(f'{guild_id}_server_settings.txt', 'r') as f:
                return eval(f.read())

        def save_settings(guild_id, settings):
            with open(f'{guild_id}_server_settings.txt', 'w') as f:
                f.write(str(settings))

        settings = {
            'welcome_channel': welcome_channel.id,
            'leave_channel': leave_channel.id,
            'welcome_message': welcome_message,
            'leave_message': leave_message
        }

        save_settings(guild.id, settings)

        bot.add_listener(on_member_join, 'on_member_join')
        bot.add_listener(on_member_remove, 'on_member_remove')

        await interaction.response.send_message("Setup complete.", ephemeral=True)
    
    
    
    
    
    
    
    
    
    