import requests

def send_notification(m):
    url = "https://us-central1-scarlet-labs.cloudfunctions.net/send_tg_message"
    params = {"token": "1371710582:AAEgLpGJK803GmN2T1RA1-kiM8yK11LJKEc",
              "chat_id": "-330984210",
              "message": m}
    r = requests.post(url, json=params)
