import requests

url = "https://ntfy.sh/botc-vote-BVegUd2mWC"

def send_notification(notification_id: str, name: str="") -> None:
    data = "err"
    headers = {"Title": "invalid notification id supplied"}
    match notification_id:
        case "server_up":
            data = "Server Started Successfully"
            headers = {
                "Icon": "https://github.com/Nathan3-14/botc/blob/main/icons/other/fabled.png?raw=true",
                "Priority": "low",
                "Click": "https://nathan3-14.github.io/botc/vote/"
            }
        case "server_down":
            data = "Server Shut Down Successfully"
            headers = {
                "Icon": "https://github.com/Nathan3-14/botc/blob/main/icons/other/fabled.png?raw=true",
                "Priority": "low"
            }
        case "vote_cast":
            data = f"{name} has voted"
            headers = {
                "Icon": "https://github.com/Nathan3-14/botc/blob/main/icons/other/legion_good.png?raw=true",
                "Click": "https://nathan3-14.github.io/botc/vote/results",
                "Priority": "low"
            }
        case "suggestion_made":
            data = f"{name} has been suggested"
            headers = {
                "Icon": "https://github.com/Nathan3-14/botc/blob/main/icons/other/loric.png?raw=true",
                "Click": "https://nathan3-14.github.io/botc/vote/suggest"
            }
    requests.post(url, data=data, headers=headers)

if __name__ == "__main__":
    send_notification("server_down")
