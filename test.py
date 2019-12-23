from tkinter import *
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import threading

window=Tk()
window.wm_title("Internshala-scraper")
window.geometry("520x200")
window.iconbitmap('scraper.ico')
window.configure(background='black')
window.resizable(0,0)


def grabber(key):

    page=1
    l=[]

    while page != 0 :

        url="https://internshala.com/internships/keywords-"+key+"/page-"+ str(page)
        r=requests.get(url)
        c=r.content
        soup=bs(c,"html.parser")
        all=soup.find_all("div",{"class":"container-fluid individual_internship"})

        #test if isLastPage=1
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
            try:
                r1=requests.get(d["URL"])
                c1=r1.content
                soup1=bs(c1,"html.parser")
                skills=soup1.find("span",{"id":"skillNames"})
                d["Skills"]=skills.get_text()
            except:
                pass
            l.append(d)
        print(page)
    #Exporting to csv file
    df=pd.DataFrame(l)
    df.to_csv(key+'.csv')
    task["text"]=str(len(l))+" records exported to "+key+".csv"



l1=Label(window,text="Enter keyword(s)")
l1.grid(row=1,column=1)

key_text=StringVar()
e1=Entry(window,textvariable=key_text,width=50)
e1.grid(row=2,column=1)

b1=Button(window,text="SEARCH", width=12,command=lambda: grabber(key_text.get()))
b1.grid(row=3,column=1)

status=Label(window,text=" ")
status.grid(row=4,column=1)

task=Label(window,text=" ")
task.grid(row=5,column=1)

author=Label(window,text="-devanshds",font=('helvetica', 6))
author.grid(row=6,column=2)


window.grid_columnconfigure(0, minsize=50)
window.grid_rowconfigure(0,minsize=40)

window.mainloop()
