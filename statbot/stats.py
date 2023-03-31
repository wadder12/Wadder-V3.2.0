
# needs some serious fixing! 


import nextcord


# Define the counters
def member_count(guild):
    return len(guild.members)

def bot_count(guild):
    return len([member for member in guild.members if member.bot])

def online_members(guild):
    return len([member for member in guild.members if member.status == nextcord.Status.online])

def voice_channels(guild):
    return len(guild.voice_channels)

def text_channels(guild):
    return len(guild.text_channels)

def roles(guild):
    return len(guild.roles)

def emojis(guild):
    return len(guild.emojis)

COUNTERS = {
    'members': member_count,
    'bots': bot_count,
    'online': online_members,
    'voice_channels': voice_channels,
    'text_channels': text_channels,
    'roles': roles,
    'emojis': emojis,
}


# Function to update the counters
async def update_counters(guild):
    for channel in guild.channels:
        if channel.name.startswith('Stats-'):
            counter_name = channel.name.split('-')[-1]
            counter_func = COUNTERS.get(counter_name)

            if counter_func:
                new_name = f'Stats-{counter_name}: {counter_func(guild)}'
                await channel.edit(name=new_name)


# Function to create or update the counters
async def create_counter_channel(guild, category, counter_name, counter_func):
    if len(category.channels) >= 5:
        return  # Reached maximum number of channels

    counter_channel_name = f'🔢 Stats-{counter_name}: {counter_func(guild)}'
    overwrites = {guild.default_role: nextcord.PermissionOverwrite(send_messages=False)}
    await guild.create_text_channel(counter_channel_name, overwrites=overwrites, category=category)


async def create_or_update_counters(guild, selected_counters=None):
    if selected_counters is None:
        selected_counters = COUNTERS.keys()

    category_name = "📊 ServerStats"
    category = nextcord.utils.get(guild.categories, name=category_name)

    if not category:
        category = await guild.create_category(category_name)

    for counter_name in selected_counters:
        counter_func = COUNTERS.get(counter_name)
        if counter_func:
            counter_channel_name = f'🔢 Stats-{counter_name}: {counter_func(guild)}'
            counter_channel = nextcord.utils.get(guild.channels, name=counter_channel_name, category=category)

            if not counter_channel:
                await create_counter_channel(guild, category, counter_name, counter_func)
            else:
                await update_counters(guild)