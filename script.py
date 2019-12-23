import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def grabber(key):
    page=1
    print(key)
    l=[]
    print("Script running")
    while page != 0 :

        url="https://internshala.com/internships/keywords-"+key+"/page-"+ str(page)
        r=requests.get(url)
        c=r.content
        soup=bs(c,"html.parser")
        all=soup.find_all("div",{"class":"container-fluid individual_internship"})
        print(page)
        #test if the current page is last page or not
        test=soup.find("input",{"id":"isLastPage"})
        if test["value"] == "1":
            page=0
        else:
            page+=1


        """
        Title, By, Location, Stipend, Duration, Skills, URL
        """
        for item in all:
            d={}
            #Title
            title=item.find("h4")
            try:
                d["Title"]=title["title"]
            except:
                pass
            #By
            by=item.find("a",{"class":"link_display_like_text"})
            try:
                d["By"]=by.text.strip()

            except:
                pass

            #URL
            link=item.find_all("a")
            try:
                d["URL"]="https://www.internshala.com"+[a["href"] for a in link if a["href"].startswith("/internship/detail/")][0]
            except:
                pass

            #Location
            location=item.find("a",{"class":"location_link"})
            try:
                d["Location"]=location.text
            except:
                pass

            #Stipend
            stipend=item.find("i",{"class":"fa fa-inr"})
            try:
                d["Stipend"]="INR " + stipend.next_sibling.strip()
            except:
                pass

            #Duration
            duration=item.find_all("td")
            try:
                d["Duration"]=duration[1].text.strip()
            except:
                pass

            #Skills
            """
            Requests individual URL's and scrapes "Skills required" from them. Also responsible for slow execution of program.
            """
            try:
                r1=requests.get(d["URL"])
                c1=r1.content
                soup1=bs(c1,"html.parser")
                skills=soup1.find("span",{"id":"skillNames"})
                d["Skills"]=skills.get_text()
            except:
                pass
            l.append(d)
    #Exporting to csv file
    df=pd.DataFrame(l)
    df.to_csv(key+'.csv')
    print("Exported to"+key+".csv")
