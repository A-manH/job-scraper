from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd
import re

def parse(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    return soup

def get_jobs():
    soup = parse("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=")
    job_list = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
    job_info = [{
                "title": job.a.text.strip(), 
                "company": job.h3.text.strip(), 
                "location": job.find("li", class_="srp-zindex location-tru").text.strip(),
                "experience": job.find("i", class_="srp-icons experience").parent.text.strip(),
                "skills": ", ".join(job.find("div",class_="more-skills-sections").text.split()),
                "posted": job.find("span", class_="sim-posted").text.strip(),
                "job_page": job.find("a", class_="posoverlay_srp")["href"]
                } for job in job_list]
    return job_info


connection = sqlite3.connect("data.db")
c = connection.cursor()
def get_info():
    job_info = get_jobs()
    for i, info in enumerate(job_info):
        has_int = False

        if info["posted"] == "few days ago":
            continue
        
        for word in info["posted"].split():
            if word.isdigit():
                if int(word) > 5:
                    has_int = True
                break
            
        if has_int == True: 
            has_int = False
            continue

        matches = re.search(r"(\d)[- ]+(\d)", info["experience"])
        min_exp, max_exp = matches.groups()

        c.execute('''INSERT INTO data(id, job_title, company_name, min_exp, max_exp, location, date_posted, job_page) VALUES(?,?,?,?,?,?,?,?)''', 
                    (
                        i,
                      info["title"],
                      info["company"],
                      int(min_exp),
                      int(max_exp),
                      info["location"],
                      info["posted"],
                      info["job_page"]
                    ))
        
connection.commit()
get_info()

df = pd.read_sql_query("SELECT * FROM data", connection)
df.to_csv("data.csv")
connection.close()

