import re
from turtle import title
from bs4 import BeautifulSoup
import requests

html_text = requests.get("https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=").text
soup = BeautifulSoup(html_text, "lxml")

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

for info in job_info:
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

    print(f"Job Title: {info["title"]}")
    print(f"Company Title: {info["company"]}")
    print(f"Location: {info["location"]}")
    print(f"Experience: {info["experience"]}")
    print(f"Skills: {info["skills"]}")
    print(f"Posted: {info["posted"]}")
    print(f"Job-Page: {info["job_page"]}\n")