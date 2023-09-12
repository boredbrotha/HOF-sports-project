import requests
import time
import pandas as pd
import numpy as np
import urllib.request
from sys import exit
import cv2 as cv

class HOFlib:

    def __init__(self, aList = None, apiHeaders = None) -> None:
        if aList != None:
            self.athletes = aList
        else: 
            self.athletes = []

        if apiHeaders != None:
            self.headers = apiHeaders

    def createDict(self, potentialList = None):
        rDict = {}
        """
        This function creates the dictionaries that the later functions will use. It creates the dictionary from the athlete list attribute of the class.

        Input: None
        Output: A DoL
        """
        if potentialList == None:
            for i in self.athletes:
                rDict[i] = []
        
        else:
            for i in potentialList:
                rDict[i] = []

        return rDict
    
    def outputFollowers(self, athDict):
        """
        This essentially takes a list of IG usernames and a dicctionary and fills the dictionary with the IG usernames' followers (per account, of course).

        Inputs:
            athDict -> a dictionary containing the athlete handles as the key and an empty array to dump their followers into.

        Output: No output. It's an in-place function.
        """

        headers = self.headers

        for cAthlete in self.athletes:
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


                querystring = None


                while True:
                    try:
                        r2 = requests.get(getFollowers, headers=headers, params= querystring)
                        
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

    def export(self, athDict, eType = False):
        """
        This function exports a DoL into a CSV or Excel format depending on the eType parameter.

        False = CSV
        True = Excel
        """

        data = pd.DataFrame.from_dict(athDict, orient= 'index')
        
        data = data.transpose()

        if eType == False:
            
            data.to_csv("./output.csv")
        
        elif eType == True:
            data.to_excel("./outpus.xlsx")

        else:
            print("You fucked up.")
            exit()
        
    def compareImages(self, storyImagePath):
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
        
    def isPostCompleted(self, athDict):
            
        """
        note: I should eventually add the functionality for this function to be able to have a list of raw images to compare to that it will push into the compareImages function, but this is good for now.
        note note: I should also eventually add the functionality of having the user select what type of media the script should look for (story, post, etc). For implementation's sake, stories are fine to initially start with. 


        1. For each athlete in the dict, check if they have a story up.
        2. If they have a story up, run throgh the stories and brute force check if any of them match the set of images we have. If true, append True to the value of the the athlete name key thingy. False if otherwise.
        """
        

        handleList = athDict.keys()

        checkType = input("What kind of media are you looking for? \n 1: Story \n 2: Post \n Input here: ")

        if int(checkType) == 1:

            for handle in handleList:

                url = "https://instagram-api-20231.p.rapidapi.com/api/user_stories_from_username/{}".format(handle)

                r1 = requests.get(url, headers=self.headers)

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

                        if self.compareImages("./images/{}post.jpg".format(handle)):
                            athDict[handle].append(True)
                        else:
                            athDict[handle].append(False)
        
        elif int(checkType) == 2:
            for handle in handleList:
                url = "https://instagram-api-20231.p.rapidapi.com/api/user_posts_from_username/{}".format(handle)

                querystring = {"count":"10"}

                listOfPosts = requests.get(url, headers = self.headers, params = querystring).json()['data']['items']

                # I eventually need to make it so that it returns None if an IG doesn't have any posts in it, but for now, all is ok.

                for post in listOfPosts:
                    sUrl = post['image_versions2']['candidates'][1]['url']
                    data = requests.get(sUrl).content
                    f = open('./images/{}post.jpg'.format(handle),'wb') 
                    f.write(data)
                    f.close()
                    if self.compareImages("./images/{}post.jpg".format(handle)):
                        athDict[handle].append(True)
                    else:
                        athDict[handle].append(False)


    

        


    
