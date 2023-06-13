import requests
import time
import pandas

"""
username = "sallyevesilber"

getUserID = "https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{}".format(username)

headers = {
	"X-RapidAPI-Key": "",
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
"""

athList = ["billyguzzo_", "mrrelentess", "cadenowik", "vin_cognetta" ,"jordan_waterhouse03"]


def outputFollowers(dataFrame, accTP):
    """
    This essentially takes a list of IG usernames, creates a list of their followers, puts them in a pandas dataframe, then outputs them to a spreadsheet.

    Inputs:
        dataFrame -> the (hopefully) empty pandas dataframe we'll use to output a spreadsheet
        accTP -> List of IG accounts the function will parse

    Output: A spreadsheet!
    """

    headers = {
	"X-RapidAPI-Key": "",
	"X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
    }

    for i in accTP:
        username = i
        getUserID = "https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{}".format(username)

        r0 = requests.get(getUserID, headers=headers) #Get userID from username

        userID=r0.json()['data']['id']

        fCount = r0.json()['data']['followers']

        #Now we'll check if this userID is private
        getUserInfo = "https://instagram-api-20231.p.rapidapi.com/api/get_user_info/{}".format(userID)

        r1 = requests.get(getUserInfo, headers=headers)

        isPrivate = r1.json()['data']['is_private']

        if isPrivate == 'false': #If isPrivate is false, we get all of the usernames
            
            getFollowers = "https://instagram-api-20231.p.rapidapi.com/api/user_followers/{}".format(userID)
            timesToIterate = fCount%100
            followerList = []
            querystring = None
            for i in range(1,timesToIterate):

                r2 = requests.get(getFollowers, headers=headers,params= querystring)

                querystring = {"max_id":"{}".format(r2.json()['data']['next_max_id'])}

                for i in range(len(r2.json()['data']['users'])):

                    followerList.append(r2.json()['data']['users'][i]['username'])

                time.sleep(30)
    

        else:
            pass
            #ADD LATER: make fCount a new row for the corresponding name
            
    print("done")




