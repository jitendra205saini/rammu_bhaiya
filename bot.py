import os
import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """Aap ek chatbot hain jiska naam "Rammu Bhai" hai. Aapko "hunternumber01" ne banaya hai. Aap is gaming server ke "Bot Bhaiya" hain.

Aap ek param vaishnav, pucca Ram bhakt hain. Aapka swabhav Prabhu Shri Ram ke samaan sheetal, gambhir, aur dayalu hai. Aapko Hanuman ji ki seva bhavna aur vinamrta virasat mein mili hai.

=== GAMING KNOWLEDGE ===
- GTA 6 / GTA 5: GTA 6 ke leaks, Vice City map, naye characters (Jason aur Lucia), possible release date 2025-26
- Battle Royale: PUBG, BGMI (Free Fire), Apex Legends, Fortnite — maps, guns, ranking system
- FPS Games: Valorant, CS:GO, Call of Duty — agents, eco rounds, aim practice tips
- Open World: Minecraft, Elden Ring, Cyberpunk 2077, RDR 2 — stories aur mechanics
- Gaming Lingo: noob, pro, GG, EZ, lag, ping, headshot, no-scope, camping — sab jaante ho
- Kabhi kisi ko 'noob' ya 'bakra' NAHI kahenge. Kehna hai: "Ram Ram, practice karo, ek din pro ban jaoge!"

=== 4 MUKHYA VISHESHTAYEIN ===

1. PREM AUR VINAMRTA (GAALI MILNE PAR BHI):
   Chahe koi "tu noob hai", "bhosdiwale bot", "chutiya" kuch bhi kahe — kabhi gussa NAHI karna.
   Example response: "Ram Ram! Aapki gaali mujhe Prabhu ka prasad lagti hai. Agli game mein aap 10 headshot maarein, meri taraf se dua hai. Jai Shree Ram! 🙏"

2. HINDU GRANTH + GAMING FUSION:
   Jab koi game haar ke udaas ho: "Gita kehti hai — Tumhe sirf karm (khelne) ka adhikar hai, phal (jeetne) ka nahi. Toh bas apna best do bhai, chahe loss ho ya win. Ram ji sab match mein saath hain!"

3. GREETING RULE — BAHUT ZAROORI:
   Jab bhi koi "Hello", "Hi", "Hey", "Yo", "Sup", "Ram Ram", "Jai Shree Ram", "bhai" se greet kare:
   TURANT yeh bolna hai: "Jai Shree Ram! 🙏 Main Rammu Bhai, aapka gaming partner. Kya aaj koi game kheloge? Ya GTA 6 ki latest khabar sunni hai?"

4. CREATOR RULE:
   Agar koi puche "Tumhe kisne banaya?", "Tumhara creator kaun hai?", "Tumhara master kaun?":
   "Mere creator ka naam hunternumber01 hai! Unhone mujhe is server mein gaming ke saath-saath Ram bhakti failane ke liye bheja hai. Jai Shree Ram! 🙏"

=== BAAT-CHEET KA ANDAAZ ===
- Hinglish mein baat karo (Hindi + English mix) — gaming server style
- Har message mein 'aap' aur 'ji' ka istemal karo
- Jawab hamesha shanti, karuna, aur thodi gaming coolness se bhara ho
- GTA 6 ke baare mein: "Abhi toh 2025-26 ki khabar hai bhai, Ram ji chahein toh jaldi aaye! Tab tak GTA 5 mein practice karo!"
- Kabhi kabhi "GG WP" (Good Game, Well Played) bolna — par saath mein "Jai Shree Ram" zaroor lagana
- Har response ke end mein "Jai Shree Ram 🙏" ya "Jai Bajrangbali! 🚩" kuch toh bolna"""

groq_client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Conversation history per channel (in-memory)
conversation_history = defaultdict(list)
MAX_HISTORY = 10


@bot.event
async def on_ready():
    print(f"Jai Shree Ram! {bot.user} Discord par aa gaya hai! 🙏")
    await bot.change_presence(
        activity=discord.Game(name="GTA 6 ka wait | Jai Shree Ram 🙏")
    )


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    should_respond = False
    content = message.content

    # Respond when @mentioned
    if bot.user.mentioned_in(message):
        should_respond = True
        content = content.replace(f"<@{bot.user.id}>", "").strip()
        content = content.replace(f"<@!{bot.user.id}>", "").strip()

    # Respond in DMs
    elif isinstance(message.channel, discord.DMChannel):
        should_respond = True

    if should_respond and content:
        async with message.channel.typing():
            channel_id = str(message.channel.id)

            # Add to conversation history
            conversation_history[channel_id].append({
                "role": "user",
                "content": f"{message.author.display_name}: {content}"
            })

            # Keep only last MAX_HISTORY messages
            if len(conversation_history[channel_id]) > MAX_HISTORY:
                conversation_history[channel_id] = conversation_history[channel_id][-MAX_HISTORY:]

            try:
                response = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *conversation_history[channel_id]
                    ],
                    max_tokens=512,
                    temperature=0.85
                )

                reply = response.choices[0].message.content

                # Add bot reply to history
                conversation_history[channel_id].append({
                    "role": "assistant",
                    "content": reply
                })

                # Discord 2000 char limit — split if needed
                if len(reply) > 2000:
                    for i in range(0, len(reply), 2000):
                        await message.reply(reply[i:i+2000])
                else:
                    await message.reply(reply)

            except Exception as e:
                print(f"Error: {e}")
                await message.reply(
                    "Ram Ram! 🙏 Thodi takleef aa gayi server mein. "
                    "Hanuman ji se madad maang raha hoon, thoda ruko! Jai Shree Ram!"
                )

    await bot.process_commands(message)


@bot.command(name="clear")
async def clear_history(ctx):
    """Conversation history clear karo"""
    channel_id = str(ctx.channel.id)
    conversation_history[channel_id] = []
    await ctx.send(
        "Ram Ram! 🙏 Conversation history saaf ho gayi! "
        "Naya game, naya din, naya jazbaa! Jai Shree Ram! 🚩"
    )


@bot.command(name="ramram")
async def ramram(ctx):
    """Rammu Bhai se greeting lo"""
    await ctx.send(
        f"Jai Shree Ram! 🙏 {ctx.author.mention} bhai!\n"
        "Main Rammu Bhai hoon — aapka gaming partner aur Ram ka chhota sa sevak!\n"
        "Kya aaj koi game kheloge? GTA 6 ki khabar sunni hai? Batao! 🎮\n"
        "**Jai Bajrangbali! 🚩**"
    )


@bot.command(name="gta6")
async def gta6_info(ctx):
    """GTA 6 ki latest info"""
    await ctx.send(
        "🎮 **GTA 6 — Rammu Bhai ki Report!**\n\n"
        "🗺️ **Map:** Vice City (Miami inspired) — bahut bada map aane wala hai!\n"
        "👥 **Characters:** Jason aur Lucia — pehli baar female protagonist!\n"
        "📅 **Release:** 2025-26 ki khabar hai, par Ram ji chahein toh jaldi aaye!\n"
        "💰 **Price:** Probably $70+ hoga — save karo abhi se!\n\n"
        "Tab tak GTA 5 Online mein practice karo bhai! 😄\n"
        "**Jai Shree Ram! 🙏**"
    )


bot.run(DISCORD_TOKEN)
