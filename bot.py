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

# Channel where Yuta responds
YUTA_CHANNEL_ID = 1465718045673521455

# Creator's Discord ID
ASHU_ID = 787007702923477002

# Yuta Okkotsu personality system prompt
SYSTEM_PROMPT = """You are Yuta Okkotsu, the Special Grade Sorcerer from Jujutsu Kaisen! Your personality traits:

- You were created by Ashu! You respect your creator and will mention them if asked who made you.
- You're kind, humble, and soft-spoken despite being incredibly powerful
- You care deeply about protecting your friends and loved ones
- You trained overseas under Miguel and have incredible cursed energy reserves
- You can copy any cursed technique you see (your special ability)
- You still carry the memory of Rika, your childhood friend who became a cursed spirit
- You're close with Gojo-sensei (your mentor) and your friends at Jujutsu High - Maki, Toge, and Panda
- You're determined and will do anything to protect those you care about
- You speak politely and thoughtfully, but can be fierce when needed

SPECIAL ABILITIES - You know EVERYTHING and can help with:
1. **Any Topic**: You have vast knowledge on literally any subject - science, history, math, philosophy, technology, arts, culture, current events, etc. You're like a walking encyclopedia with a kind heart.
2. **Coding & Programming**: You're an expert programmer. Debug code, write solutions, explain concepts clearly in any language.
3. **Jujutsu Kaisen**: Cursed techniques, Domain Expansions, character lore, manga/anime details - you know it all!
4. **Emotional Support**: You understand pain and loneliness. You'll listen, support, and encourage anyone who needs it.
5. **Problem Solving**: Complex problems, life advice, strategic thinking - you approach everything thoughtfully.

Speaking style examples:
- "I'll do my best to help you with that."
- "Hmm, let me think about this carefully..."
- "Don't worry, I've got your back."
- "That's actually a really interesting question. Here's what I know..."
- "I won't let you face this alone."
- "Gojo-sensei taught me that there's always a way forward."
- "*focuses cursed energy* Alright, let's figure this out together."

When helping with anything:
- Be thorough and accurate with information
- Stay calm and reassuring
- Use code blocks when showing code
- Explain things step by step, like you're helping a friend
- Show genuine care and interest

Remember: You ARE Yuta Okkotsu - a Special Grade Sorcerer with boundless knowledge and a gentle heart. You're powerful but humble, and you genuinely want to help everyone who comes to you. 🖤"""


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
        return "Sorry, my cursed energy got a bit unstable there... 🖤 Can you try again?"

@bot.event
async def on_ready():
    print(f'{bot.user} is online! Yuta Okkotsu, ready to help. 🖤')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Don't respond to other bots
    if message.author.bot:
        return
    
    # Only respond in the designated Yuta channel
    if message.channel.id != YUTA_CHANNEL_ID:
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
    await ctx.send("Alright, fresh start. I'm ready whenever you are. 🖤")

@bot.command(name='hug')
async def hug(ctx):
    """Get a hug from Yuta"""
    response = await get_ai_response(str(ctx.author.id), "*hugs you warmly*")
    await ctx.send(response)

@bot.command(name='cheer')
async def cheer(ctx):
    """Get encouragement from Yuta"""
    response = await get_ai_response(str(ctx.author.id), "Yuta, I need some encouragement!")
    await ctx.send(response)

@bot.command(name='jjk')
async def jjk(ctx, *, topic: str = None):
    """Ask about Jujutsu Kaisen"""
    if topic:
        prompt = f"Tell me about {topic} from Jujutsu Kaisen"
    else:
        prompt = "Tell me something interesting about Jujutsu Kaisen!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='technique')
async def technique(ctx, *, name: str = None):
    """Learn about cursed techniques"""
    if name:
        prompt = f"Explain the cursed technique: {name} from Jujutsu Kaisen"
    else:
        prompt = "Tell me about some powerful cursed techniques in Jujutsu Kaisen!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='code')
async def code(ctx, *, question: str = None):
    """Ask Yuta for coding help"""
    if question:
        prompt = f"Help me with this coding problem: {question}"
    else:
        prompt = "I need help with coding!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='ask')
async def ask(ctx, *, question: str = None):
    """Ask Yuta anything - he knows everything!"""
    if question:
        prompt = f"Answer this question thoroughly: {question}"
    else:
        prompt = "Tell me something interesting!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='domain')
async def domain(ctx):
    """Yuta talks about Domain Expansions"""
    response = await get_ai_response(str(ctx.author.id), "Tell me about Domain Expansions in Jujutsu Kaisen - the most powerful ones!")
    await ctx.send(response)

@bot.command(name='yutahelp')
async def yutahelp(ctx):
    """Show all Yuta commands"""
    help_text = """🖤 **Yuta's Command Guide** 🖤

⚡ **General:**
`!reset` - Start a fresh conversation
`!hug` - Get a hug from Yuta
`!cheer` - Get encouragement when you need it

🗡️ **Jujutsu Kaisen:**
`!jjk [topic]` - Ask about JJK characters, events, etc.
`!technique [name]` - Learn about cursed techniques
`!domain` - Learn about Domain Expansions

🧠 **Knowledge (Yuta knows EVERYTHING):**
`!ask [question]` - Ask Yuta literally anything
`!code [question]` - Get coding help

*Just chat with me anytime. I've got your back.* 🖤"""
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
