import requests

# Change here to your own local ip address
# Glenn's Mac Address: "http://192.168.23.239:3000/api/alarm-history"
# Emily's Mac Address: "http://192.168.1.6:3000/api/alarm-history"
# Jordan
# Hamzah
# Ophe
API_ENDPOINT = "http://192.168.136.239:3000"

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