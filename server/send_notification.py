def send_notification(notification: str) -> None:
    match notification:
        case "server_up":
            ...
        case "server_down":
            ...
        case "vote_cast":
            ...
        case "suggestion_made":
            ...


import requests

url = "https://ntfy.sh/botc-vote-BVegUd2mWC"
#TODO upload some images to botc / botc-vote repo as pngs
requests.post(
    url,
    data="A23456789B23456789C23456789D23456789E23456789F23456789",
    headers={
        "Title": "Title Here..."
        # "Icon": "https://release.botc.app/resources/characters/generic/fabled.webp"
    }
)
