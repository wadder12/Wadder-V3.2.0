import nextcord
from nextcord.ext import commands

class BugReportSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_bug_report_category(self, guild):
        category_name = "🤖・Bug Reports"
        existing_categories = [c.name for c in guild.categories]
        if category_name not in existing_categories:
            return await guild.create_category(category_name)
        else:
            return nextcord.utils.get(guild.categories, name=category_name)

    async def create_bug_report_channel(self, guild):
        bug_report_channel_name = "📁・bug-report-channel"
        existing_channels = [c.name for c in guild.channels]
        if bug_report_channel_name not in existing_channels:
            category = await self.create_bug_report_category(guild)
            return await category.create_text_channel(bug_report_channel_name)
        else:
            return nextcord.utils.get(guild.channels, name=bug_report_channel_name)

    async def create_bug_report(self, interaction):
        user = interaction.user
        guild = interaction.guild
        category = await self.create_bug_report_category(guild)
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            user: nextcord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        bug_report_channel = await category.create_text_channel(f"bug-report-{user.display_name.lower()}", overwrites=overwrites)
        admin_role = nextcord.utils.get(guild.roles, name="Admin")
        if admin_role:
            await bug_report_channel.set_permissions(admin_role, read_messages=True, send_messages=True)

        await interaction.response.send_message(f"Bug report created: {bug_report_channel.mention}", ephemeral=True)
        await bug_report_channel.send(f"{user.mention}, your bug report has been created. An admin will be with you shortly.\n\n{admin_role.mention} a new bug report has been created by {user.mention}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_bug_report_system(self, ctx):
        bug_report_channel = await self.create_bug_report_channel(ctx.guild)
        embed = nextcord.Embed(title="Bug Report", description="Click the button below to open a bug report.")
        button = nextcord.ui.Button(style=nextcord.ButtonStyle.red, label="Report Bug", custom_id="report_bug")
        view = nextcord.ui.View()
        view.add_item(button)
        await bug_report_channel.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nextcord.Interaction):
        if interaction.type == nextcord.InteractionType.component:
            if interaction.data["custom_id"] == "report_bug":
                await self.create_bug_report(interaction)

def setup(bot):
    bot.add_cog(BugReportSystemCog(bot))