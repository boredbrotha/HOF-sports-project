import requests
import time
import pandas as pd


def outputFollowers(athDict,accTP):
    """
    This essentially takes a list of IG usernames, creates a list of their followers, puts them in a pandas dataframe, then outputs them to a spreadsheet.

    Inputs:
        dataFrame -> the (hopefully) empty pandas dataframe we'll use to output a spreadsheet
        accTP -> List of IG accounts the function will parse

    Output: A DoL that we can turn into a DataFrame
    """

    headers = {
	"X-RapidAPI-Key": "cdbbb8b397msh7ad25518cbc088ep1bba24jsn2e54fcaaac66",
	"X-RapidAPI-Host": "instagram-api-20231.p.rapidapi.com"
    }

    for cAthlete in accTP:
        username = cAthlete
        getUserID = "https://instagram-api-20231.p.rapidapi.com/api/get_user_id/{}".format(username)

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
                timesToIterate = fCount//100 +3

            querystring = None

            last_one = False
            for i in range(1,timesToIterate):

                r2 = requests.get(getFollowers, headers=headers,params= querystring)
                if('next_max_id' in r2.json()['data']):
                    querystring = {"max_id":"{}".format(r2.json()['data']['next_max_id'])}
                else: 
                    querystring = None
                    last_one = True
                    

                for i in range(len(r2.json()['data']['users'])):

                    athDict[cAthlete].append(r2.json()['data']['users'][i]['username'])


                #time.sleep(15)
                if last_one ==True:
                    break

        else:
            pass
            athDict[cAthlete].append(fCount)
            
    print("done")
    

def main():
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
    'michaelmagruire48': [],
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
    
    outputFollowers(athleteDict,athleteDict.keys())

    data = pd.DataFrame.from_dict(athleteDict, orient= 'index')

    data.to_excel("output.xlsx")
    
main()



"""
    athleteDict = {"billyguzzo_": [],
           "mrrelentess": [], 
           "cadenowik": [], 
           "vin_cognetta": [] ,
           "jordan_waterhouse03": [],
           "kingadinkra" : []}
"""