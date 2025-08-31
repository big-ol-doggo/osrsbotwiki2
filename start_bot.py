#!/usr/bin/env python3
"""
Startup script for the OSRS Wiki Discord Bot
This script checks dependencies and environment variables before starting the bot
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'discord.py',
        'requests',
        'beautifulsoup4',
        'python-dotenv',
        'aiohttp',
        'lxml'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your Discord bot token.")
        print("See env_example.txt for reference.")
        return False
    
    load_dotenv()
    
    discord_token = os.getenv('DISCORD_TOKEN')
    if not discord_token or discord_token == 'your_discord_bot_token_here':
        print("❌ DISCORD_TOKEN not set in .env file!")
        print("Please add your Discord bot token to the .env file.")
        return False
    
    print("✅ Environment variables loaded")
    return True

def test_wiki_connection():
    """Test connection to the OSRS Wiki"""
    try:
        import asyncio
        import aiohttp
        
        async def test_connection():
            async with aiohttp.ClientSession() as session:
                async with session.get('https://oldschool.runescape.wiki/api.php?action=query&format=json&list=search&srsearch=test&srlimit=1') as response:
                    if response.status == 200:
                        return True
                    return False
        
        result = asyncio.run(test_connection())
        if result:
            print("✅ OSRS Wiki connection successful")
            return True
        else:
            print("❌ OSRS Wiki connection failed")
            return False
    except Exception as e:
        print(f"❌ Error testing wiki connection: {e}")
        return False

def main():
    """Main startup function"""
    print("🤖 OSRS Wiki Discord Bot Startup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🔧 Checking environment...")
    if not check_env_file():
        sys.exit(1)
    
    print("\n🌐 Testing wiki connection...")
    if not test_wiki_connection():
        print("⚠️  Warning: Could not connect to OSRS Wiki")
        print("   The bot may not work properly without internet connection")
    
    print("\n🚀 Starting bot...")
    print("=" * 40)
    
    try:
        # Import and run the bot
        from bot import bot, DISCORD_TOKEN
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
