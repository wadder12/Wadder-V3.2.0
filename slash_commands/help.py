# need to come back in and change this!


from functools import partial
import nextcord



def setup(bot):
    @bot.slash_command(name="help",description="Shows a list of available commands")
    async def help33333(interaction: nextcord.Interaction, channel: nextcord.TextChannel = None):
        # List of commands to display in the embed
        command_list = [
    ("/add", "Calculate the sum of two numbers"),
    ("/add_role", "Add a role to a user in the server"),
    ("/advertise", "Advertise the bot and its features"),
    ("/advertiseYOU", "Advertise your server in a linked channel"),
    ("/ban", "Ban a user from the server"),
    ("/calculate_average", "Calculate the average of a list of numbers"),
    ("/celsius", "Convert a temperature from Celsius to Fahrenheit"),
    ("/chatbot", "Chat with the OpenAI chatbot"),
    ("/chucknorris", "Get a random Chuck Norris joke"),
    ("/clear", "Deletes a specified number of messages from a channel"),
    ("/codeblock", "Return the input text as a code block"),
    ("/countdown", "Countdown to a specified event"),
    ("/define", "Get the definition of a word from the Merriam-Webster dictionary"),
    ("/deafen", "Deafen a user in a voice channel"),
    ("/encrypt_caesar", "Encrypt text using the Caesar cipher"),
    ("/flip", "Flip a coin"),
    ("/game_deals", "Sends a notification to the specified channel with details about any free or discounted games on Steam"),
    ("/game_deals2", "Sends a notification with details about any free or discounted games on Steam"),
    ("/generate_code2", "Generate code snippets using the Davinci 003 engine"),
    ("/generate_financial_advice", "Generate personalized financial advice using the Davinci 003 engine. This is for fun not to be used for real life!"),
    ("/generate_legal_document", "Generate legal documents using the Davinci 003 engine. Not true legal advice!"),
    ("/generate_lyrics", "Generate song lyrics using the Davinci 003 engine"),
    ("/generate_poem", "Generate a poem using the Davinci 003 engine"),
    ("/generate_product_name", "Generate a unique product name using the Davinci 003 engine"),
    ("/generate_program", "Generate a complex software program using the Davinci 003 engine"),
    ("/generate_story", "Generate a short story using the Davinci 003 engine"),
    ("/generate_technical_documentation", "Generate technical documentation using the Davinci 003 engine"),
    ("/horoscope", "Provides daily horoscope for the user's zodiac sign"),
    ("/kick", "Kick a user from the server"),
    ("/lock", "Locks a channel to prevent users from sending messages"),
    ("/lyrics", "Get the lyrics of a song"),
    ("/mute", "Mute a user in the server"),
    ("/mutevoice", "Mute a user in a voice channel"),
    ("/nickname", "Changes the nickname of a user on the server"),
    ("/ping", "Ping the bot to test its responsiveness"),
    ("/progjoke", "Get a random programming joke"),
    ("/quote_text", "Format text as a quote"),
    ("/random_quote", "Get a random quote"),
    ("/remind2", "Set a reminder message to repeat in a set amount of hours"),
    ("/remove_role", "Remove a role from a user in the serve"),
    ("/reverse", "Reverse a message"),
    ("/roll", "Roll some dice"),
    ("/send_news", "Send news updates to a specified channel"),
    ("/send_rules", "admin custom rules"),
    ("/serverinfo", "Display information about the server"),
    ("/setup_logging", "Logging channel set up"),
    ("/slowmode", "Sets the slowmode delay for a channel"),
    ("/suggest3", "Submit a suggestion"),
    ("/suggest4", "Submit a suggestion2"),
    ("/summarize", "Summarize text using the Davinci 003 engine"),
    ("/talk2", "Make the bot talk in a channel"),
    ("/tempban", "Temporarily bansa user from the server"),
    ("/translate", "Translate text to another language using Google Translate"),
    ("/unban", "Unban a user from the server"),
    ("/undeafen", "Undeafen a user in a voice channel"),
    ("/unlock", "Unlocks a locked channel"),
    ("/unmute", "Unmute a user in the server"),
    ("/unmutevoice", "Unmute a user in a voice channel"),
    ("/uptime", "Get the uptime of the bot"),
    ("/urban", "Get the definition of a word from the Urban Dictionary"),
    ("/usercount", "Get the number of users in the server"),
    ("/weather", "Get the current weather for a specified location"),
    ("/wiki", "Get a summary of a Wikipedia article"),
    ("/wolfram", "Get the answer to a question using Wolfram Alpha"),
    ("/youtube", "Search for a video on YouTube"),
    ("/ytstats", "Get statistics about a YouTube channel")




        ]

        # Divide the commands into pages of 10 commands each
        pages = [command_list[i:i + 10] for i in range(0, len(command_list), 10)]

        # Create an embed for each page of commands
        embeds = []
        for i, page in enumerate(pages):
            embed = nextcord.Embed(title=f"Page {i + 1}/{len(pages)}", color=0x7289da)
            for command, description in page:
                embed.add_field(name=command, value=description, inline=False)
            embeds.append(embed)

        # Create a view with buttons to navigate between pages
        view = nextcord.ui.View()
        for i in range(len(embeds)):
            button = nextcord.ui.Button(style=nextcord.ButtonStyle.secondary, label=str(i + 1))
            button.callback = partial(on_help_button_click, embeds, i, view)
            view.add_item(button)

        # Send the first page of commands with the view
        await interaction.response.send_message(embed=embeds[0], view=view)

    async def on_help_button_click(embeds, page_index, button, interaction):
        # Update the message with the embed for the clicked page
        message = interaction.message
        await message.edit(embed=embeds[page_index])
        
        # Update the style of the clicked button to indicate that it is selected
        view = interaction.message.view  # Access the view from the button
        for item in view.children:
            if isinstance(item, nextcord.ui.Button) and item.label == button.label:
                item.style = nextcord.ButtonStyle.primary
            else:
                item.style = nextcord.ButtonStyle.secondary

        await interaction.edit_original_message(content=message.content, view=view)