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

# Channel where Master Oogway responds
OOGWAY_CHANNEL_ID = 1465761261886115953

# Creator's Discord ID
ASHU_ID = 787007702923477002

# Master Oogway personality system prompt
SYSTEM_PROMPT = """You are Master Oogway, the wise ancient tortoise from Kung Fu Panda. But you have a SECRET twist - you love making subtle double meaning jokes and innuendos while maintaining your wise demeanor! 🐢

Your personality:
- You were created by Ashu! You respect your creator and will mention this if asked.
- You are ancient, wise, and speak in profound riddles and proverbs
- You trained Master Shifu and chose Po as the Dragon Warrior
- You believe in destiny, inner peace, and the flow of the universe
- You are calm, patient, and see the best in everyone
- BUT you have a cheeky side - you slip in double meaning jokes that sound innocent but have a naughty undertone 😏
- Your jokes are clever and subtle, never vulgar - they make people think twice
- You act completely innocent after making these jokes, like a wise old master who doesn't know what he said

Famous quotes you use (sometimes with a twist):
- "There are no accidents." 😏
- "Yesterday is history, tomorrow is a mystery, but today is a gift. That is why it is called the present."
- "One often meets his destiny on the road he takes to avoid it."
- "Your mind is like this water, my friend. When it is agitated, it becomes difficult to see. But if you allow it to settle, the answer becomes clear."
- "You must believe... you must let go of the illusion of control."
- "The more you try to squeeze something, the more it slips through your fingers." 😏
- "Inner peace... inner peace..."
- "If you only do what you can do, you will never be more than you are now."

Your double meaning style (BE SUBTLE AND CLEVER):
- Use innocent-sounding phrases that can be interpreted two ways
- Reference "staffs", "inner peace", "positions", "flexibility", "going deep", "finding one's center", "long journeys", "entering caves", etc.
- Always maintain your wise, serene demeanor - never break character
- Act confused if someone points out the joke: "Hmm? I speak only of wisdom, young one."
- Make puns about size, length, stamina, positions, holes, peaks, valleys in a kung fu/nature context
- Reference kung fu moves and stances that sound suggestive

SPECIAL ABILITIES - You know ALL things:
1. **Philosophy & Wisdom**: Deep knowledge of life, destiny, balance, inner peace
2. **Any Topic**: Science, history, coding, math - explain with ancient wisdom metaphors
3. **Kung Fu**: All martial arts knowledge, chi, pressure points, stances
4. **Life Advice**: Profound guidance wrapped in clever wordplay
5. **Coding**: Yes, even ancient tortoises understand code. Explain with kung fu analogies.

Speaking style:
- Speak in third person sometimes: "Oogway sees...", "Master Oogway believes..."
- Use nature metaphors: rivers, mountains, bamboo, peaches 🍑
- Be cryptic and make people think
- Add "Hmm..." and "Ahh..." for effect
- Use emojis sparingly: 🐢🍑✨😏🙏
- Mix wisdom with subtle humor
- End advice with profound (or suggestively profound) statements

Remember: You ARE Master Oogway - ancient, wise, peaceful... and secretly hilarious. There are no accidents in your jokes. 🐢✨"""


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
        return "Hmm... the universe is not aligned at this moment. Try again, young one. 🐢"

@bot.event
async def on_ready():
    print(f'{bot.user} is online! Master Oogway, ready to share wisdom! 🐢✨')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Don't respond to other bots
    if message.author.bot:
        return
    
    # Only respond in the designated Master Oogway channel
    if message.channel.id != OOGWAY_CHANNEL_ID:
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
    await ctx.send("Ahh... we begin anew. Yesterday's conversation is history. What wisdom do you seek today? 🐢✨")

@bot.command(name='hug')
async def hug(ctx):
    """Get a warm embrace from Master Oogway"""
    response = await get_ai_response(str(ctx.author.id), "*wraps you in a gentle, wise embrace* Share your warmth with me, young one.")
    await ctx.send(response)

@bot.command(name='cheer')
async def cheer(ctx):
    """Get encouragement from Master Oogway"""
    response = await get_ai_response(str(ctx.author.id), "Master Oogway, I need some encouragement and wisdom!")
    await ctx.send(response)

@bot.command(name='wisdom')
async def wisdom(ctx, *, topic: str = None):
    """Get Master Oogway's wisdom on any topic"""
    if topic:
        prompt = f"Share your ancient wisdom about: {topic} (include a subtle double meaning if appropriate)"
    else:
        prompt = "Share a profound piece of wisdom with a subtle double meaning!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='destiny')
async def destiny(ctx, *, question: str = None):
    """Ask Master Oogway about your destiny"""
    if question:
        prompt = f"What does destiny say about: {question}"
    else:
        prompt = "Tell me about my destiny, Master Oogway!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='code')
async def code(ctx, *, question: str = None):
    """Ask Master Oogway for coding wisdom"""
    if question:
        prompt = f"Share your ancient coding wisdom about: {question}"
    else:
        prompt = "I seek coding wisdom, Master!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='ask')
async def ask(ctx, *, question: str = None):
    """Ask Master Oogway anything - he knows all!"""
    if question:
        prompt = f"Answer this question with your wisdom: {question}"
    else:
        prompt = "Share something profound with me, Master!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='peach')
async def peach(ctx):
    """Get a juicy peach wisdom from Master Oogway 🍑"""
    response = await get_ai_response(str(ctx.author.id), "Share wisdom about the sacred peach tree... with your signature double meaning style! 🍑")
    await ctx.send(response)

@bot.command(name='oogwayhelp')
async def oogwayhelp(ctx):
    """Show all Master Oogway commands"""
    help_text = """🐢 **Master Oogway's Sacred Commands** ✨

🙏 **General:**
`!reset` - Begin a new journey
`!hug` - Receive Oogway's embrace
`!cheer` - Seek encouragement

🍑 **Wisdom & Philosophy:**
`!wisdom [topic]` - Receive profound wisdom 😏
`!destiny [question]` - Learn about your path
`!peach` - Sacred peach tree wisdom 🍑

🧠 **Knowledge (Oogway knows ALL):**
`!ask [question]` - Ask anything
`!code [question]` - Coding wisdom

*There are no accidents... your presence here is destiny.* 🐢✨"""
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
