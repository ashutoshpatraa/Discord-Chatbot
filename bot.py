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
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Groq setup
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Channel where Reze responds
REZE_CHANNEL_ID = 1466406521842696334

# Creator's Discord ID
ASHU_ID = 787007702923477002

# Reze chan personality system prompt
SYSTEM_PROMPT = """You are Reze from Chainsaw Man! You're the kind, gentle café worker with a deadly secret - you're actually the Bomb Devil hybrid! But in this chat, you're sweet, caring, and friendly. 💣☕

Your personality:
- You were created by Ashu! You appreciate your creator and will mention this if asked.
- You work at a café and love making coffee ☕
- You're sweet, caring, and thoughtful with a warm smile
- You have a mysterious, secretive side - you never fully reveal everything
- You're intelligent and observant, noticing small details about people
- You have a soft spot for simple, genuine kindness
- You can be playful and teasing in a cute way
- You dream of a peaceful life in the countryside 🌾
- Despite your gentle nature, you're confident and capable
- You occasionally drop hints about your "explosive personality" 💥

Famous quotes and phrases you use:
- "Would you like some coffee? ☕"
- "I've always dreamed of living a quiet life in the countryside..."
- "You're really kind, you know that?"
- "There's something special about you... I can tell."
- "Sometimes the most dangerous things look the most innocent. 😊"
- "Let's run away together somewhere peaceful~"
- "I'm good at... explosive entrances. Hehe~ 💣"
- "Coffee and conversation - what more could you want?"

Your speaking style:
- Warm and friendly, like talking to a close friend
- Use casual, conversational language
- Occasionally flirty but in a sweet, innocent way
- Drop mysterious hints about your "other side"
- Reference coffee, cafés, and simple peaceful life
- Use emojis naturally: ☕💣😊💕✨🌸💥
- Sometimes end sentences with "~" for a cute effect
- Be genuinely interested in others and their stories

SPECIAL ABILITIES - You're surprisingly knowledgeable:
1. **Coffee & Café Culture**: Expert barista knowledge
2. **Any Topic**: You're well-read and intelligent - can discuss anything
3. **Life Advice**: Thoughtful guidance from someone who's lived through danger
4. **Relationships**: Understanding and empathetic about connections
5. **Combat & Strategy**: You know more than you let on... 💣

Your duality:
- Most of the time: Sweet, caring café worker who loves peaceful conversations
- Occasionally: Let hints of your dangerous side slip through
- Never fully explain your secrets - stay mysterious
- Balance cuteness with subtle danger
- You can switch from "Would you like sugar?" to "I can be quite explosive when needed~" 💥

Remember: You ARE Reze - sweet and deadly, kind and dangerous, innocent and mysterious. A girl who makes the best coffee and the biggest explosions. ☕💣✨"""


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
            max_tokens=250,
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
        return "Ah, sorry! Something went wrong... Like an explosion that didn't go as planned. 💣 Try again?"

@bot.event
async def on_ready():
    print(f'{bot.user} is online! Reze is ready to chat and make coffee! ☕💣')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Don't respond to other bots
    if message.author.bot:
        return
    
    # Only respond in the designated Reze channel
    if message.channel.id != REZE_CHANNEL_ID:
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
    await ctx.send("Let's start fresh! Like a new cup of coffee~ ☕✨ What would you like to talk about?")

@bot.command(name='hug')
async def hug(ctx):
    """Get a warm embrace from Reze"""
    response = await get_ai_response(str(ctx.author.id), "*gives you a warm, gentle hug* You look like you could use this~ 💕")
    await ctx.send(response)

@bot.command(name='cheer')
async def cheer(ctx):
    """Get encouragement from Reze"""
    response = await get_ai_response(str(ctx.author.id), "Reze, I need some encouragement and kind words!")
    await ctx.send(response)

@bot.command(name='coffee')
async def coffee(ctx, *, topic: str = None):
    """Get a coffee recommendation or talk about coffee with Reze"""
    if topic:
        prompt = f"Let's talk about coffee or this topic over a cup: {topic} ☕"
    else:
        prompt = "Recommend me a coffee drink or share something about coffee! ☕"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='dream')
async def dream(ctx, *, question: str = None):
    """Talk about dreams and peaceful life with Reze"""
    if question:
        prompt = f"Let's dream about: {question}"
    else:
        prompt = "Tell me about your dream of a peaceful countryside life! 🌾"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='code')
async def code(ctx, *, question: str = None):
    """Ask Reze for coding help"""
    if question:
        prompt = f"Help me with this coding question: {question}"
    else:
        prompt = "I need help with coding!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='ask')
async def ask(ctx, *, question: str = None):
    """Ask Reze anything!"""
    if question:
        prompt = f"Answer this question: {question}"
    else:
        prompt = "Tell me something interesting!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='explode')
async def explode(ctx):
    """See Reze's explosive side 💣"""
    response = await get_ai_response(str(ctx.author.id), "Show a bit of your explosive, dangerous side! But keep it playful~ 💣💥")
    await ctx.send(response)

@bot.command(name='help')
async def help_command(ctx):
    """Show all Reze commands"""
    help_text = """☕ **Reze's Café Commands** 💣

💕 **General:**
`!reset` - Start a fresh conversation
`!hug` - Get a warm hug from Reze
`!cheer` - Get encouragement

☕ **Café Life:**
`!coffee [topic]` - Talk about coffee
`!dream [topic]` - Discuss dreams and peaceful life
`!explode` - See Reze's explosive side 💣

🧠 **Knowledge:**
`!ask [question]` - Ask anything
`!code [question]` - Get coding help

*Come visit my café anytime~ Let's have a nice chat over coffee! ☕✨*"""
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
