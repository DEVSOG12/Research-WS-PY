import requests as requests


def send_simple_message(data):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc90a44973a78431e8faa47bd2b632cb2.mailgun.org/messages",
        auth=("api", "key-ded180a76d4b1efa5e19a1f50730b74b"),
        data={"from": "Research Bot <postmaster@sandboxc90a44973a78431e8faa47bd2b632cb2.mailgun.org>",
              "to": "Oreofe Solarin <khakis_forearm.0u@icloud.com>",
              "subject": "Run Complete",
              "html": str(data)})


print(send_simple_message("Hello").text)