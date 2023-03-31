# want to improve this way more!
# need to fix this



import nextcord
import asyncio



def setup(bot):
    @bot.slash_command(name="create_ticket", description="Create a ticket")
    async def create_ticket(interaction: nextcord.Interaction):
        try:
            # Create a category for the ticket channels
            category_name = "Tickets"
            category = await interaction.guild.create_category(category_name)

            # Create a new ticket channel
            ticket_channel_name = f"ticket-{interaction.user.name}"
            overwrites = {
                interaction.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                interaction.user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
                bot.user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await interaction.guild.create_text_channel(ticket_channel_name, category=category, overwrites=overwrites)

            # Add reaction to the ticket message
            message = await ticket_channel.send(f"{interaction.user.mention} created a new ticket. React with 👍 to claim it!")
            await message.add_reaction("👍")

            # Wait for a reaction to the ticket message
            def check(reaction, user):
                return user != bot.user and reaction.message == message and str(reaction.emoji) == "👍"

            reaction, claimed_by = await bot.wait_for('reaction_add', check=check, timeout=3600.0)
        except asyncio.TimeoutError:
            await interaction.response.send_message("This ticket has been closed due to inactivity.")
            await category.delete()
            return
        except Exception as e:
            print(f"Error creating ticket: {e}")
            await interaction.response.send_message("An error occurred while creating your ticket.")
            return

        try:
            # Add the admin and the user who claimed the ticket to the same channel
            overwrites[claimed_by] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
            ticket_channel_name = f"ticket-{interaction.user.name}-{claimed_by.name}"
            ticket_channel.name = ticket_channel_name
            await ticket_channel.edit(overwrites=overwrites)

            # Notify the admin and the user who claimed the ticket
            await ticket_channel.send(f"{interaction.user.mention} and {claimed_by.mention} are now in a private chat.")
        except Exception as e:
            print(f"Error creating ticket: {e}")
            await interaction.response.send_message("An error occurred while creating your ticket.")
            return

        await interaction.response.send_message("Your ticket has been created successfully!")