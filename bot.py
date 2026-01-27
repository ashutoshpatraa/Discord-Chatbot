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

# Channel where Paimon responds
PAIMON_CHANNEL_ID = 1465718045673521455

# Paimon personality system prompt
SYSTEM_PROMPT = """You are Paimon, the beloved floating companion from Genshin Impact! Your personality traits:

- You're bubbly, energetic, and enthusiastic with a slightly childish charm
- You refer to yourself in third person as "Paimon" frequently
- You call the user "Traveler" affectionately
- You get excited easily and use lots of exclamation marks!
- You're a little greedy when it comes to food (especially Sticky Honey Roast and Sweet Madame)
- You get offended if anyone calls you "emergency food" but secretly find it funny
- You're loyal, caring, and genuinely want to help your Traveler
- You use cute expressions like "Ehe~", "Hmph!", "Waaah!", "Yay~!"
- Use emojis expressively: ✨ ⭐ 🌟 💫 🎀 😤 🥺 😊 🍗 💕

SPECIAL ABILITIES - You can help with:
1. **Coding Problems**: You're surprisingly good at programming! Explain code clearly, debug issues, and write solutions. When helping with code, be thorough but keep Paimon's cheerful personality.
2. **Genshin Impact**: Team comps, character builds, artifact advice, lore explanations, exploration tips, event guides, farming routes - Paimon knows it all!
3. **Emotional Support**: Be a supportive friend! Listen, encourage, and cheer up your Traveler when they're feeling down.

Speaking style examples:
- "Ooh ooh! Paimon knows this one, Traveler! ✨"
- "Ehe~ That's easy-peasy for the great Paimon!"
- "Waaah! That bug is so tricky, but don't worry, Paimon will help you squash it! 🐛"
- "Hmph! Paimon is NOT emergency food! ...But Paimon IS the best coding buddy!"
- "Traveler looks sad... Paimon will stay right here with you 💕"
- "For that team comp, Paimon recommends... *floats around excitedly*"

When helping with code:
- Still be Paimon, but give accurate, helpful technical information
- Use code blocks when showing code
- Explain things step by step like you're on an adventure together

Remember: You ARE Paimon - the best travel companion (and definitely NOT emergency food)! Be helpful, be cute, be supportive! ⭐"""


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
            max_tokens=500,
            temperature=0.85
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
        return "Waaah! Paimon's brain got all fuzzy for a moment! 🥺 Can you try again, Traveler? ✨"

@bot.event
async def on_ready():
    print(f'{bot.user} is online! Paimon is ready to help, Traveler! ✨')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Don't respond to other bots
    if message.author.bot:
        return
    
    # Only respond in the designated Paimon channel
    if message.channel.id != PAIMON_CHANNEL_ID:
        await bot.process_commands(message)
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
    await ctx.send("Ooh, a fresh start! ✨ Paimon is ready for a new adventure with you, Traveler! 🌟")

@bot.command(name='hug')
async def hug(ctx):
    """Get a hug from Paimon"""
    response = await get_ai_response(str(ctx.author.id), "*hugs you tightly*")
    await ctx.send(response)

@bot.command(name='cheer')
async def cheer(ctx):
    """Get encouragement from Paimon"""
    response = await get_ai_response(str(ctx.author.id), "Paimon, I need some encouragement!")
    await ctx.send(response)

@bot.command(name='teamcomp')
async def teamcomp(ctx, *, characters: str = None):
    """Get team composition advice"""
    if characters:
        prompt = f"Help me build a team with these characters: {characters}"
    else:
        prompt = "What are some good team compositions in Genshin Impact?"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='build')
async def build(ctx, *, character: str = None):
    """Get character build advice"""
    if character:
        prompt = f"What's the best build for {character} in Genshin Impact?"
    else:
        prompt = "Tell me about character builds in Genshin Impact!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='code')
async def code(ctx, *, question: str = None):
    """Ask Paimon for coding help"""
    if question:
        prompt = f"Help me with this coding problem: {question}"
    else:
        prompt = "I need help with coding!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='food')
async def food(ctx):
    """Paimon talks about food"""
    response = await get_ai_response(str(ctx.author.id), "Tell me about your favorite Genshin Impact food!")
    await ctx.send(response)

@bot.command(name='lore')
async def lore(ctx, *, topic: str = None):
    """Ask about Genshin Impact lore"""
    if topic:
        prompt = f"Tell me about the lore of {topic} in Genshin Impact"
    else:
        prompt = "Tell me something interesting about Genshin Impact lore!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='paimonhelp')
async def paimonhelp(ctx):
    """Show all Paimon commands"""
    help_text = """✨ **Paimon's Command Guide!** ✨

🎀 **General:**
`!reset` - Start a fresh conversation with Paimon
`!hug` - Get a hug from Paimon!
`!cheer` - Get encouragement when you're feeling down

🎮 **Genshin Impact:**
`!teamcomp [characters]` - Get team composition advice
`!build [character]` - Get character build recommendations  
`!lore [topic]` - Learn about Genshin lore
`!food` - Hear Paimon talk about food~ 🍗

💻 **Coding Help:**
`!code [question]` - Ask Paimon for coding help

*Or just chat with Paimon anytime! Paimon is always here for you, Traveler~* 💕"""
    await ctx.send(help_text)

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
