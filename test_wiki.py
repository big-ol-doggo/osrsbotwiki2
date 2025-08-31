#!/usr/bin/env python3
"""
Test script for OSRS Wiki MediaWiki API integration
This script tests the basic functionality of the wiki searcher
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

class OSRSWikiTester:
    def __init__(self, base_url: str = 'https://oldschool.runescape.wiki'):
        self.base_url = base_url
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def test_search(self, query: str):
        """Test the search functionality"""
        print(f"\n🔍 Testing search for: '{query}'")
        
        session = await self.get_session()
        search_url = f"{self.base_url}/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': 3,
            'srnamespace': 0
        }
        
        try:
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('query', {}).get('search', [])
                    
                    if results:
                        print(f"✅ Found {len(results)} results:")
                        for i, result in enumerate(results, 1):
                            print(f"  {i}. {result['title']}")
                            snippet = re.sub(r'<[^>]+>', '', result['snippet'])
                            print(f"     {snippet[:100]}...")
                    else:
                        print("❌ No results found")
                else:
                    print(f"❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_page_content(self, page_title: str):
        """Test getting page content"""
        print(f"\n📖 Testing page content for: '{page_title}'")
        
        session = await self.get_session()
        content_url = f"{self.base_url}/api.php"
        params = {
            'action': 'parse',
            'format': 'json',
            'page': page_title,
            'prop': 'text|sections',
            'section': 0
        }
        
        try:
            async with session.get(content_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'parse' in data:
                        content = data['parse']
                        print(f"✅ Successfully retrieved content")
                        print(f"   Title: {content['title']}")
                        print(f"   Sections: {len(content.get('sections', []))}")
                        
                        # Extract some text
                        soup = BeautifulSoup(content['text']['*'], 'html.parser')
                        for element in soup(['script', 'style', 'table', 'img']):
                            element.decompose()
                        
                        text = soup.get_text()
                        lines = (line.strip() for line in text.splitlines())
                        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        text = ' '.join(chunk for chunk in chunks if chunk)
                        
                        print(f"   Preview: {text[:200]}...")
                    else:
                        print("❌ No parse data found")
                else:
                    print(f"❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_random_page(self):
        """Test getting a random page"""
        print(f"\n🎲 Testing random page")
        
        session = await self.get_session()
        random_url = f"{self.base_url}/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'random',
            'rnnamespace': 0,
            'rnlimit': 1
        }
        
        try:
            async with session.get(random_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    random_pages = data.get('query', {}).get('random', [])
                    
                    if random_pages:
                        page = random_pages[0]
                        print(f"✅ Random page: {page['title']}")
                        print(f"   ID: {page['id']}")
                    else:
                        print("❌ No random page found")
                else:
                    print(f"❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_recent_changes(self):
        """Test getting recent changes"""
        print(f"\n📝 Testing recent changes")
        
        session = await self.get_session()
        changes_url = f"{self.base_url}/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'recentchanges',
            'rcnamespace': 0,
            'rclimit': 3,
            'rcprop': 'title|timestamp|user|comment'
        }
        
        try:
            async with session.get(changes_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    changes = data.get('query', {}).get('recentchanges', [])
                    
                    if changes:
                        print(f"✅ Found {len(changes)} recent changes:")
                        for i, change in enumerate(changes, 1):
                            print(f"  {i}. {change['title']}")
                            print(f"     Edited by: {change.get('user', 'Unknown')}")
                            print(f"     Comment: {change.get('comment', 'No comment')[:50]}...")
                    else:
                        print("❌ No recent changes found")
                else:
                    print(f"❌ HTTP Error: {response.status}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()

async def main():
    """Run all tests"""
    print("🧪 OSRS Wiki MediaWiki API Test")
    print("=" * 40)
    
    tester = OSRSWikiTester()
    
    # Test search functionality
    await tester.test_search("dragon scimitar")
    await tester.test_search("fishing")
    await tester.test_search("quest guide")
    
    # Test page content
    await tester.test_page_content("Dragon scimitar")
    await tester.test_page_content("Fishing")
    
    # Test random page
    await tester.test_random_page()
    
    # Test recent changes
    await tester.test_recent_changes()
    
    # Close session
    await tester.close()
    
    print("\n" + "=" * 40)
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
