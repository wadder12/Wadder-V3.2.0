import nextcord
from nextcord.ext import commands

class CloudStorage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage = {}  # A dictionary to store file data
        
    @commands.command()
    async def upload(self, ctx, filename):
        """Upload a file to the cloud storage"""
        attachment = ctx.message.attachments[0]
        file_data = await attachment.read()
        self.storage[filename] = file_data
        await ctx.send(f"File {filename} uploaded successfully!")
        
    @commands.command()
    async def download(self, ctx, filename):
        """Download a file from the cloud storage"""
        if filename not in self.storage:
            await ctx.send(f"File {filename} not found in the cloud storage.")
        else:
            file_data = self.storage[filename]
            await ctx.send(file=nextcord.File(file_data, filename=filename))
            
    @commands.command()
    async def share(self, ctx, filename, user: nextcord.Member):
        """Share a file with another user"""
        if filename not in self.storage:
            await ctx.send(f"File {filename} not found in the cloud storage.")
        else:
            file_data = self.storage[filename]
            await user.send(file=nextcord.File(file_data, filename=filename))
            await ctx.send(f"File {filename} shared with {user.name} successfully!")
    
    @commands.command()
    async def delete(self, ctx, filename):
        """Delete a file from the cloud storage"""
        if filename not in self.storage:
            await ctx.send(f"File {filename} not found in the cloud storage.")
        else:
            del self.storage[filename]
            await ctx.send(f"File {filename} deleted from the cloud storage.")
    @commands.command()
    async def grant_access(self, ctx, filename, user: nextcord.Member):
        """Grant access to a file for a specific user"""
        if filename not in self.storage:
            await ctx.send(f"File {filename} not found in the cloud storage.")
        else:
            # Add user to the access list for the file
            if 'access_list' not in self.storage[filename]:
                self.storage[filename]['access_list'] = []
            self.storage[filename]['access_list'].append(user.id)
            await ctx.send(f"Access granted to file {filename} for user {user.name}")
            
    @commands.command()
    async def revoke_access(self, ctx, filename, user: nextcord.Member):
        """Revoke access to a file for a specific user"""
        if filename not in self.storage:
            await ctx.send(f"File {filename} not found in the cloud storage.")
        else:
            # Remove user from the access list for the file
            if 'access_list' in self.storage[filename]:
                if user.id in self.storage[filename]['access_list']:
                    self.storage[filename]['access_list'].remove(user.id)
                    await ctx.send(f"Access revoked to file {filename} for user {user.name}")
                else:
                    await ctx.send(f"User {user.name} does not have access to file {filename}")
            else:
                await ctx.send(f"No access list found for file {filename}")        
    # Add other methods for access control and security features
    
def setup(bot):
    bot.add_cog(CloudStorage(bot))