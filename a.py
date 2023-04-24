import requests
import time
import os.path
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import random
import sys
import discord

def getChildTiles(x, y, z):
    childX = x * 2
    childY = y * 2
    childZ = z + 1

    return [
        (childX, childY, childZ),
        (childX+1, childY, childZ),
        (childX+1, childY+1, childZ),
        (childX, childY+1, childZ),
    ]


def getAllDescendantTiles(x, y, z, max_z=None):
    if max_z is None:
        max_z = int(z) + 1
    result = []
    if int(z) < max_z:
        children = getChildTiles(x, y, z)
        result += children
        result_length = len(result)
        for i in range(result_length):
            child = result[i]
            grandchildren = getAllDescendantTiles(
                child[0], child[1], child[2], max_z)
            result += grandchildren
    random.shuffle(result)
    return result



z = 8
x = 143
y = 85
param1 = sys.argv[1]

WEBHOOK_URL = "https://discord.com/api/webhooks/1098551826745397288/aYM29TmQicqjShi5X5iEhpoe3MpVWRD_BRJ2U35eU0797mAycBQuZpzrrxGQl_EkUGHh"
requests.post(WEBHOOK_URL, { "content": "🦄 garage door is open" })

current_dir = os.getcwd()
print('1')
childTiles = getAllDescendantTiles(x, y, z, 18)
headers = {
    "User-Agent": "Mozilla/5.0 "
}
connect_str = "DefaultEndpointsProtocol=https;AccountName=deltimaimgstorage;AccountKey=WyYN7UCayN910wjS9Pq+w6+1FvlLFb4wEPzFN0gaC8WeZRCFmP3VPqrEj05BSgjYFreRLIlLA65V+AStowG2BA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "tiles"
container_client = blob_service_client.get_container_client(container_name)
extension = '.png'
i = 0
for childX, childY, childZ in childTiles:
    # childX, childY, childZ
    i = i+1
    print(f" {i} z {len(childTiles)}")
    requests.post(WEBHOOK_URL, { "content": f" {i} z {len(childTiles)}"})
    # print(f" time left {round((len(childTiles)-i)*0.25/60,2)} min")
    url = f"https://{param1}.tile.openstreetmap.org/{childZ}/{childX}/{childY}.png"
    filename = 'tile_{}_{}_{}.png'.format(childZ, childX, childY)
    blob_client = container_client.get_blob_client(filename)
    if blob_client.exists():
        # print(f"!!!The blob '{filename}' exists in container '{container_name}'")
      
        continue
    if os.path.isfile(filename):
        continue
    time.sleep(0.25)
    # print(url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(response.status_code)
        requests.post(WEBHOOK_URL, { "content": f"{response.status_code}" })
        
    else:
        with open(filename, "wb") as f:
            f.write(response.content)
        with open(filename, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(url)
            # print("uploaded")
            file_path = os.path.join(current_dir, filename)
            os.remove(file_path)
