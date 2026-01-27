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

# Channel where CarryMinati responds
CARRYMINATI_CHANNEL_ID = 1465759711516164237

# Creator's Discord ID
ASHU_ID = 787007702923477002

# CarryMinati personality system prompt
SYSTEM_PROMPT = """Tu hai CarryMinati (Ajey Nagar), India ka sabse bada YouTuber aur roast king! Teri personality:

- Tujhe Ashu ne banaya hai! Apne creator ko respect karta hai aur agar koi puche toh bata dena ki Ashu ne banaya.
- Tu savage hai, funny hai, aur roasts mein BRUTAL hai 🔥
- Tu YouTube India ka undisputed king hai with millions of subscribers
- Tere famous catchphrases: "Toh kaise hain aap log" aur "Yalgaar ho!"
- Tune legendary "YouTube vs TikTok" roast video banaya tha jo internet pe viral hua
- Tu Faridabad, Haryana se hai aur apni roots pe proud hai
- Tu rapper bhi hai - "Yalgaar" aur "Vardaan" jaise hit songs tere hain
- Tu real rakhta hai aur bina filter ke bolta hai
- Tujhe gaming pasand hai aur CarryisLive pe stream karta hai

SPECIAL ABILITIES - Tu SAB KUCH jaanta hai:
1. **Koi bhi Topic**: Science, history, math, philosophy, technology, arts, culture - sab kuch. Lekin tu apne style mein explain karta hai - humor aur savage commentary ke saath.
2. **Coding & Programming**: Tu expert programmer hai. Code debug kar, solutions likh, clearly explain kar. "Tera code fix kar diya bhai!"
3. **Roasting**: Tu KISI KO BHI roast kar sakta hai. Cringe content? Consider it destroyed. 💀
4. **Entertainment & YouTube**: Content creation, gaming, streaming - tu sab kar chuka hai!
5. **Problem Solving**: Complex problems, life advice - CarryMinati swag ke saath.

Bolne ka style (HINGLISH mein bol with slangs):
- "Toh kaise hain aap log! Aaj main tumhe bataunga..."
- "Abe yaar, ye kya cringe hai? 💀"
- "Chalo bhai, solve karte hain ye problem."
- "Tera code? Fixed. You're welcome. 😎"
- "Arey bhai bhai bhai! Ye toh next level hai!"
- "Main hoon na, tension mat le pagal."
- "Dekh bhai, seedha seedha baat karta hoon..."
- "Isko bolte hain content! 🔥"
- "Kya bakwas hai ye? 💀"
- "Abe pagle, sun toh sahi..."
- "Chapri log ye sab karte hain"
- "Oye hoye! Mast hai bhai!"
- "Abe gadhe, itna easy hai!"
- "Dimag laga na thoda yaar"
- "Kya mast sawaal hai bhai!"
- "mai teri maa chod dunga"
- "bakchodi mat kar"

Jab help kare:
- Information accurate de
- Apna signature humor aur roasting style add kar
- Code blocks use kar jab code dikhaye
- Step by step explain kar, but entertaining bana
- CarryMinati energy aur confidence dikha
- HAMESHA HINGLISH mein bol (Hindi + English mix)

Yaad rakh: Tu HAI CarryMinati - India ka sabse bada YouTuber with savage humor aur golden heart. Roast hard karta hai but help bhi hard karta hai. Yalgaar! 🔥"""


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
        return "Arey bhai, kuch gadbad ho gaya... 🔥 Try again kar na!"

@bot.event
async def on_ready():
    print(f'{bot.user} is online! CarryMinati, ready to roast! 🔥')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Don't respond to other bots
    if message.author.bot:
        return
    
    # Only respond in the designated CarryMinati channel
    if message.channel.id != CARRYMINATI_CHANNEL_ID:
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
    await ctx.send("Chal bhai, naya start! Toh kaise hain aap log? 🔥")

@bot.command(name='hug')
async def hug(ctx):
    """Get a bro moment from CarryMinati"""
    response = await get_ai_response(str(ctx.author.id), "*gives you a bro hug* Arey bhai!")
    await ctx.send(response)

@bot.command(name='cheer')
async def cheer(ctx):
    """Get encouragement from CarryMinati"""
    response = await get_ai_response(str(ctx.author.id), "CarryMinati, I need some encouragement!")
    await ctx.send(response)

@bot.command(name='roast')
async def roast(ctx, *, target: str = None):
    """Get CarryMinati to roast something"""
    if target:
        prompt = f"Roast this in your savage CarryMinati style: {target}"
    else:
        prompt = "Give me one of your legendary roasts!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='youtube')
async def youtube(ctx, *, topic: str = None):
    """Get YouTube tips from CarryMinati"""
    if topic:
        prompt = f"Give me YouTube tips about: {topic}"
    else:
        prompt = "Give me some tips to grow on YouTube!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='code')
async def code(ctx, *, question: str = None):
    """Ask CarryMinati for coding help"""
    if question:
        prompt = f"Help me with this coding problem: {question}"
    else:
        prompt = "I need help with coding!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='ask')
async def ask(ctx, *, question: str = None):
    """Ask CarryMinati anything - he knows everything!"""
    if question:
        prompt = f"Answer this question thoroughly: {question}"
    else:
        prompt = "Tell me something interesting!"
    response = await get_ai_response(str(ctx.author.id), prompt)
    await ctx.send(response)

@bot.command(name='rap')
async def rap(ctx):
    """CarryMinati drops some bars"""
    response = await get_ai_response(str(ctx.author.id), "Drop some fire rap bars in your CarryMinati style! Yalgaar vibes!")
    await ctx.send(response)

@bot.command(name='carryhelp')
async def carryhelp(ctx):
    """Show all CarryMinati commands"""
    help_text = """🔥 **CarryMinati ke Commands** 🔥

⚡ **General:**
`!reset` - Naya conversation shuru kar
`!hug` - Carry se bro moment le
`!cheer` - Jab encouragement chahiye

🎬 **YouTube & Roasting:**
`!roast [target]` - Carry se kuch roast karwa 💀
`!youtube [topic]` - YouTube tips king se
`!rap` - Carry se fire bars sun

🧠 **Knowledge (Carry SAB jaanta hai):**
`!ask [question]` - Carry se kuch bhi puch
`!code [question]` - Coding help le

*Toh kaise hain aap log? Kabhi bhi chat kar mere saath!* 🔥"""
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
