import requests

# Change here to your own local ip address
# Glenn's Mac Address: "http://192.168.23.239:3000/api/alarm-history"
# Emily's Mac Address: "http://192.168.1.6:3000/api/alarm-history"
# Jordan
# Hamzah
# Ophe
ALARM_HISTORY_ENDPOINT = "http://192.168.1.6:3000/api/alarm-history"

def post_alarm_history(payload):
    try:
        response = requests.post(ALARM_HISTORY_ENDPOINT, json=payload)
        print(f"POST status: {response.status_code} | Response: {response.text}")
    except Exception as e:
        print(f"Failed to post alarm history: {e}")