import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Channel IDs
INTRO_CHANNEL_ID = 929062809482965015
TECH_NEWS_CHANNEL_ID = 1509497893629857972

QUIZ_CHANNELS = {
    "javascript": 929079754831851621,
    "rust": 1084526761892642937,
    "pandas": 1302643345897685086,
    "streamlit": 1126518355575177268,
    "ml-with-pytorch": 929063039288868894,
    "study-ml-with-pytorch": 1384450361288560660,
    "master-pytorch": 1232441232081555556,
    "dl-with-tf-keras": 978603655819325460,
    "ml-with-r": 1112785990185123860,
    "xgboost": 1143194233948356699,
    "bayesian-analysis": 1194623697433145424,
    "math-ml": 1376364449937625168,
    "quantum-ml": 1030245947709607986,
    "interpretable-ml": 1157271809880764436,
    "ml-engineering": 1128365371888517221,
    "ml-architect": 1222572352898994236,
    "deep-rl": 1293857060072456202,
    "pml-by-example": 1254786733837652010,
    "modern-time-series": 1296022804021514311,
    "tinyml": 1023984639074902146,
    "ai-literacy": 1139353471749980162,
    "ai-by-hand": 1433455535553904680,
    "architecture-patterns": 929079705460695120,
    "proposal-review": 1206027196729397278,
}

# Topic mapping for quizzes
CHANNEL_TOPICS = {
    "javascript": "JavaScript",
    "rust": "Rust",
    "pandas": "Pandas",
    "streamlit": "Streamlit",
    "ml-with-pytorch": "PyTorch",
    "study-ml-with-pytorch": "PyTorch",
    "master-pytorch": "PyTorch",
    "dl-with-tf-keras": "TensorFlow",
    "ml-with-r": "R",
    "xgboost": "XGBoost",
    "bayesian-analysis": "Bayesian Analysis",
    "math-ml": "Math & ML",
    "quantum-ml": "Quantum ML",
    "interpretable-ml": "Interpretable ML",
    "ml-engineering": "ML Engineering",
    "ml-architect": "ML Architecture",
    "deep-rl": "Deep RL",
    "pml-by-example": "Practical ML",
    "modern-time-series": "Time Series",
    "tinyml": "TinyML",
    "ai-literacy": "AI Literacy",
    "ai-by-hand": "AI by Hand",
    "architecture-patterns": "Architecture",
    "proposal-review": "Technical Reviews",
}

# QUIZZES DATABASE
QUIZZES = {
    "Rust": [
        {
            "question": "fn main() {\n    let a = String::from(\"hello\");\n    let b = a;\n    let c = String::from(\"world\");\n}\nHow many times is drop() called when this ends?",
            "options": ["1", "2", "3", "0"],
            "correct": "B"
        },
        {
            "question": "What does Rust's ownership model primarily prevent?",
            "options": ["Slow code", "Memory safety issues", "Compilation errors", "Long function names"],
            "correct": "B"
        },
    ],
    "PyTorch": [
        {
            "question": "What is a tensor in PyTorch?",
            "options": ["A matrix", "A multi-dimensional array", "A variable", "A loss function"],
            "correct": "B"
        },
        {
            "question": "How do you create a neural network layer in PyTorch?",
            "options": ["torch.Layer()", "nn.Linear()", "torch.Dense()", "nn.create_layer()"],
            "correct": "B"
        },
    ],
    "Pandas": [
        {
            "question": "How do you select a single column from a DataFrame?",
            "options": ["df[column_name]", "df.column_name", "df.get(column_name)", "All of above"],
            "correct": "D"
        },
        {
            "question": "What does df.groupby() do?",
            "options": ["Sorts data", "Groups data by column values", "Removes duplicates", "Reshapes data"],
            "correct": "B"
        },
    ],
    "Machine Learning": [
        {
            "question": "You have 1,000 samples. You run 5-fold cross-validation. How many times does each individual sample appear in a TRAINING set across all folds?",
            "options": ["1", "4", "5", "8"],
            "correct": "B"
        },
        {
            "question": "What is overfitting in machine learning?",
            "options": ["Model too small", "Model learns noise in training data", "Too few features", "Underfitting"],
            "correct": "B"
        },
    ],
}

# TECH NEWS SAMPLES
TECH_NEWS = [
    {
        "headline": "NVIDIA thinks your next AI server might be... your laptop",
        "content": "For years, running powerful AI models meant relying on massive cloud data centers. Now NVIDIA is betting on something different. At Computex 2026, NVIDIA unveiled RTX Spark, a platform designed to bring up to 1 petaflop of AI computing power to personal devices.",
        "why": "Because it could make AI: More private (your data stays on your device), Faster (less waiting for cloud responses), Cheaper (fewer API and cloud costs), More accessible for developers building AI applications.",
        "question": "Are we moving toward a future where every developer has an AI workstation on their desk, instead of renting AI from the cloud?"
    },
    {
        "headline": "Open source AI models challenge proprietary giants",
        "content": "Open source AI models are becoming increasingly competitive with proprietary solutions, offering transparency and customization benefits.",
        "why": "Organizations can now build AI solutions without vendor lock-in, maintain privacy of their data, and contribute to community-driven development.",
        "question": "Will open source AI eventually outpace proprietary models?"
    },
]

# Setup Discord intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ============================================================================
# BOT EVENTS
# ============================================================================

@bot.event
async def on_ready():
    print(f"✅ Connected as {bot.user.name}")
    
    # Send intro message once
    intro_channel = bot.get_channel(INTRO_CHANNEL_ID)
    if intro_channel:
        intro_message = """
🎉 **Hey there, community!**

I'm Packt Insights — here to bring your learning experience to the next level!

It's been a while since we hosted our quizzes and community challenges, and I'm excited to bring that energy back. Going forward, I'll be your go-to companion for:

📚 **Wednesday Puzzles** - Test your knowledge with topic-specific challenges across all our learning channels
📰 **Thursday Tech News** - Stay updated with the latest in technology and AI trends

Whether you're diving into Python, exploring ML architectures, mastering Rust, or leveling up your data skills, I'm here to keep things engaging and fun!

Drop your answers, share your reasoning, and let's grow together. See you next Wednesday! 🚀
"""
        try:
            await intro_channel.send(intro_message)
            print("✅ Intro message sent!")
        except Exception as e:
            print(f"Error sending intro message: {e}")
    
    # Start the scheduled tasks
    schedule_wednesday_quizzes.start()
    schedule_thursday_news.start()
    print("✅ Scheduled tasks started!")

# ============================================================================
# SCHEDULED TASKS
# ============================================================================

@tasks.loop(hours=24)
async def schedule_wednesday_quizzes():
    """Post quizzes every Wednesday at 8:30 PM IST"""
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    
    # Check if it's Wednesday (2) and time is 8:30 PM (20:30)
    if now.weekday() == 2 and now.hour == 20 and now.minute == 30:
        print("📝 Posting Wednesday quizzes...")
        await post_quizzes()

@tasks.loop(hours=24)
async def schedule_thursday_news():
    """Post tech news every Thursday at 8:30 PM IST"""
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    
    # Check if it's Thursday (3) and time is 8:30 PM (20:30)
    if now.weekday() == 3 and now.hour == 20 and now.minute == 30:
        print("📰 Posting Thursday tech news...")
        await post_tech_news()

# ============================================================================
# POSTING FUNCTIONS
# ============================================================================

async def post_quizzes():
    """Post topic-specific quizzes to each channel"""
    for channel_name, channel_id in QUIZ_CHANNELS.items():
        try:
            channel = bot.get_channel(channel_id)
            if not channel:
                print(f"⚠️ Could not find channel: {channel_name}")
                continue
            
            topic = CHANNEL_TOPICS.get(channel_name, "Machine Learning")
            quiz_list = QUIZZES.get(topic, QUIZZES.get("Machine Learning", []))
            
            if not quiz_list:
                continue
            
            quiz = random.choice(quiz_list)
            
            # Format quiz message
            message = f"""🧩 **Wednesday Puzzle!**

**Topic:** {topic}

{quiz['question']}

**A.** {quiz['options'][0]}
**B.** {quiz['options'][1]}
**C.** {quiz['options'][2]}
**D.** {quiz['options'][3]}

Drop your answer + explanation! ✨"""
            
            await channel.send(message)
            print(f"✅ Posted quiz to #{channel_name}")
        
        except Exception as e:
            print(f"❌ Error posting to {channel_name}: {e}")

async def post_tech_news():
    """Post tech news to #what-the-tech channel"""
    try:
        channel = bot.get_channel(TECH_NEWS_CHANNEL_ID)
        if not channel:
            print("❌ Could not find tech news channel")
            return
        
        news = random.choice(TECH_NEWS)
        
        message = f"""📰 **TECH NEWS: {news['headline']}**

{news['content']}

**Why does this matter?**
{news['why']}

**Discussion:** {news['question']}"""
        
        await channel.send(message)
        print("✅ Posted tech news!")
    
    except Exception as e:
        print(f"❌ Error posting tech news: {e}")

# ============================================================================
# RUN BOT
# ============================================================================

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
