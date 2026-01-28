# Reze Discord Bot ☕💣

A sweet and charming Discord bot embodying Reze from Chainsaw Man - a kind café worker with a deadly secret! Powered by Groq AI.

## Features

✨ **AI-Powered Conversations** - Warm responses using Groq AI  
💬 **Conversation Memory** - Remembers context within your chat  
☕ **Café Worker Charm** - Coffee recommendations and cozy café vibes  
💣 **Explosive Secret** - Hints at Reze's dangerous Bomb Devil side  
⚡ **Fast Responses** - Powered by Groq's lightning-fast inference  
🐱 **Reze Personality** - Sweet, mysterious, kind, and secretly dangerous  

## Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under the bot's username, click "Reset Token" to get your bot token
5. **Important:** Enable these Privileged Gateway Intents:
   - MESSAGE CONTENT INTENT ✅

### 2. Get a Groq API Key

1. Go to [Groq Console](https://console.groq.com/keys)
2. Create an account or sign in
3. Generate a new API key

### 3. Invite the Bot to Your Server

1. Go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`
3. Select permissions: `Send Messages`, `Read Message History`
4. Copy the generated URL and open it in your browser to invite the bot

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and add your tokens:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Channel ID

Edit `bot.py` and set your desired channel ID:
```python
REZE_CHANNEL_ID = 1466111829188022571  # Replace with your channel ID
```

### 7. Run the Bot

```bash
python bot.py
```

## Commands

### � General Commands
- `!reset` - Start a fresh conversation
- `!hug` - Get a warm embrace from Reze
- `!cheer` - Receive encouragement and kind words

### ☕ Café Life
- `!coffee [topic]` - Talk about coffee or discuss a topic over a cup
- `!dream [topic]` - Discuss dreams and peaceful countryside life
- `!explode` - See Reze's explosive, dangerous side 💣

### 🧠 Knowledge
- `!ask [question]` - Ask Reze anything
- `!code [question]` - Get coding help

### 📚 Help
- `!help` - View all available commands

## Reze Personality

Reze will:
- Be warm, caring, and genuinely interested in conversation
- Share her passion for coffee and café life ☕
- Dream about peaceful countryside living 🌾
- Drop mysterious hints about her secret Bomb Devil powers 💣
- Balance sweetness with subtle danger
- Show both her gentle café worker side and her explosive capabilities

**Example of her style:**
> "Would you like some coffee? ☕"
> 
> "I've always dreamed of living a quiet life in the countryside..."
>
> "I'm good at... explosive entrances. Hehe~ 💣"

## 🚀 Free 24/7 Hosting

### Option 1: Railway (Recommended)
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect your GitHub repo
4. Add environment variables (`DISCORD_TOKEN`, `GROQ_API_KEY`)
5. Deploy!

### Option 2: Render
1. Go to [render.com](https://render.com)
2. Create a "Background Worker"
3. Connect GitHub repo
4. Set environment variables
5. Set start command: `python bot.py`

### Option 3: Replit
1. Go to [replit.com](https://replit.com)
2. Import your GitHub repo
3. Add Secrets (environment variables)
4. Use Replit Deployments

## License

MIT License - Feel free to use and modify!

## Enjoy! ☕💣

*"Come visit my café anytime. Let's have a nice chat over coffee!"* - Reze

*"There are no accidents... only destiny."* - Master Oogway
