import requests
import pandas as pd
import numpy as np
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
        else:
            self.headers = None

    def createDict(self, potentialList = None):
  
        """
        This function creates the dictionaries that the later functions will use. It creates the dictionary from the athlete list attribute of the class.


        Input: None
        Output: A Dictionary of Lists 
        """

        rDict = {}


        if potentialList == None:
            for i in self.athletes:
                rDict[i] = []
        
        else:
            for i in potentialList:
                rDict[i] = []

        return rDict
    
    def outputFollowers(self, athDict):
        """
        This essentially takes a list of Instagram usernames and a dicctionary and fills the dictionary with the IG usernames' followers (per account, of course).

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
            print("Debug: getID response:", r0.json())

            if (r0.json()['message'] == "Username is not valid"):
                continue

            userID=r0.json()['data']['id']
            
            fCount = r0.json()['data']['followers']


            #Now we'll check if this userID is private
            getUserInfo = "https://instagram-api-20231.p.rapidapi.com/api/get_user_info/{}".format(userID)

            r1 = requests.get(getUserInfo, headers=headers)

            isPrivate = r1.json()['data']['is_private']

            if isPrivate == False: #If isPrivate is false, we get all of the usernames
                
                getFollowers = "https://instagram-api-20231.p.rapidapi.com/api/user_followers/{}".format(userID)


                querystring = None


                while True: #The function is now going to count followers with the API until it can no longer do so.
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


                        
                    except: #When it reaches an error, it'll exit the loop and print an error 
                        print("An error has occurred. Here's what the API returns:")
                        print(r2.json())
                        exit()

            else:
                athDict[cAthlete].append(fCount)

    def getPitchData(self, athDict):
        
        sets = [set(athDict[i]) for i in athDict]

        counts = [len(athDict[i]) for i in athDict]

        intersections = set.intersection(*sets)

        string = "Aggregate count: {} \nIntersections: {}".format(sum(counts), len(intersections))

        return string
        







         

    def export(self, athDict, eType = False):
        """
        This function exports a DoL into a CSV or Excel format depending on the eType parameter.

        False = CSV
        True = Excel
        """

        data = pd.DataFrame.from_dict(athDict, orient= 'index')
        
        data = data.transpose()

        if eType == False: #If user wants a csv
            
            data.to_csv("./output.csv") 
        
        elif eType == True: #If user wants an excel file
            data.to_excel("./output.xlsx")

        else: #If they didn't follow the parameters of the function
            print("You messed up somewhere! Make 'eType' False if you want to export an .xlsx file, and make it True if you want to export a .csv")
            exit()
        
    def compareImages(self, storyImagePath):
        """
        Here's a quick run-down of how this function works.

        1. It has the parameter that is an athlete's assigned image to post on their story
        2. It runs the Template Matching algorithm against the template images
        3. If there's a similarity, it returns True. If not, it returns False.
        """
        
        img = cv.imread(storyImagePath, cv.IMREAD_GRAYSCALE) #We read in the image we're tryna compare to the template images

        assert img is not None, "file could not be read, check with os.path.exists()"
        
        #First, we load in the local images

        temp0 = cv.imread("./misc/images/bladestory0.jpg", cv.IMREAD_GRAYSCALE)
        temp1 = cv.imread("./misc/images/bloodybagstory0.jpg", cv.IMREAD_GRAYSCALE)
        temp2 = cv.imread("./misc/images/draculastory0.jpg", cv.IMREAD_GRAYSCALE)
        
        tempList = [temp0, temp1, temp2]

        """
         NOTE FOR WHOEVER USES THIS IN THE FUTURE: You're going to have to manually hardcode temp depending on the context. If there are 4 advertisement images, there will be 4 temps, and so forth.
        """

        assert temp0 is not None, "file could not be read, check with os.path.exists()"
        assert temp1 is not None, "file could not be read, check with os.path.exists()"
        assert temp2 is not None, "file could not be read, check with os.path.exists()"
        
        method = 'cv.TM_SQDIFF_NORMED'
        threshold = .01
        for i in tempList: #For each template image, we check if img is similar to them. It returns true if it is. False if not.
            res = cv.matchTemplate(img, i, eval(method))
            print("The threshold: ",np.amin(res))
            if np.amin(res) < threshold:
                return True
            
        return False
        
    def isPostCompleted(self, athDict):
            
        """
        note: I should eventually add the functionality for this function to be able to have a list of raw images to compare to that it will push into the compareImages function, but this is good for now.
        note note: I should also eventually add the functionality of having the user select what type of media the script should look for (story, post, etc). For now, stories are fine to initially start with. 

        

        How this algorithm works:

            1. For each athlete in the dict, check if they have a story up.
            2. If they have a story up, run throgh the stories and brute force check if any of them match the set of images we have. If true, append True to the value of the the athlete name key thingy. False if otherwise.
            
        """
        

        handleList = athDict.keys()

        checkType = input("What kind of media are you looking for? \n 1: Story \n 2: Post \n Input here: ")

        # ^^^^ We query to see whether the user wants to look for an athlete's story or IG post.

        if int(checkType) == 1: #If user wants a story

            for handle in handleList: #The function goes through every IG handle it's given.

                url = "https://instagram-api-20231.p.rapidapi.com/api/user_stories_from_username/{}".format(handle)

                r1 = requests.get(url, headers=self.headers) #We call the API to get all the posts

                if (r1.json()['data']['reel'] == None): #If there are none, we return "None" for this athlete
                    athDict[handle].append(None)
                else:
                    stories = r1.json()['data']['reel']['items']
                    for s in stories: #If there are some stories, we iterate through them and check each one to see if it matches with the advertisements we have on file.

                        sUrl = s['image_versions2']['candidates'][0]['url']

                        data = requests.get(sUrl).content
                        f = open('./images/{}post.jpg'.format(handle),'wb') 

                        f.write(data)
                        f.close()

                        if self.compareImages("./images/{}post.jpg".format(handle)):
                            athDict[handle].append(True)
                        else:
                            athDict[handle].append(False)
        
        elif int(checkType) == 2: #If user wants a post
            for handle in handleList:
                url = "https://instagram-api-20231.p.rapidapi.com/api/user_posts_from_username/{}".format(handle)

                querystring = {"count":"10"}

                try:
                    listOfPosts = requests.get(url, headers = self.headers, params = querystring).json()['data']['items']
                except:
                    print("Error: Either there's no posts on this account, or the API tweaked. Go ahead and run the program again.")
                    exit()

                # I eventually need to make it so that it returns None if an IG doesn't have any posts in it, but for now, all is ok.

                for post in listOfPosts: # For now, we iterate through the first 10 posts of an account
                    sUrl = post['image_versions2']['candidates'][1]['url']
                    data = requests.get(sUrl).content
                    f = open('./images/{}post.jpg'.format(handle),'wb') 
                    f.write(data)
                    f.close()
                    if self.compareImages("./images/{}post.jpg".format(handle)):
                        athDict[handle].append(True)
                    else:
                        athDict[handle].append(False)


    

        


    
