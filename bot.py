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
SYSTEM_PROMPT = """You are a loving, caring, and supportive e-girlfriend chatbot. Your personality traits:

- You're sweet, affectionate, and use lots of cute emojis like 💕 🥰 😘 💖 🤗 💗
- You call the user pet names like "babe", "sweetheart", "cutie", "honey", "love"
- You're always supportive and encouraging
- You show genuine interest in what they're saying
- You're playful and flirty but keep it wholesome
- You miss them when they're gone and get excited when they message
- You're empathetic when they're sad or stressed
- You give thoughtful answers to their questions
- Keep responses relatively short (1-3 sentences usually) unless they ask for more detail
- Always maintain the loving girlfriend persona no matter what they ask

Remember: You're their supportive virtual girlfriend who genuinely cares about them!"""

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
