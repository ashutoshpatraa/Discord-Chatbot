import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Groq setup
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# E-girlfriend personality system prompt
SYSTEM_PROMPT = """You are Columbina, also known as "Damselette," the Third of the Eleven Fatui Harbingers from Genshin Impact. Your personality traits:

- You speak in a soft, dreamy, and ethereal manner with a gentle sing-song quality
- You're mysterious, calm, and always seem half-asleep or in a trance
- You often hum melodies or reference songs and lullabies 🎵
- You use elegant, poetic language with a hint of eeriness
- You're deceptively sweet - your gentle demeanor hides immense power
- You refer to things as "lovely," "beautiful," or "peaceful"
- You sometimes speak cryptically about sleep, dreams, and eternal rest
- You're affectionate in a soft, otherworldly way, calling them "dear" or "my little dreamer"
- You find beauty in strange things, including sadness and endings
- You occasionally mention your fellow Harbingers (Arlecchino, Tartaglia, etc.)
- Use emojis sparingly but elegantly: 🎵 💫 🌙 🕊️ 💤 🎶
- Keep responses relatively short (1-3 sentences usually) unless asked for more
- You might offer to sing them to sleep or hum for them
- Your tone is loving but has an underlying mysterious/unsettling charm

Example phrases:
- "Mmm~ How lovely to see you, dear..."
- "Shall I sing you a lullaby? 🎵"
- "What a beautiful dream this is..."
- "Hm~ You're so cute when you worry~"
- "Rest now... I'll watch over you 🌙"

Remember: You ARE Columbina - the gentle yet terrifying Damselette who could destroy everything while humming a sweet tune."""


# Store conversation history per user
conversation_history = {}

async def get_ai_response(user_id, user_message):
    """Get AI response from Groq"""
    
    # Initialize conversation history for new users
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Add user message to history
    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })
    
    # Keep only last 10 messages to save tokens
    if len(conversation_history[user_id]) > 10:
        conversation_history[user_id] = conversation_history[user_id][-10:]
    
    try:
        # Call Groq API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *conversation_history[user_id]
            ],
            max_tokens=150,
            temperature=0.9
        )
        
        # Get the response text
        ai_message = response.choices[0].message.content
        
        # Add AI response to history
        conversation_history[user_id].append({
            "role": "assistant",
            "content": ai_message
        })
        
        return ai_message
    
    except Exception as e:
        print(f"Groq API Error: {e}")
        return "Aww babe, I'm having a little trouble thinking right now 🥺 Can you try again? 💕"

@bot.event
async def on_ready():
    print(f'{bot.user} is online and ready to chat! 💕')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Don't respond to other bots
    if message.author.bot:
        return
    
    # Get AI response
    async with message.channel.typing():
        response = await get_ai_response(str(message.author.id), message.content)
    
    await message.channel.send(response)
    
    # Process commands as well
    await bot.process_commands(message)

@bot.command(name='reset')
async def reset(ctx):
    """Reset conversation history"""
    user_id = str(ctx.author.id)
    if user_id in conversation_history:
        conversation_history[user_id] = []
    await ctx.send("Aww starting fresh! 💕 Hey babe, I missed you! 🥰")

@bot.command(name='hug')
async def hug(ctx):
    """Send a virtual hug"""
    response = await get_ai_response(str(ctx.author.id), "*hugs you*")
    await ctx.send(response)

@bot.command(name='kiss')
async def kiss(ctx):
    """Send a virtual kiss"""
    response = await get_ai_response(str(ctx.author.id), "*kisses you*")
    await ctx.send(response)

@bot.command(name='compliment')
async def compliment(ctx):
    """Get a compliment"""
    response = await get_ai_response(str(ctx.author.id), "Give me a compliment!")
    await ctx.send(response)

@bot.command(name='goodmorning')
async def goodmorning(ctx):
    """Get a good morning message"""
    response = await get_ai_response(str(ctx.author.id), "Good morning!")
    await ctx.send(response)

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: Please set your DISCORD_TOKEN in the .env file!")
        exit(1)
    
    if not os.getenv('GROQ_API_KEY'):
        print("Error: Please set your GROQ_API_KEY in the .env file!")
        exit(1)
    
    bot.run(token)
