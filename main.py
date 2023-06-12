import requests
import time
import pandas

username = "sallyevesilber"

getUserID = "https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{}".format(username)

headers = {
	"X-RapidAPI-Key": "cdbbb8b397msh7ad25518cbc088ep1bba24jsn2e54fcaaac66",
	"X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
}

response = requests.get(getUserID, headers=headers)

userID=response.json()['data']['id']

fCount = response.json()['data']['followers']

getFollowers = "https://instagram-api-20231.p.rapidapi.com/api/user_followers/{}".format(userID)


timesToIterate = fCount%100
followerList = []
querystring = None
for i in range(1,timesToIterate):
    getFollowers = "https://instagram-api-20231.p.rapidapi.com/api/user_followers/{}".format(userID)
    
    response = requests.get(getFollowers, headers=headers,params= querystring)
    querystring = {"max_id":"{}".format(response.json()['data']['next_max_id'])}

    for i in range(len(response.json()['data']['users'])):
        followerList.append(response.json()['data']['users'][i]['username'])
    time.sleep(30)
    
print("done")



print(followerList)

def outputFollowers(dataFrame, accTP):
    """
    This essentially takes a list of IG usernames, creates a list of their followers, puts them in a pandas dataframe, then outputs them to a spreadsheet.

    Inputs:
        dataFrame -> the (hopefully) empty pandas dataframe we'll use to output a spreadsheet
        accTP -> List of IG accounts the function will parse

    Output: A spreadsheet!
    """

    