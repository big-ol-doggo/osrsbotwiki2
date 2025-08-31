# OSRS Wiki Discord Bot 🤖

A powerful Discord bot that searches and retrieves information from the [Old School RuneScape Wiki](https://oldschool.runescape.wiki/) using the MediaWiki API.

## Features ✨

- **🔍 Wiki Search**: Search the OSRS Wiki for any topic, item, quest, or skill
- **📖 Detailed Information**: Get comprehensive information about specific OSRS topics
- **🤖 AI-Enhanced Analysis**: Get AI-powered explanations and insights (requires OpenAI API key)
- **📋 Section Navigation**: View available sections of wiki pages
- **🔗 Direct Links**: Easy access to full wiki pages
- **⚡ Fast Responses**: Optimized async requests for quick results

## Commands 📝

| Command | Description | Example |
|---------|-------------|---------|
| `/search [query]` | Search the OSRS Wiki for information | `/search dragon scimitar` |
| `/info [topic]` | Get detailed information about a specific topic | `/info fishing` |
| `/ai [topic]` | Get AI-enhanced analysis (requires OpenAI API key) | `/ai money making` |
| `/help` | Show available commands and examples | `/help` |

## Setup Instructions 🚀

### 1. Prerequisites
- Python 3.8 or higher
- A Discord account
- Discord Bot Token (optional: OpenAI API key for AI features)

### 2. Create a Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token (you'll need this later)
5. Under "Privileged Gateway Intents", enable "Message Content Intent"

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Discord Bot Token (Get this from Discord Developer Portal)
DISCORD_TOKEN=your_discord_bot_token_here

# OpenAI API Key (Optional - for enhanced AI responses)
OPENAI_API_KEY=your_openai_api_key_here

# OSRS Wiki Base URL
OSRS_WIKI_BASE_URL=https://oldschool.runescape.wiki
```

### 5. Invite Bot to Your Server
1. Go to the "OAuth2" > "URL Generator" section in your Discord app
2. Select "bot" under scopes
3. Select the following permissions:
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 6. Run the Bot
```bash
python bot.py
```

## How It Works 🔧

### MediaWiki API Integration
The bot uses the MediaWiki API to interact with the OSRS Wiki:

- **Search API**: `api.php?action=query&list=search` - Searches for pages matching the query
- **Parse API**: `api.php?action=parse&prop=text|sections` - Retrieves page content and structure
- **Async Requests**: Uses `aiohttp` for efficient concurrent API calls

### Data Processing
1. **Search Results**: Fetches up to 5 relevant search results
2. **Content Extraction**: Parses HTML content using BeautifulSoup
3. **Text Cleaning**: Removes HTML tags and formats text for Discord embeds
4. **AI Enhancement**: (Optional) Uses OpenAI API to provide enhanced explanations

### Discord Integration
- **Slash Commands**: Modern Discord slash command interface
- **Rich Embeds**: Beautiful, formatted responses with links and sections
- **Error Handling**: Graceful error handling with user-friendly messages
- **Async Operations**: Non-blocking operations for better performance

## Example Usage 💡

### Basic Search
```
/search dragon scimitar
```
Returns search results with snippets and links to relevant wiki pages.

### Detailed Information
```
/info fishing
```
Provides comprehensive information about fishing, including available sections.

### AI-Enhanced Analysis
```
/ai money making
```
Gets AI-powered analysis of money-making methods with tips and insights.

## API Endpoints Used 📡

The bot interacts with these MediaWiki API endpoints:

- **Search**: `https://oldschool.runescape.wiki/api.php?action=query&list=search`
- **Parse**: `https://oldschool.runescape.wiki/api.php?action=parse&prop=text|sections`
- **Base URL**: `https://oldschool.runescape.wiki`

## Features in Detail 🎯

### Search Functionality
- Searches across all wiki pages
- Returns top 5 most relevant results
- Provides snippets with context
- Direct links to full wiki pages

### Information Retrieval
- Fetches complete page content
- Extracts and cleans text
- Shows available page sections
- Limits content for Discord compatibility

### AI Enhancement
- Uses OpenAI GPT-3.5-turbo
- Provides structured explanations
- Includes player tips and insights
- Formats responses for easy reading

## Troubleshooting 🔧

### Common Issues

1. **Bot not responding to commands**
   - Ensure the bot has the correct permissions
   - Check that slash commands are synced
   - Verify the bot token is correct

2. **No search results**
   - Check your internet connection
   - Verify the OSRS Wiki is accessible
   - Try different search terms

3. **AI commands not working**
   - Ensure you have a valid OpenAI API key
   - Check your OpenAI account has credits
   - Verify the API key is correctly set in `.env`

### Error Messages
- **"DISCORD_TOKEN not found"**: Create a `.env` file with your bot token
- **"OpenAI API Key Required"**: Add your OpenAI API key to `.env` for AI features
- **"No Results Found"**: Try different search terms or check spelling

## Contributing 🤝

Feel free to contribute to this project! Some ideas:
- Add more search filters
- Implement caching for frequently searched topics
- Add support for other RuneScape wikis
- Create additional AI features

## License 📄

This project is open source and available under the MIT License.

## Support 💬

If you need help:
1. Check the troubleshooting section above
2. Review the Discord.py documentation
3. Check the MediaWiki API documentation
4. Open an issue on GitHub

## Credits 🙏

- **Data Source**: [Old School RuneScape Wiki](https://oldschool.runescape.wiki/)
- **Discord Library**: [discord.py](https://discordpy.readthedocs.io/)
- **AI Integration**: [OpenAI API](https://openai.com/api/)
- **Web Scraping**: [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

**Happy Scaping! 🎮**
