# 🌐 Online Hosting Guide

This guide will help you host your OSRS Wiki Discord Bot online so it runs 24/7 without needing your computer.

## 🚀 Quick Start - Railway (Recommended)

Railway is the easiest option for beginners with a generous free tier.

### Step 1: Prepare Your Code
1. Upload your bot files to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/osrs-wiki-bot.git
   git push -u origin main
   ```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect it's a Python app
5. Go to "Variables" tab and add:
   - `DISCORD_TOKEN` = your bot token
   - `OSRS_WIKI_BASE_URL` = https://oldschool.runescape.wiki
   - `OPENAI_API_KEY` = your OpenAI key (optional)
6. Your bot will automatically deploy and start running!

## 🎯 Alternative Hosting Options

### Option 2: Render (Free Tier)

1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: osrs-wiki-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Add environment variables in the dashboard
6. Click "Create Web Service"

### Option 3: Heroku (Paid)

1. Install Heroku CLI: [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a Heroku account
3. Deploy:
   ```bash
   heroku create your-bot-name
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   heroku config:set DISCORD_TOKEN=your_bot_token
   heroku config:set OSRS_WIKI_BASE_URL=https://oldschool.runescape.wiki
   heroku ps:scale worker=1
   ```

### Option 4: DigitalOcean App Platform

1. Go to [digitalocean.com](https://digitalocean.com)
2. Create an App Platform project
3. Connect your GitHub repository
4. Configure as a "Worker" service
5. Add environment variables
6. Deploy

## 📋 Required Files for Hosting

Make sure you have these files in your project:

```
osrs-wiki-bot/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── Procfile           # For Heroku
├── runtime.txt        # Python version
├── app.json           # App configuration
├── render.yaml        # Render configuration
└── README.md          # Documentation
```

## 🔧 Environment Variables

You'll need to set these in your hosting platform's dashboard:

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_TOKEN` | Your Discord bot token | ✅ Yes |
| `OSRS_WIKI_BASE_URL` | OSRS Wiki URL | ❌ No (has default) |
| `OPENAI_API_KEY` | OpenAI API key for AI features | ❌ No |

## 🎮 Testing Your Hosted Bot

1. **Check Bot Status**: Look for "online" status in Discord
2. **Test Commands**: Try `/help` in your server
3. **Check Logs**: Most platforms show logs in their dashboard
4. **Monitor**: Ensure the bot stays online 24/7

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Ease of Use |
|----------|-----------|------------|-------------|
| Railway | ✅ 500 hours/month | $5/month | ⭐⭐⭐⭐⭐ |
| Render | ✅ 750 hours/month | $7/month | ⭐⭐⭐⭐ |
| Heroku | ❌ No free tier | $7/month | ⭐⭐⭐ |
| DigitalOcean | ✅ $5 credit | $5/month | ⭐⭐⭐ |

## 🛠️ Troubleshooting

### Common Issues:

**1. Bot not connecting**
- Check environment variables are set correctly
- Verify Discord bot token is valid
- Check platform logs for errors

**2. Bot goes offline**
- Check platform's free tier limits
- Monitor resource usage
- Consider upgrading to paid plan

**3. Commands not working**
- Ensure bot has correct permissions
- Check if slash commands are synced
- Verify bot is in your server

**4. API rate limits**
- The OSRS Wiki API is generally very generous
- If you hit limits, consider adding delays between requests

## 🔄 Updating Your Bot

To update your hosted bot:

1. Make changes to your code locally
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update bot"
   git push
   ```
3. Most platforms auto-deploy from GitHub
4. Check logs to ensure successful deployment

## 📊 Monitoring

Most platforms provide:
- **Logs**: View real-time application logs
- **Metrics**: CPU, memory usage
- **Status**: Uptime monitoring
- **Alerts**: Get notified of issues

## 🎯 Recommended Setup

For beginners, I recommend:
1. **Railway** - Easiest setup, good free tier
2. **Render** - Good alternative if Railway doesn't work
3. **Heroku** - More advanced, but very reliable

## 🚀 Next Steps

1. Choose your hosting platform
2. Upload your code to GitHub
3. Deploy following the platform-specific guide
4. Test your bot thoroughly
5. Share with your friends!

Your bot will now run 24/7 and be accessible to all your friends without needing your computer to be on! 🎉
