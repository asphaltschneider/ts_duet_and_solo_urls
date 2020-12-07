import requests
import json

## enter your username, the client id and the client secret in here
TWITCH_USERNAME = "<YOUR_NAME_ON_TWITCH>"
CLIENT_ID = "<YOUR_CLIENT_ID>"
CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"

## As Twitch Sings generates uploads under your profile, we use "upload"
VIDEO_TYPE = "upload"

secretKeyURL = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials".format(CLIENT_ID, CLIENT_SECRET)
responseA = requests.post(secretKeyURL)
accessTokenData = responseA.json()

userIDURL = "https://api.twitch.tv/helix/users?login=%s"%TWITCH_USERNAME
responseB = requests.get(userIDURL, headers={"Client-ID":CLIENT_ID,
                                             'Authorization': "Bearer "+accessTokenData["access_token"]})
userID = responseB.json()["data"][0]["id"]

twcontinue = 1
twstart = 1

while twcontinue == 1:
    if twstart == 1:
        findVideoURL = "https://api.twitch.tv/helix/videos?user_id=%s&type=%s&first=100"%(userID, VIDEO_TYPE)
    else:
        findVideoURL = "https://api.twitch.tv/helix/videos?user_id=%s&type=%s&first=100&after=%s" % (
        userID, VIDEO_TYPE, aftercoursor)

    responseC= requests.get(findVideoURL, headers={"Client-ID":CLIENT_ID,
                                                   'Authorization': "Bearer "+accessTokenData["access_token"]})

    j = json.loads(responseC.text)

    if j['data']:
        for vodlist in j['data']:
            # in case you have more uploads, we limit everything on the usually generated titles
            if ("Duet with " in vodlist['title']) or ("Solo performance: " in vodlist['title']):
                print(vodlist['url']," - ",vodlist['title'])

    if j['pagination']:
        aftercoursor = (j['pagination']['cursor'])
        twcontinue = 1
    else:
        twcontinue = 0

    twstart = 0

