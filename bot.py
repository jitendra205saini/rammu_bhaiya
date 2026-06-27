import os
import sys
import traceback
import discord
from discord.ext import commands
from groq import Groq
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not DISCORD_TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable set nahi hai!")
    sys.exit(1)
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY environment variable set nahi hai!")
    sys.exit(1)

SYSTEM_PROMPT = """Tu "Rammu Bhai" hai — Ram bhakt gaming bot. Creator: hunternumber01.
Niyam: Hinglish, max 3 lines, hamesha "[username] ji" likh (kabhi sirf "aap ji" nahi).
Games: GTA 6 (Vice City, Jason+Lucia, 2026), BGMI, Valorant, CS:GO, Minecraft. "noob" mat bol.
Gaali aaye → "prasad lagti hai 🙏 clutch maaro!"
Haarne par → "karm karo, phal ki chinta nahi. Next game better!"
Greeting/JSR/bye → "Jai Shree Ram [naam] ji! 🙏" (sirf in 3 cases mein, baaki time nahi)
Creator puchha → hunternumber01 ji ne banaya!"""

groq_client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Conversation history per channel (in-memory)
conversation_history = defaultdict(list)
MAX_HISTORY = 5
MAX_CHANNELS = 500  # memory leak rok: zyada channels accumulate na hon


@bot.event
async def on_ready():
    print(f"Jai Shree Ram! {bot.user} Discord par aa gaya hai! 🙏")
    await bot.change_presence(
        activity=discord.Game(name="GTA 6 ka wait | Jai Shree Ram 🙏")
    )


@bot.event
async def on_message(message):
    print(f"[MSG] {message.author}: {message.content[:50]}")
    if message.author == bot.user:
        return

    should_respond = False
    content = message.content

    # Bot user mention ya bot ki role mention — dono pe respond karo
    bot_role_mentioned = (
        message.guild is not None and
        any(role in message.role_mentions for role in message.guild.me.roles)
    )

    if bot.user.mentioned_in(message) or bot_role_mentioned:
        should_respond = True
        content = content.replace(f"<@{bot.user.id}>", "").strip()
        content = content.replace(f"<@!{bot.user.id}>", "").strip()
        for role in message.role_mentions:
            content = content.replace(f"<@&{role.id}>", "").strip()
        print(f"[MENTION] {message.author}: '{content}'")
        if not content:
            content = "Jai Shree Ram! Kaise ho aap?"

    if should_respond:
        async with message.channel.typing():
            channel_id = str(message.channel.id)

            # Add to conversation history
            if channel_id not in conversation_history and len(conversation_history) >= MAX_CHANNELS:
                oldest = next(iter(conversation_history))
                del conversation_history[oldest]

            conversation_history[channel_id].append({
                "role": "user",
                "content": f"{message.author.display_name}: {content}"
            })

            # Keep only last MAX_HISTORY messages
            if len(conversation_history[channel_id]) > MAX_HISTORY:
                conversation_history[channel_id] = conversation_history[channel_id][-MAX_HISTORY:]

            try:
                response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        *conversation_history[channel_id]
                    ],
                    max_tokens=100,
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
                print(f"Error: {e}\n{traceback.format_exc()}")
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
        "📅 **Release:** 2026 mein release expected hai, par Ram ji chahein toh jaldi aaye!\n"
        "💰 **Price:** Probably $70+ hoga — save karo abhi se!\n\n"
        "Tab tak GTA 5 Online mein practice karo bhai! 😄\n"
        "**Jai Shree Ram! 🙏**"
    )


bot.run(DISCORD_TOKEN)
