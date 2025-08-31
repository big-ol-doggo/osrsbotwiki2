import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import aiohttp
import re
from dotenv import load_dotenv
import openai
from typing import Optional, List, Dict, Any
import random
import urllib.parse
import html

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OSRS_WIKI_BASE_URL = os.getenv('OSRS_WIKI_BASE_URL', 'https://oldschool.runescape.wiki')

# Initialize OpenAI if API key is provided
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def clean_html(html_content: str) -> str:
    """Clean HTML content and extract text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_content)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

class OSRSWikiSearcher:
    def __init__(self, base_url: str = OSRS_WIKI_BASE_URL):
        self.base_url = base_url
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def search_wiki(self, query: str) -> List[Dict[str, Any]]:
        """Search the OSRS Wiki for the given query"""
        session = await self.get_session()
        
        # Construct search URL
        search_url = f"{self.base_url}/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': 5,  # Limit to 5 results
            'srnamespace': 0  # Main namespace only
        }
        
        try:
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('query', {}).get('search', [])
                else:
                    return []
        except Exception as e:
            print(f"Error searching wiki: {e}")
            return []
    
    async def get_page_content(self, page_title: str) -> Optional[Dict[str, Any]]:
        """Get the content of a specific wiki page"""
        session = await self.get_session()
        
        # Get page content
        content_url = f"{self.base_url}/api.php"
        params = {
            'action': 'parse',
            'format': 'json',
            'page': page_title,
            'prop': 'text|sections',
            'section': 0  # Get the introduction section
        }
        
        try:
            async with session.get(content_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'parse' in data:
                        return {
                            'title': data['parse']['title'],
                            'content': data['parse']['text']['*'],
                            'sections': data['parse'].get('sections', [])
                        }
                return None
        except Exception as e:
            print(f"Error getting page content: {e}")
            return None
    
    async def get_random_page(self) -> Optional[Dict[str, Any]]:
        """Get a random page from the OSRS Wiki"""
        session = await self.get_session()
        
        # Get random page
        random_url = f"{self.base_url}/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'random',
            'rnnamespace': 0,  # Main namespace only
            'rnlimit': 1
        }
        
        try:
            async with session.get(random_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    random_pages = data.get('query', {}).get('random', [])
                    if random_pages:
                        return random_pages[0]
                return None
        except Exception as e:
            print(f"Error getting random page: {e}")
            return None
    
    async def get_recent_changes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent changes from the OSRS Wiki"""
        session = await self.get_session()
        
        # Get recent changes
        changes_url = f"{self.base_url}/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'recentchanges',
            'rcnamespace': 0,  # Main namespace only
            'rclimit': limit,
            'rcprop': 'title|timestamp|user|comment'
        }
        
        try:
            async with session.get(changes_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('query', {}).get('recentchanges', [])
                else:
                    return []
        except Exception as e:
            print(f"Error getting recent changes: {e}")
            return []
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()

# Initialize wiki searcher
wiki_searcher = OSRSWikiSearcher()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="search", description="Search the Old School RuneScape Wiki")
async def search_wiki(interaction: discord.Interaction, query: str):
    """Search the OSRS Wiki for information"""
    await interaction.response.defer()
    
    try:
        # Search for results
        results = await wiki_searcher.search_wiki(query)
        
        if not results:
            embed = discord.Embed(
                title="❌ No Results Found",
                description=f"No results found for '{query}' on the OSRS Wiki.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Create embed with search results
        embed = discord.Embed(
            title=f"🔍 Search Results for '{query}'",
            description=f"Found {len(results)} result(s) on the OSRS Wiki:",
            color=discord.Color.blue(),
            url=f"{OSRS_WIKI_BASE_URL}/Special:Search?search={urllib.parse.quote(query)}"
        )
        
        for i, result in enumerate(results[:3], 1):  # Show top 3 results
            title = result['title']
            snippet = result['snippet']
            
            # Clean up snippet
            snippet = clean_html(snippet)
            
            # Create page URL
            page_url = f"{OSRS_WIKI_BASE_URL}/{title.replace(' ', '_')}"
            
            embed.add_field(
                name=f"{i}. {title}",
                value=f"{snippet[:200]}...\n[Read More]({page_url})",
                inline=False
            )
        
        embed.set_footer(text="Click on the links to read more on the OSRS Wiki")
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while searching: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=error_embed)

@bot.tree.command(name="info", description="Get detailed information about a specific OSRS topic")
async def get_info(interaction: discord.Interaction, topic: str):
    """Get detailed information about a specific OSRS topic"""
    await interaction.response.defer()
    
    try:
        # First search for the topic
        results = await wiki_searcher.search_wiki(topic)
        
        if not results:
            embed = discord.Embed(
                title="❌ Topic Not Found",
                description=f"Could not find information about '{topic}' on the OSRS Wiki.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Get the first (most relevant) result
        best_match = results[0]
        page_title = best_match['title']
        
        # Get detailed content
        content = await wiki_searcher.get_page_content(page_title)
        
        if not content:
            embed = discord.Embed(
                title="❌ Content Error",
                description=f"Could not retrieve content for '{page_title}'.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Extract and clean content
        text = clean_html(content['content'])
        
        # Limit text length
        if len(text) > 1500:
            text = text[:1500] + "..."
        
        # Create embed
        embed = discord.Embed(
            title=f"📖 {page_title}",
            description=text,
            color=discord.Color.green(),
            url=f"{OSRS_WIKI_BASE_URL}/{page_title.replace(' ', '_')}"
        )
        
        # Add sections if available
        if content.get('sections'):
            sections_text = "**Available Sections:**\n"
            for section in content['sections'][:5]:  # Show first 5 sections
                sections_text += f"• {section['line']}\n"
            embed.add_field(name="📋 Sections", value=sections_text, inline=False)
        
        embed.set_footer(text="Click the title to view the full page on the OSRS Wiki")
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while getting information: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=error_embed)

@bot.tree.command(name="random", description="Get a random page from the OSRS Wiki")
async def random_page(interaction: discord.Interaction):
    """Get a random page from the OSRS Wiki"""
    await interaction.response.defer()
    
    try:
        # Get random page
        random_page_data = await wiki_searcher.get_random_page()
        
        if not random_page_data:
            embed = discord.Embed(
                title="❌ Error",
                description="Could not retrieve a random page from the OSRS Wiki.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        page_title = random_page_data['title']
        
        # Get page content
        content = await wiki_searcher.get_page_content(page_title)
        
        if not content:
            embed = discord.Embed(
                title="❌ Content Error",
                description=f"Could not retrieve content for '{page_title}'.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Extract and clean content
        text = clean_html(content['content'])
        
        # Limit text length
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        # Create embed
        embed = discord.Embed(
            title=f"🎲 Random Page: {page_title}",
            description=text,
            color=discord.Color.orange(),
            url=f"{OSRS_WIKI_BASE_URL}/{page_title.replace(' ', '_')}"
        )
        
        embed.set_footer(text="🎲 This is a random page from the OSRS Wiki")
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while getting random page: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=error_embed)

@bot.tree.command(name="recent", description="Show recent changes to the OSRS Wiki")
async def recent_changes(interaction: discord.Interaction, limit: int = 5):
    """Show recent changes to the OSRS Wiki"""
    await interaction.response.defer()
    
    try:
        # Limit the number of results
        if limit > 10:
            limit = 10
        elif limit < 1:
            limit = 5
        
        # Get recent changes
        changes = await wiki_searcher.get_recent_changes(limit)
        
        if not changes:
            embed = discord.Embed(
                title="❌ No Recent Changes",
                description="Could not retrieve recent changes from the OSRS Wiki.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Create embed with recent changes
        embed = discord.Embed(
            title=f"📝 Recent Changes ({len(changes)} items)",
            description="Recent edits to the OSRS Wiki:",
            color=discord.Color.purple(),
            url=f"{OSRS_WIKI_BASE_URL}/Special:RecentChanges"
        )
        
        for i, change in enumerate(changes, 1):
            title = change['title']
            user = change.get('user', 'Unknown')
            timestamp = change.get('timestamp', 'Unknown')
            comment = change.get('comment', 'No comment')
            
            # Clean up comment
            comment = clean_html(comment)
            if len(comment) > 100:
                comment = comment[:100] + "..."
            
            # Create page URL
            page_url = f"{OSRS_WIKI_BASE_URL}/{title.replace(' ', '_')}"
            
            embed.add_field(
                name=f"{i}. {title}",
                value=f"**Edited by:** {user}\n**Comment:** {comment}\n[View Page]({page_url})",
                inline=False
            )
        
        embed.set_footer(text="Click 'View Page' to see the full article")
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while getting recent changes: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=error_embed)

@bot.tree.command(name="ai", description="Get AI-enhanced information about an OSRS topic")
async def ai_info(interaction: discord.Interaction, topic: str):
    """Get AI-enhanced information about an OSRS topic (requires OpenAI API key)"""
    if not OPENAI_API_KEY:
        embed = discord.Embed(
            title="❌ OpenAI API Key Required",
            description="This command requires an OpenAI API key to be configured.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
    
    await interaction.response.defer()
    
    try:
        # Get wiki information first
        results = await wiki_searcher.search_wiki(topic)
        
        if not results:
            embed = discord.Embed(
                title="❌ Topic Not Found",
                description=f"Could not find information about '{topic}' on the OSRS Wiki.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Get content from the best match
        best_match = results[0]
        content = await wiki_searcher.get_page_content(best_match['title'])
        
        if not content:
            embed = discord.Embed(
                title="❌ Content Error",
                description=f"Could not retrieve content for '{best_match['title']}'.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        # Extract text content
        wiki_text = clean_html(content['content'])
        
        # Limit wiki text for API call
        if len(wiki_text) > 2000:
            wiki_text = wiki_text[:2000] + "..."
        
        # Create AI prompt
        prompt = f"""Based on the following information from the Old School RuneScape Wiki about '{topic}', provide a clear, concise, and helpful explanation:

Wiki Information:
{wiki_text}

Please provide:
1. A brief overview of what this is
2. Key details and important information
3. Any relevant tips or notes for players
4. Keep it concise and easy to understand

Format your response in a clear, structured way."""

        # Get AI response using new OpenAI API format
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains Old School RuneScape topics clearly and concisely."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Create embed
        embed = discord.Embed(
            title=f"🤖 AI Analysis: {best_match['title']}",
            description=ai_response,
            color=discord.Color.purple(),
            url=f"{OSRS_WIKI_BASE_URL}/{best_match['title'].replace(' ', '_')}"
        )
        
        embed.set_footer(text="AI-powered analysis based on OSRS Wiki data")
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred while getting AI information: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=error_embed)

@bot.tree.command(name="help", description="Show available commands and how to use them")
async def help_command(interaction: discord.Interaction):
    """Show help information"""
    embed = discord.Embed(
        title="🤖 OSRS Wiki Bot Help",
        description="This bot helps you search and get information from the Old School RuneScape Wiki!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🔍 /search [query]",
        value="Search the OSRS Wiki for information about a topic",
        inline=False
    )
    
    embed.add_field(
        name="📖 /info [topic]",
        value="Get detailed information about a specific OSRS topic",
        inline=False
    )
    
    embed.add_field(
        name="🎲 /random",
        value="Get a random page from the OSRS Wiki",
        inline=False
    )
    
    embed.add_field(
        name="📝 /recent [limit]",
        value="Show recent changes to the OSRS Wiki (default: 5, max: 10)",
        inline=False
    )
    
    embed.add_field(
        name="🤖 /ai [topic]",
        value="Get AI-enhanced analysis of an OSRS topic (requires OpenAI API key)",
        inline=False
    )
    
    embed.add_field(
        name="❓ /help",
        value="Show this help message",
        inline=False
    )
    
    embed.add_field(
        name="💡 Examples",
        value="""
• `/search dragon scimitar`
• `/info fishing`
• `/random`
• `/recent 8`
• `/ai money making`
• `/info quest guide`
        """,
        inline=False
    )
    
    embed.set_footer(text="Data sourced from the official Old School RuneScape Wiki")
    await interaction.response.send_message(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    
    embed = discord.Embed(
        title="❌ Error",
        description=f"An error occurred: {str(error)}",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

# Cleanup on bot shutdown
@bot.event
async def on_close():
    await wiki_searcher.close()

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables!")
        print("Please create a .env file with your Discord bot token.")
        exit(1)
    
    print("Starting OSRS Wiki Bot...")
    bot.run(DISCORD_TOKEN)
