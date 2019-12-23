```TL;DR : Web scraper application using bs4 and tkinter with some multithreading to scrape internships from www.internshala.com```
# Internshala-scraper

Simplifies the task of finding and applying to relevant internships on internshala.com by fetching all the records that match a certain keyword and exporting them to a more manageable .csv format. 

The key feature here is that the application fetches the skills required from the details page thus saving the user's time that would have been wasted to visit each individual detail page. 

<p align="center">
  <img src="https://i.imgur.com/vREMrC0.png" height=1000>
</p>

## Details:

  ### Libraries used :
    - Tkinter
    - BeautifulSoup4
    - Requests
    - Threading
 
  ### Features :
    - Grabs following data for individual record: Title, By, URL, Location, Stipend, Duration, and Skills Required
    - Waiting text that displays the script is running
    - Multithreading to make the application run smoother
    - Dark theme for aesthetic a-holes

## Usage:
  - To download the executable, run following commands in cmd:
  ```git clone https://github.com/devanshds/Internshala-scraper.git```
  
  ```cd Internshala-scraper```
  
  - Run the file ```scraper.exe``` present in ```dist``` folder.
  
    <img src="https://i.imgur.com/FqyXeTV.png" height=150>
  - Enter the topic of internships you want to find and press the ```Search``` button.
  
    <img src="https://i.imgur.com/f0OEXbP.png" height=150>
  - Wait for completion.
  
    <img src="https://i.imgur.com/iN5bCdT.png" height=150>
  - Find the csv file created in ```dist``` folder.

## Notes:
  - The .exe may take some time to launch as it is packaged with ```--onefile``` attrib in pyinstaller.
  - Application needs to be restarted before a different keyword can be searched.
  - I wish I was better at typing and didnt have to prepare such readmes to showcase my work to employers.
  - Yes, I use this to find myself internships.
  - I hope someday someone reads all this crap.
