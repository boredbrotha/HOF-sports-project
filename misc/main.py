import requests
import time
import pandas as pd
import numpy as np
import urllib.request
from sys import exit
import cv2 as cv


#https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
#^^ using this for the image comparison stuff

athleteDict = {
    'billyguzzo_': [],
    'mrrelentess': [],
    'cadenowik': [],
    'vin_cognetta': [],
    'jordan_waterhouse03': [],
    'owen_fallon': [],
    'nhalnbk7': [],
    'vzelisko': [],
    'josh_ilo': [],
    'dcunningham._': [],
    'abrownlee21': [],
    'claydenstorff': [],
    'alexdobbins14': [],
    'higlejonathon': [],
    'danieldesantis4': [],
    'oliverkovass': [],
    'jimmy.stines': [],
    'alex.stackhouse': [],
    'treyfabrocini': [],
    'mason.marchinsky': [],
    '_joshstegich': [],
    'lariviere.christian': [],
    '_sean_carr': [],
    'michael_ballenger': [],
    'jonadamson11': [],
    'hdirico21': [],
    'nimer_26': [],
    'cadecormier7': [],
    'chaaunce': [],
    'jonathanbearden2': [],
    'eddiedreher': [],
    'willsolis27': [],
    'collin.j.murphy': [],
    'matthewwiley_': [],
    'charliep_22_': [],
    'andrew_brown_37': [],
    'colinluse': [],
    'michaelmaguire48': [],
    '_jeffmoore': [],
    'nj.austria': [],
    'willisgauze': [],
    'cole_graney36': [],
    'caseycampbell00': [],
    'connor_kratzert': [],
    'cburzynski55': [],
    'thegrandcanyon_56': [],
    'matthewrussell20': [],
    'samsecrest': [],
    'gmcclung_': [],
    'kevin_stone123456': [],
    'brianstone7587': [],
    'austin.smith7.3': [],
    'jacksonwalsh20': [],
    'h.slack_': [],
    'willsforman': [],
    'alex_sket21': [],
    't.dunn_': [],
    'trevor.goodrich': [],
    'prestona_73': [],
    'kadyn0101': [],
    'loganyater3': [],
    '__jwill3': [],
    'evangelo_24': [],
    'preston.fisk': [],
    'jthallett15': [],
    'casper_rublowsky': [],
    'mpmead25': [],
    'liam.mendham': [],
    'davidsonojump': [],
    'shawn.ugbana': [],
    'jackp_dee': [],
    'ryanlallly': []
}

def outputFollowers(athDict,accTP):


    """
    This essentially takes a list of IG usernames,

    Inputs:
        athDict -> a dictionary containing the athlete handles as the key and an empty array to dump their followers into.
        accTP -> List of IG accounts the function will parse

    Output: No output. It's an in-place function.
    """

    headers = {
	"X-RapidAPI-Key": "",
	"X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
    }

    for cAthlete in accTP:
        username = cAthlete
        getUserID = "https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{}".format(username)

        print("Debug: We're currently working on: ",cAthlete)

        r0 = requests.get(getUserID, headers=headers) #Get userID from username


        userID=r0.json()['data']['id']

        fCount = r0.json()['data']['followers']


        #Now we'll check if this userID is private
        getUserInfo = "https://instagram-api-20231.p.rapidapi.com/api/get_user_info/{}".format(userID)

        r1 = requests.get(getUserInfo, headers=headers)

        isPrivate = r1.json()['data']['is_private']

        if isPrivate == False: #If isPrivate is false, we get all of the usernames
            
            getFollowers = "https://instagram-api-20231.p.rapidapi.com/api/user_followers/{}".format(userID)

            if fCount%100 == 0:
                timesToIterate = fCount/100
            else:
                timesToIterate = fCount//100 +2

            querystring = None


            while True:
                try:
                    r2 = requests.get(getFollowers, headers=headers,params= querystring)
                    
                    if r2.json()['data']['big_list'] == False:
                        for i in range(len(r2.json()['data']['users'])):
                            athDict[cAthlete].append(r2.json()['data']['users'][i]['username'])
                        break

                    if('next_max_id' in r2.json()['data']):
                        querystring = {"max_id":"{}".format(r2.json()['data']['next_max_id'])}
                        
                    print("Debug: Current ID: ",r2.json()['data']['next_max_id'])

                    for i in range(len(r2.json()['data']['users'])):

                        athDict[cAthlete].append(r2.json()['data']['users'][i]['username'])

                    print("Debug: appended to dictionary!")


                    
                except:
                    print("An error has occurred. Here's what the API returns:")
                    print(r2.json())
                    exit()

        else:
            pass
            athDict[cAthlete].append(fCount)
            
    print("done")
    
def compareImages(storyImagePath):
    """
    SO, Here's the rundown of how this function works:

    1. It has the parameter that is an athlete's instagram story image
    2. It runs the Template Matching algorithm I found against the template images
    3. If there's a similarity, it returns True. Else, it returns False.
    """
    
    img = cv.imread(storyImagePath, cv.IMREAD_GRAYSCALE)

    assert img is not None, "file could not be read, check with os.path.exists()"

    img2 = img.copy()
    
    #First, we load in the local images

    temp0 = cv.imread("./images/bladestory0.jpg", cv.IMREAD_GRAYSCALE)
    temp1 = cv.imread("./images/bloodybagstory0.jpg", cv.IMREAD_GRAYSCALE)
    temp2 = cv.imread("./images/draculastory0.jpg", cv.IMREAD_GRAYSCALE)
    
    tempList = [temp0, temp1, temp2]

    assert temp0 is not None, "file could not be read, check with os.path.exists()"
    assert temp1 is not None, "file could not be read, check with os.path.exists()"
    assert temp2 is not None, "file could not be read, check with os.path.exists()"
    
    method = 'cv.TM_SQDIFF_NORMED'
    threshold = .01
    for i in tempList:
        res = cv.matchTemplate(img, i, eval(method))
        print("The threshold: ",np.amin(res))
        if np.amin(res) < threshold:
            return True
        
    return False

def isPostCompleted(athDict):
    
    """
     note: I should eventually add the functionality for this function to be able to have a list of raw images to compare to that it will push into the compareImages function, but this is good for now.
     note note: I should also eventually add the functionality of having the user select what type of media the script should look for (story, post, etc). For implementation's sake, stories are fine to initially start with. 


     1. For each athlete in the dict, check if they have a story up.
     2. If they have a story up, run throgh the stories and brute force check if any of them match the set of images we have. If true, append True to the value of the the athlete name key thingy. False if otherwise.
    """
    
    headers = {
	"X-RapidAPI-Key": "cdbbb8b397msh7ad25518cbc088ep1bba24jsn2e54fcaaac66",
	"X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
    }

    handleList = athDict.keys()

    checkType = input("What kind of media are you looking for? \n 1: Story \n 2: Post \n Input here: ")

    if int(checkType) == 1:

        for handle in handleList:

            url = "https://instagram-api-20231.p.rapidapi.com/api/user_stories_from_username/{}".format(handle)

            r1 = requests.get(url, headers=headers)

            if (r1.json()['data']['reel'] == None):
                athDict[handle].append(None)
            else:
                stories = r1.json()['data']['reel']['items']
                for s in stories:

                    sUrl = s['image_versions2']['candidates'][0]['url']

                    data = requests.get(sUrl).content
                    f = open('./images/{}post.jpg'.format(handle),'wb') 

                    f.write(data)
                    f.close()

                    if compareImages("./images/{}post.jpg".format(handle)):
                        athDict[handle].append(True)
                    else:
                        athDict[handle].append(False)
    
    elif int(checkType) == 2:
        for handle in handleList:
            url = "https://instagram-api-20231.p.rapidapi.com/api/user_posts_from_username/{}".format(handle)

            querystring = {"count":"10"}

            listOfPosts = requests.get(url, headers = headers, params = querystring).json()['data']['items']

            # I eventually need to make it so that it returns None if an IG doesn't have any posts in it, but for now, all is ok.

            for post in listOfPosts:
                sUrl = post['image_versions2']['candidates'][1]['url']
                data = requests.get(sUrl).content
                f = open('./images/{}post.jpg'.format(handle),'wb') 
                f.write(data)
                f.close()
                if compareImages("./images/{}post.jpg".format(handle)):
                    athDict[handle].append(True)
                else:
                    athDict[handle].append(False)







                    

        








    


def main():
    # outputFollowers(athleteDict,athleteDict.keys())
    # data = pd.DataFrame.from_dict(athleteDict, orient= 'index')
    # data = data.transpose()
    # data.to_excel("output.xlsx")


    # df = pd.read_excel("./output.xlsx")
    # uniquedf= {}
    # for col in df:
    #     uniquedf[col] = df[col].unique().tolist()



    # for key in uniquedf:
    #     for i in uniquedf[key]:
    #         if i == np.nan:
    #             uniquedf[key].remove(i)

    # uniquedf = pd.DataFrame.from_dict(uniquedf, orient= 'index')
    # uniquedf = uniquedf.transpose()
    # uniquedf.to_excel("uniqueoutput.xlsx")

    
    thisDict = {'hofsportsllc':[]}
    isPostCompleted(thisDict)
    print(thisDict)
    
    

    #print(compareImages("./images/bloodybagstory.jpg"))

main()
