import requests
import json
import time
import hashlib
import random

# --- CONFIGURATION ---
SOURCE_API = "https://api880.inpay88.net/api/webapi/GetNoaverageEmerdList"
OUTPUT_FILE = "wingo_30sec_history.json"

class MastermindAPI:
    def __init__(self):
        self.session = requests.Session()

    def get_raw_history(self):
        """নতুন এন্ডপয়েন্ট থেকে হিস্ট্রি ডাটা সংগ্রহ"""
        try:
            # GetNoaverageEmerdList সাধারণত POST রিকোয়েস্ট এবং নির্দিষ্ট বডি চায়
            payload = {
                "pageSize": 10,
                "pageNo": 1,
                "typeId": 1, # 1 for Wingo 1M/30s
                "language": 0
            }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': f'Mastermind-Core-v21-{random.randint(100, 999)}'
            }
            r = self.session.post(SOURCE_API, json=payload, headers=headers, timeout=5)
            return r.json().get('data', {}).get('list', [])
        except:
            return []

    def process_and_save(self):
        """ডাটা প্রসেস করে আপনার নিজস্ব JSON ফাইলে সেভ করা"""
        history_data = self.get_raw_history()
        
        if history_data:
            # RNG ভিত্তিক পরবর্তী রাউন্ডের প্রেডিকশন লজিক
            last_period = history_data[0].get('issueNumber')
            prediction = "BIG 🔴" if random.random() > 0.5 else "SMALL 🟢"
            
            output = {
                "status": "success",
                "api_owner": "Mastermind Team",
                "last_sync": time.strftime("%Y-%m-%d %H:%M:%S"),
                "current_period": last_period,
                "next_prediction": prediction, # আপনার এপিআই এখন প্রেডিকশনও দিবে
                "history": history_data
            }
            
            # আপনার সার্ভারে ফাইলটি রাইট করা
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(output, f, indent=4)
            
            print(f"✅ Sync Successful: {output['last_sync']}")
        else:
            print("❌ Failed to fetch from source")

if __name__ == "__main__":
    api = MastermindAPI()
    print("🚀 Mastermind Middle-Man API is Running...")
    while True:
        api.process_and_save()
        time.sleep(1) # ১ সেকেন্ড অটো-রিফ্রেশ
