from tkinter import *
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import threading

window=Tk()
window.wm_title("Internshala-scraper")
window.geometry("520x220")
window.iconbitmap('scraper.ico')
window.configure(background='black')
window.resizable(0,0)

flag=0

def update_status():

    def callback2():

        global flag
        # Get the current message
        current_status = status["text"]

        # If the message is "Working...", start over with "Working"
        if current_status.endswith("..."): current_status = "Working"

        # If not, then just add a "." on the end
        else: current_status += "."

        # Update the message
        status["text"] = current_status

        # After 1 second, update the status
        if flag==0:
            window.after(1000, callback2)
        elif flag==1:
            return 0
    s=threading.Thread(target=callback2)
    s.start()

def grabber(key):
    task["text"]=" "
    status["text"]="Working"
    page = 1
    l=[]

    update_status()

    def callback():
        global flag
        nonlocal page
        nonlocal l
        while page != 0 :
            task["text"]="Fetching Page "+ str(page)
            url="https://www.internshala.com/internships/keywords-"+key+"/page-"+ str(page)
            r=requests.get(url)
            c=r.content
            soup=bs(c,"html.parser")
            all=soup.find_all("div",{"class":"container-fluid individual_internship"})
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
                title=item.find("h4")
                by=item.find("a",{"class":"link_display_like_text"})
                link=item.find_all("a")
                location=item.find("a",{"class":"location_link"})
                stipend=item.find("i",{"class":"fa fa-inr"})
                duration=item.find_all("td")
                try:
                    d["Title"]=title["title"]
                    d["By"]=by.text.strip()
                    d["URL"]="https://www.internshala.com"+[a["href"] for a in link if a["href"].startswith("/internship/detail/")][0]
                    d["Location"]=location.text
                    d["Stipend"]="INR " + stipend.next_sibling.strip()
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
            task["text"]="Page "+ str(page-1) +" Fetched"
            print(page)
        flag=1
        status["text"]="Completed"
        #Exporting to csv file
        df=pd.DataFrame(l)
        df.to_csv(key+'.csv')
        task["text"]=str(len(l))+" records exported to "+key+".csv"

    t = threading.Thread(target=callback)
    t.start()

l1=Label(window,text="Enter keyword(s)",fg='white',bg='black')
l1.grid(row=1,column=1)

key_text=StringVar()
e1=Entry(window,textvariable=key_text,width=50)
e1.grid(row=2,column=1)

b1=Button(window,text="SEARCH", width=12,command=lambda: grabber(key_text.get()),bg='white',fg='black')
b1.grid(row=4,column=1)

status=Label(window,text=" ",fg='white',bg='black')
status.grid(row=5,column=1)

task=Label(window,text=" ",fg='white',bg='black')
task.grid(row=6,column=1)

author=Label(window,text="-devanshds",font=('helvetica', 6),fg='white',bg='black')
author.grid(row=7,column=2)


window.grid_columnconfigure(0, minsize=50)
window.grid_rowconfigure(0,minsize=40)
window.grid_rowconfigure(3,minsize=20)

window.mainloop()
