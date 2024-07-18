import os
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

api_key = os.environ.get('CF_KEY')
game_id = 00000
game_version_id = 00000
modLoaderTypes = {'Any': 0, 'Forge': 1, 'Cauldron': 2, 'LiteLoader': 3, 'Fabric': 4, 'Quilt': 5, 'NeoForge': 6}
base_url = "https://api.curseforge.com"

def get_data(type, version, loader):
    modLoaderType = modLoaderTypes[loader]
    url = f"{base_url}/v1/mods/search/"
    request = requests.get(url, params={"gameId": game_id, "classId": type, "gameVersion": version, "loaderType": modLoaderType}, headers={"x-api-key": api_key})
    if request.status_code != 200:
        print(f"Error: {request.status_code}")
        return {"pagination": {"totalCount": -1}}
    return json.load(request.content)

def get_total_hits_for_all(type, version, loaders):
    return [get_data(type, version, loader)["pagination"]["totalCount"] for loader in loaders]

version = '1.21'
labels = ['Fabric', 'Forge', 'NeoForge', 'Quilt']
content = get_total_hits_for_all('00000', version, labels)

fig, ax = plt.subplots()
ax.bar(labels, content)
ax.set_ylabel('Number of mods')
ax.set_title(f"Minecraft {version} Mods on CurseForge as of {datetime.today().strftime('%Y-%m-%d')}")

plt.show()