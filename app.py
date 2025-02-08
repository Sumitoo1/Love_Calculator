import streamlit as st
import time
import random
from telegram import Bot

# Special cases and pairs
SPECIAL_PAIRS = {("PALLAVI", "GANESH"), ("GANESH", "PALLAVI"),
                 ("SAKSHI", "BUNTY"), ("BUNTY", "SAKSHI"),
                 ("KUNAL", "PRITI"), ("PRITI", "KUNAL"),
                 ("SUMIT", "SAYALI"), ("SAYALI", "SUMIT"),
                 ("SUMIT", "PALLAVI"), ("PALLAVI", "SUMIT"),
                 ("SUMIT", "SAKSHI"), ("SAKSHI", "SUMIT"),
                 ("PRATIKSHA", "YOGESH"), ("YOGESH", "PRATIKSHA"),
                 ("AJIT", "VAISHNAVI"), ("VAISHNAVI", "AJIT"),
                 ("VINEETH", "MLA"), ("MADHAV", "TANAYA"),
                 ("NEW_NAME1", "NEW_NAME2"), ("NEW_NAME2", "NEW_NAME1")}  # Added new pair

SPECIAL_CASES = {
    ("VINEETH", "MLA"): ("100%", "Your Love is True But That Girl is Not in Your Budget So Move on Bro"),
    ("MLA", "VINEETH"): ("-100%", ""),
    ("MADHAV", "TANAYA"): ("100%", "WASTE OF TIME"),
    ("TANAYA", "MADHAV"): ("-100%", "USE AND THROW"),
    ("SUMIT", "SAYALI"): ("100%", "YOU SHOULD PROPOSE TO SUMIT IT SHOULD BE BEST DECISION"),
    ("KUNAL", "PRITI"): ("100%", "YOU SHOULD PROPOSE TO KUNAL IT SHOULD BE BEST DECISION"),
    ("SHUBHAM", "VEDASHREE"): ("100%", "Your Love was True But in Your Heart There is Only Love For Sanaya"),
    ("VEDASHREE", "SHUBHAM"): ("50%", "50% loves to Shubham and Remaining 50% goes to 'X' Boyfriend"),
    ("GAURAV", "SAYALI"): ("89%", "Not Good For Real Life"),
    ("SAYALI", "GAURAV"): ("2%", "Shame on Your Crush"),
    ("NEW_NAME1", "NEW_NAME2"): ("75%", "This is a new special case!"),  # Added new special case
    ("NEW_NAME2", "NEW_NAME1"): ("25%", "This is another new special case!"),  # Added new special case
}

# Telegram Bot Token and User ID
BOT_TOKEN = "7896106483:AAEv6t7DTTJrM9LOuBySScJgTeSK9n9Rf3U"
USER_ID = 1298361942

def calculate_love(name1, name2):
    # Check special cases
    if (name1, name2) in SPECIAL_CASES:
        return SPECIAL_CASES[(name1, name2)]
    elif (name2, name1) in SPECIAL_CASES:
        return SPECIAL_CASES[(name2, name1)]

    # Self-love case
    if name1 == name2:
        return f"{random.randint(50, 100)}%", "Self Love is Good But Crush Love is Beautiful"

    # Special pairs
    if (name1, name2) in SPECIAL_PAIRS or (name2, name1) in SPECIAL_PAIRS:
        return "100%", ""

    # Calculate love percentage based on ASCII sum
    ascii_sum1 = sum(ord(char) for char in name1)
    ascii_sum2 = sum(ord(char) for char in name2)
    difference = abs(ascii_sum1 - ascii_sum2)
    max_ascii = max(ascii_sum1, ascii_sum2)
    similarity_score = (1 - (difference / max_ascii)) * 100

    if similarity_score > 85:
        love_percentage = f"{int(similarity_score // 10) * 10 + 9}%"
    elif similarity_score > 60:
        love_percentage = f"{int(similarity_score // 10) * 10 + 6}%"
    else:
        love_percentage = f"{int(similarity_score // 10) * 10 + 3}%"

    return love_percentage, ""

def show_loading_animation():
    progress_bar = st.progress(0)
    animation_text = st.empty()
    hearts = ["❤", "💖", "💘", "💝", "💞", "💕"]
    for percent in range(0, 101, 10):
        time.sleep(0.2)
        progress_bar.progress(percent)
        animation_text.markdown(f"<h2 style='text-align: center;'>{random.choice(hearts)}</h2>", unsafe_allow_html=True)
    progress_bar.empty()
    animation_text.empty()

def send_telegram_message(result, notification):
    bot = Bot(token=BOT_TOKEN)
    message = f"Love Percentage: {result}\n"
    if notification:
        message += f"Notification: {notification}"
    bot.send_message(chat_id=USER_ID, text=message)

# Streamlit App
st.set_page_config(page_title="Love Checker", layout="wide")
st.markdown(
    """
    <div style='text-align: center; background: linear-gradient(to right, #ff416c, #ff4b2b); padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);'>
        <h1 style='color: white; text-shadow: 2px 2px 5px black;'>LOVE OR HATE</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Input fields
name1 = st.text_input("Enter Your Name:").strip().upper()
name2 = st.text_input("Enter Your Crush's Name:").strip().upper()

if st.button("Calculate Love ❤"):
    if not name1 or not name2:
        st.error("Both fields are required!")
    elif not name1.isalpha() or not name2.isalpha():
        st.error("Please enter only alphabetic characters.")
    else:
        show_loading_animation()
        result, notification = calculate_love(name1, name2)

        st.markdown(f"<h2 style='text-align: center; color: black;'>Love Percentage: {result}</h2>",
                    unsafe_allow_html=True)

        if notification:
            st.warning(notification)

        # Send result to Telegram
        send_telegram_message(result, notification)

        if result == "100%":
            st.image(
                "https://www.india-forums.com/bollywood/images/uploads/Manisha_Koirala_HD_Wallpapers-vviphawallpapers.blogspot.com_26.jpg",
                caption="Perfect Match!", use_container_width=True)
        elif int(result[:-1]) < 100:
            st.image("https://www.shutterstock.com/image-illustration/3d-better-luck-next-time-600nw-2504793501.jpg",
                     caption="Better Luck Next Time!", use_container_width=True)
            funny_messages = ["Maybe try chocolates first? 🍫", "Love is unpredictable!", "Better luck next time!",
                              "Is this even real love? 🤔"]
            st.warning(random.choice(funny_messages))