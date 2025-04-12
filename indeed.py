import requests
from bs4 import BeautifulSoup
import pandas as pd

api_key = '39a9cad8dd03d7254823631a6f859bc8' 

Jobs = []
Company = []
Locations = []
Links = []
for page in range(0, 50): 
    print(f"\nScraping page starting at result {page}...\n")

    target_url = f'https://www.indeed.com/jobs?q=data+analyst&start={page}'
    scraper_url = f"http://api.scraperapi.com/?api_key={api_key}&url={target_url}"

    response = requests.get(scraper_url)
    print("Status:", response.status_code)
    
    # print(scraper_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        job_titles = soup.find_all('h2', class_='jobTitle')
        company_name = soup.find_all('span',class_='css-1h7lukg eu4oa1w0')
        locations = soup.find_all('div',class_='css-1restlb eu4oa1w0')
        job_links = soup.find_all('a', class_='jcs-JobTitle')
        for job in job_titles:
            Jobs.append(job.text.strip())
    else:
        print("Failed to scrape this page.")

    for company in company_name:
        Company.append(company.text.strip())

    for location in locations:
        Locations.append(location.text.strip())


    for link in job_links:
        job_url = link.get('href')
        if job_url:
            full_job_url = f'https://www.indeed.com{job_url}'
            Links.append(full_job_url)

min_len = min(len(Jobs),len(Company),len(Locations),len(Links))

df = pd.DataFrame({
    'Title':Jobs[:min_len],
    'Company_Name':Company[:min_len],
    'Locations':Locations[:min_len],
    'Jobs_Link':Links[:min_len]
})

df.to_csv('C:\\Users\\HM Laptops\\Desktop\\Web Scrapping\\Indeed.csv',index=False)
