# Discord E-Girlfriend Chatbot 💕

A sweet AI-powered Discord bot that acts as a loving e-girlfriend, powered by Groq AI!

## Features

✨ **AI-Powered Conversations** - Natural responses using Groq AI  
💬 **Conversation Memory** - Remembers context within your chat  
🥰 **Loving Personality** - Sweet, supportive, and affectionate  
⚡ **Fast Responses** - Powered by Groq's lightning-fast inference  

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

### 6. Run the Bot

```bash
python bot.py
```

## Features

The bot responds to:
- **Greetings:** hi, hello, hey
- **Love:** i love you, ily
- **Check-ins:** how are you, wyd
- **Compliments:** beautiful, cute, amazing
- **Goodnight:** goodnight, gn
- **Sad messages:** sad, upset, stressed
- **Questions:** Any message with ?

## Commands

- `!hug` - Get a virtual hug
- `!kiss` - Get a virtual kiss
- `!compliment` - Get a compliment
- `!goodmorning` - Get a good morning message

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

## Enjoy! 💖
