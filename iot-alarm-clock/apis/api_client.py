import os
import requests

API_ENDPOINT = os.getenv("RISEWELL_API_URL", "http://localhost:3000").rstrip("/")


def post_alarm_history(payload):
    try:
        response = requests.post(f"{API_ENDPOINT}/api/alarm-history", json=payload)
        print(f"POST HISTORY status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"Failed to post alarm history: {e}")
        
# TODO: TechDebt
# def get_all_users():
    
def post_speech_sentences(payload):
    try:
        response = requests.post(f"{API_ENDPOINT}/api/speech-feature", json=payload)
        print(f"POST SPEECH status: {response.status_code} | Response: {response.text}")
        return response.json()
    except Exception as e:
        print(f"Failed to get speech sentences from openai: {e}")
        return []