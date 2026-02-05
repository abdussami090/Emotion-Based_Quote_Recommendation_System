import random
import json
from collections import Counter
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# ----------------------------
# Quotes stored directly in Python dictionary
# ----------------------------
quotes = {
    "happy": [
        "Smile, it confuses people.",
        "Happiness is a choice, not a result.",
        "Keep smiling, because life is a beautiful thing.",
        "Be happy for this moment. This moment is your life."
    ],
    "sad": [
        "Every storm runs out of rain.",
        "It's okay to not be okay.",
        "Tough times never last, but tough people do.",
        "Sadness is but a wall between two gardens."
    ],
    "angry": [
        "For every minute you are angry, you lose 60 seconds of happiness.",
        "Stay calm; anger is your enemy.",
        "Anger doesn’t solve anything, it builds nothing, but it can destroy everything."
    ],
    "love": [
        "To love and be loved is everything.",
        "Where there is love, there is life.",
        "Love all, trust a few, do wrong to none."
    ],
    "motivation": [
        "Push yourself, because no one else is going to do it for you.",
        "Don’t watch the clock; do what it does — keep going.",
        "Believe you can and you’re halfway there.",
        "The harder you work for something, the greater you’ll feel when you achieve it.",
        "Success doesn’t just find you. You have to go out and get it."
    ],
    "neutral": [
        "Be yourself; everyone else is already taken.",
        "Keep learning, keep growing.",
        "Believe in yourself and you will be unstoppable."
    ]
}

# ----------------------------
# Detect emotion from user input
# ----------------------------
def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in ["happy", "joy", "calm", "excited", "great", "good", "awesome", "fun", "enjoy"]):
        return "happy"
    elif any(word in text for word in ["sad", "unhappy", "depressed", "cry", "bad", "upset", "hurt"]):
        return "sad"
    elif any(word in text for word in ["angry", "mad", "furious", "irritated", "annoyed"]):
        return "angry"
    elif any(word in text for word in ["love", "crush", "affection", "romantic"]):
        return "love"
    elif any(word in text for word in ["motivated", "strong", "motivation", "success", "goal", "dream", "energetic", "work", "inspire"]):
        return "motivation"
    else:
        return "neutral"

# ----------------------------
# Recommend a random quote based on detected emotion
# ----------------------------
def recommend_quote(emotion):
    if emotion in quotes:
        return random.choice(quotes[emotion])
    else:
        return "Sorry, I don't have quotes for that emotion yet."

# ----------------------------
# Save emotion data to JSON file
# ----------------------------
def log_emotion(emotion, filename="emotion_log.json"):
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        pass  # file not found, will create new

    data.append({
        "emotion": emotion,
        "timestamp": datetime.now().isoformat()
    })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ----------------------------
# Weekly Report: Show only top emotions + combined quote + bar chart
# ----------------------------
def generate_weekly_report(filename="emotion_log.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            emotion_data = json.load(f)
    except FileNotFoundError:
        print("No emotion data available yet.")
        return

    if not emotion_data:
        print("No emotions logged yet.")
        return

    # Filter last 7 days
    one_week_ago = datetime.now() - timedelta(days=7)
    weekly_emotions = [
        entry["emotion"] for entry in emotion_data
        if datetime.fromisoformat(entry["timestamp"]) >= one_week_ago
    ]

    if not weekly_emotions:
        print("No emotions recorded in the last 7 days.")
        return

    # Count emotions and find the highest frequency
    emotion_counts = Counter(weekly_emotions)
    highest_count = max(emotion_counts.values())

    # Get all top emotions (in case of tie)
    top_emotions = [emo for emo, count in emotion_counts.items() if count == highest_count]

    print("\n🌟 Weekly Emotion Tracker Report (Last 7 Days) 🌟")
    print("-------------------------------------------------")
    print(f"🏆 Most Frequent Emotion(s): {', '.join(e.capitalize() for e in top_emotions)}")
    print(f"🧮 Frequency: {highest_count} time(s)")
    print("-------------------------------------------------")

    # Combined quote for top emotions
    combined_quote = " ".join([random.choice(quotes[emo]) for emo in top_emotions])
    print("🌈 Combined Quote Based on Your Top Emotion(s):")
    print(f"💬 “{combined_quote}”")
    print("-------------------------------------------------\n")

    # ----------------------------
    # Bar Chart Visualization
    # ----------------------------
    emotions = list(emotion_counts.keys())
    counts = list(emotion_counts.values())

    plt.figure(figsize=(8, 5))
    plt.bar(emotions, counts, color=['#ffcc00', '#ff6666', '#66ccff', '#99ff99', '#ff99ff', '#cccccc'])
    plt.title("Weekly Emotion Frequency")
    plt.xlabel("Emotions")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save chart automatically
    chart_filename = f"weekly_emotion_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(chart_filename, bbox_inches='tight')
    print(f"📊 Bar chart saved as: {chart_filename}\n")

    plt.show()

# ----------------------------
# Main Menu
# ----------------------------
def main():
    print("🌟 Emotion-Based Quote Recommendation System 🌟")
    print("------------------------------------------------")

    while True:
        print("\nMenu:")
        print("1️⃣  Get a quote based on your mood")
        print("2️⃣  View weekly emotion report")
        print("3️⃣  Exit")

        choice = input("👉 Enter your choice (1-3): ")

        if choice == "1":
            user_input = input("\nHow are you feeling today?\n> ")
            emotion = detect_emotion(user_input)
            quote = recommend_quote(emotion)
            log_emotion(emotion)

            print("\n------------------------------------------------")
            print(f"🧠 Detected Emotion: {emotion.capitalize()}")
            print(f"💬 Recommended Quote: “{quote}”")
            print("------------------------------------------------")

        elif choice == "2":
            generate_weekly_report()

        elif choice == "3":
            print("\nThank you for using the Emotion-Based Quote Recommendation System! 💖")
            break

        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")

# ----------------------------
# Run the program
# ----------------------------
if __name__ == "__main__":
    main()
