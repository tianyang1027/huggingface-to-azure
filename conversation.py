import requests
import json
import os
import soundfile as sf
import numpy as np
import io
from datetime import datetime
 
# Azure OpenAI resource information
endpoint = "https://v-mandyyu-9920-resource.cognitiveservices.azure.com"
api_key = "7eafiEoYNCJKrK1z86H4vd9h2Sx8rP8a1Wm1lJSQDi1uFzIsXImFJQQJ99BIACHYHv6XJ3w3AAAAACOGoLbG"
deployment = "gpt-4o-mini-tts"
api_version = "2025-03-01-preview"
 
url = f"{endpoint}/openai/deployments/{deployment}/audio/speech?api-version={api_version}"
 
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
 
# Example of a multi-person conversation
conversation = [
    {"role": "Narrator", "text": "It's a cozy Saturday afternoon. Alice, Carter, and Frank are sitting at a café table, planning their big Greek adventure. Laptops open, coffee cups half-full, and Alice already has a notebook covered with doodles of olive branches and little temples."},
    {"role": "Alice", "text": "Okay, first things first—Athens! The cradle of democracy, birthplace of philosophy, land of gyros and feta cheese. We have to start there."},
    {"role": "Carter", "text": "You just sound like a travel brochure. Did you secretly get hired by the Greek Ministry of Tourism?"},
    {"role": "Alice", "text": "If they paid me in baklava, I'd take the job! Anyway, we'll start with the Acropolis. Can you imagine walking up where Socrates and Plato once debated?"},
    {"role": "Carter", "text": "Yeah, I imagine Socrates would look at my sneakers and go, “Really? That's your toga alternative?”"},
    {"role": "Frank", "text": "Hey, at least you're wearing shoes. Half the tourists I see in Athens try to climb marble stairs in flip-flops. It's like an Olympic sport called Sprained Ankle 101."},
    {"role": "Alice", "text": "True. But besides the Acropolis, we should check out the Parthenon. It was dedicated to Athena, the goddess of wisdom. The columns are still standing after 2,500 years!"},
    {"role": "Carter", "text": "Yeah, meanwhile my IKEA bookshelf didn't last two months."},
    {"role": "Frank", "text": "That's because you didn't sacrifice a goat to Athena before assembling it."},
    {"role": "Alice", "text": "Stop! Okay, but food—Carter, you'll love souvlaki. Tender grilled meat on skewers. And saganaki, which is basically cheese set on fire at your table."},
    {"role": "Carter", "text": "Flaming cheese? Okay, Greece officially understands me."},
    {"role": "Frank", "text": "Next stop: Delphi. The ancient Greeks thought it was the center of the world, right?"},
    {"role": "Alice", "text": "Yes! The Oracle of Apollo. People traveled from all over just to hear cryptic advice. Like, “You'll win if you don't lose.” Super helpful."},
    {"role": "Carter", "text": "So basically the same as a modern motivational poster."},
    {"role": "Alice", "text": "Exactly. But the ruins are incredible—the Temple of Apollo, the theater with mountain views. You feel like the gods are still listening."},
    {"role": "Frank", "text": "And don't forget the food. The mountain villages nearby? Honey, nuts, homemade yogurt. You eat something simple like bread with olive oil, and it tastes like heaven."},
    {"role": "Carter", "text": "If the oracle told me, “Your destiny is carbs,” I'd be like, “Finally, some accurate prophecy.”"},
    {"role": "Alice", "text": "Meteora is going to blow your mind. Monasteries perched on top of giant rock pillars—like castles in the clouds."},
    {"role": "Carter", "text": "Okay, but… how do monks even get groceries up there?"},
    {"role": "Frank", "text": "They used to haul supplies with ropes and baskets. Imagine being the delivery guy: 'Here's your pizza, please don't drop me.'"},
    {"role": "Alice", "text": "Those monasteries are UNESCO sites now. We'll climb up and see Byzantine frescoes that survived centuries."},
    {"role": "Carter", "text": "I'm more motivated by the 'climb down and eat moussaka' part."},
    {"role": "Frank", "text": "Good choice. Moussaka—layers of eggplant, meat, and béchamel sauce. It's basically Greek lasagna, but better."},
    {"role": "Frank", "text": "Ah, Thessaloniki. My favorite food city. Street markets full of bougatsa—sweet custard pie wrapped in flaky pastry. You eat one, then accidentally eat three more."},
    {"role": "Alice", "text": "And history too! Roman forums, Byzantine churches, Ottoman baths. Every empire left its mark."},
    {"role": "Carter", "text": "So it's like the European version of my old hard drive—cluttered with everything."},
    {"role": "Frank", "text": "Exactly. But tastier. And at night, the waterfront fills with music. You'll hear rebetiko songs—kind of like Greek blues."},
    {"role": "Alice", "text": "Romantic! We'll sit by the sea, eating fresh seafood, maybe grilled octopus."},
    {"role": "Carter", "text": "As long as it doesn't still look like it could hug me back."},
    {"role": "Alice", "text": "Now the iconic one: Santorini. White houses, blue domes, sunsets that make Instagram crash."},
    {"role": "Carter", "text": "I'm already seeing the photos: '#nofilter #livingmybestlife.'"},
    {"role": "Frank", "text": "It's true. Oia at sunset is one of those bucket-list moments. But warning: crowds. Everyone's elbowing each other for that one picture."},
    {"role": "Alice", "text": "Then we'll sneak off and find a taverna. Tomato fritters, fava bean dip, local white wine. Simple, fresh, perfect."},
    {"role": "Carter", "text": "Finally, a meal that doesn't start with 'fried cheese explosion.'"},
    {"role": "Frank", "text": "Don't worry, we'll still get fried cheese tomorrow."},
    {"role": "Frank", "text": "Crete is a whole trip by itself, but we'll squeeze in highlights. Knossos Palace—the legendary labyrinth of King Minos. Some say the Minotaur was kept there."},
    {"role": "Carter", "text": "Great, so basically 'Airbnb but with a monster roommate.'"},
    {"role": "Alice", "text": "The palace is fascinating—Minoan frescoes of dolphins and dancers. They were advanced 3,500 years ago!"},
    {"role": "Frank", "text": "And Crete's food… oh boy. Dakos—barley rusk topped with tomato and feta. Fresh fish straight from the sea. And raki, the local spirit."},
    {"role": "Carter", "text": "What's the alcohol percentage?"},
    {"role": "Frank", "text": "High enough that after two shots, you'll start believing you are the Minotaur."},
    {"role": "Alice", "text": "Final day—Mykonos. Beaches, windmills, nightlife."},
    {"role": "Carter", "text": "So this is the 'party like Dionysus' portion of the trip?"},
    {"role": "Frank", "text": "Exactly. We'll stroll through Little Venice, where houses sit right on the water. Then by night, the clubs go wild."},
    {"role": "Alice", "text": "But I want to try kopanisti cheese. Spicy, tangy, totally different from feta."},
    {"role": "Carter", "text": "I'm noticing a trend: every stop involves cheese."},
    {"role": "Frank", "text": "Hey, if Greece invented democracy and theater, the least they could do is also perfect dairy."},
    {"role": "Alice", "text": "So seven days: Athens, Delphi, Meteora, Thessaloniki, Santorini, Crete, Mykonos. History, food, sunsets, parties. Perfect balance."},
    {"role": "Carter", "text": "And enough cheese to keep me happy for the rest of my life."},
    {"role": "Frank", "text": "That's the spirit. Greece: come for the ruins, stay for the raki."},
    {"role": "Narrator", "text": "And so, their Greek adventure is set. Laughter, myths, and plenty of flaming cheese await."},
]
 
# Different voices for each role
voices = {
    "Alice": {"voice": "shimmer", "style": "excited"},
    "Carter": {"voice": "coral", "style": "humorous"},
    "Frank": {"voice": "jazz", "style": "enthusiastic"},
    "Narrator": {"voice": "alloy", "style": "calm"}  
}
 
voiceses = [
    {"role": "Narrator", "voice": "alloy", "style": "warm", "emphasis": "neutral"},  # 1
    {"role": "Alice", "voice": "shimmer", "style": "excited", "emphasis": "strong"},   # 2
    {"role": "Carter", "voice": "coral", "style": "playful", "emphasis": "light"},    # 3
    {"role": "Alice", "voice": "shimmer", "style": "enthusiastic", "emphasis": "strong"}, # 4
    {"role": "Carter", "voice": "coral", "style": "sarcastic", "emphasis": "light"},  # 5
    {"role": "Frank", "voice": "jazz", "style": "humorous", "emphasis": "medium"},  # 6
    {"role": "Alice", "voice": "shimmer", "style": "curious", "emphasis": "strong"},   # 7
    {"role": "Carter", "voice": "coral", "style": "dry", "emphasis": "light"},        # 8
    {"role": "Frank", "voice": "jazz", "style": "playful", "emphasis": "medium"},   # 9
    {"role": "Alice", "voice": "shimmer", "style": "delighted", "emphasis": "strong"}, # 10
    {"role": "Carter", "voice": "coral", "style": "amused", "emphasis": "medium"},    # 11
    {"role": "Frank", "voice": "jazz", "style": "curious", "emphasis": "medium"},   # 12
    {"role": "Alice", "voice": "shimmer", "style": "excited", "emphasis": "strong"},   # 13
    {"role": "Carter", "voice": "coral", "style": "teasing", "emphasis": "light"},    # 14
    {"role": "Alice", "voice": "shimmer", "style": "reverent", "emphasis": "medium"},  # 15
    {"role": "Frank", "voice": "jazz", "style": "warm", "emphasis": "medium"},      # 16
    {"role": "Carter", "voice": "coral", "style": "joking", "emphasis": "light"},     # 17
    {"role": "Alice", "voice": "shimmer", "style": "awe", "emphasis": "strong"},       # 18
    {"role": "Carter", "voice": "coral", "style": "curious", "emphasis": "light"},    # 19
    {"role": "Frank", "voice": "jazz", "style": "humorous", "emphasis": "medium"},  # 20
    {"role": "Alice", "voice": "shimmer", "style": "informative", "emphasis": "medium"}, # 21
    {"role": "Carter", "voice": "coral", "style": "casual", "emphasis": "light"},     # 22
    {"role": "Frank", "voice": "jazz", "style": "enthusiastic", "emphasis": "medium"}, # 23
    {"role": "Frank", "voice": "jazz", "style": "nostalgic", "emphasis": "medium"}, # 24
    {"role": "Alice", "voice": "shimmer", "style": "passionate", "emphasis": "strong"}, # 25
    {"role": "Carter", "voice": "coral", "style": "witty", "emphasis": "light"},      # 26
    {"role": "Frank", "voice": "jazz", "style": "warm", "emphasis": "medium"},      # 27
    {"role": "Alice", "voice": "shimmer", "style": "romantic", "emphasis": "strong"},  # 28
    {"role": "Carter", "voice": "coral", "style": "skeptical", "emphasis": "light"},  # 29
    {"role": "Alice", "voice": "shimmer", "style": "excited", "emphasis": "strong"},   # 30
    {"role": "Carter", "voice": "coral", "style": "mocking", "emphasis": "light"},    # 31
    {"role": "Frank", "voice": "jazz", "style": "amused", "emphasis": "medium"},    # 32
    {"role": "Alice", "voice": "shimmer", "style": "cozy", "emphasis": "medium"},      # 33
    {"role": "Carter", "voice": "coral", "style": "teasing", "emphasis": "light"},    # 34
    {"role": "Frank", "voice": "jazz", "style": "playful", "emphasis": "medium"},   # 35
    {"role": "Frank", "voice": "jazz", "style": "mysterious", "emphasis": "medium"}, # 36
    {"role": "Carter", "voice": "coral", "style": "sarcastic", "emphasis": "light"},  # 37
    {"role": "Alice", "voice": "shimmer", "style": "awe", "emphasis": "strong"},       # 38
    {"role": "Frank", "voice": "jazz", "style": "hearty", "emphasis": "medium"},    # 39
    {"role": "Carter", "voice": "coral", "style": "curious", "emphasis": "light"},    # 40
    {"role": "Frank", "voice": "jazz", "style": "joking", "emphasis": "medium"},    # 41
    {"role": "Alice", "voice": "shimmer", "style": "energetic", "emphasis": "strong"}, # 42
    {"role": "Carter", "voice": "coral", "style": "playful", "emphasis": "light"},    # 43
    {"role": "Frank", "voice": "jazz", "style": "amused", "emphasis": "medium"},    # 44
    {"role": "Alice", "voice": "shimmer", "style": "confident", "emphasis": "medium"}, # 45
    {"role": "Carter", "voice": "coral", "style": "satisfied", "emphasis": "medium"}, # 46
    {"role": "Frank", "voice": "jazz", "style": "cheerful", "emphasis": "medium"},  # 47
    {"role": "Alice", "voice": "shimmer", "style": "summarizing", "emphasis": "medium"}, # 49
    {"role": "Carter", "voice": "coral", "style": "content", "emphasis": "medium"},   # 50
    {"role": "Frank", "voice": "jazz", "style": "celebratory", "emphasis": "medium"}, # 51
    {"role": "Narrator", "voice": "alloy", "style": "warm", "emphasis": "neutral"}  # 48
]
 
# Generate audio
audio_data_list = []
sample_rate = None
 
indexConversion = 0
for msg in conversation:
    role_info = voiceses[indexConversion]
    data = {
        "model": deployment,
        "input": msg["text"],
        "voice": role_info["voice"],
        "style": role_info["style"],
        "role": role_info["role"],
        "emphasis": role_info["emphasis"]        
    }
 
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        audio_bytes = io.BytesIO(response.content)
        data_array, sr = sf.read(audio_bytes)
        if sample_rate is None:
            sample_rate = sr
        elif sr != sample_rate:
            raise ValueError("All WAV files must have the same sample rate")
        audio_data_list.append(data_array)
        print(f"{indexConversion} Audio generated for {msg['role']} with style {role_info['style']}")
    else:
        print(f"{indexConversion} Request failed ({msg['role']}):", response.status_code, response.text)
       
    indexConversion += 1
 
# Concatenate all audio
if audio_data_list:
    combined_audio = np.concatenate(audio_data_list, axis=0)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S") 
    output_file = os.path.join(os.getcwd(), f"greek_adventure_full_emotional_{timestamp}.wav")
    sf.write(output_file, combined_audio, sample_rate)
    print(f"All conversations have been combined into {output_file}")
else:
    print("No audio files were generated")