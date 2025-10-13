'''LIBRARIES!!
beautifulsoup4
requests
pandas
openpyxl
lxml'''

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

def user_input(): #GET KEYWORDSSSS
    inp = input("give me csv keywordsssss!!!! ")
    split_keywords = inp.split(',')
    
    final_keywords = []
    #alyssa u need to clean ur shit 

    for kw in split_keywords:
        cleaned_keyword = kw.strip()
        final_keywords.append(cleaned_keyword)
    
    #url comma %2C, fwd slash %2F, space %20
    url_format_keywords = '%2C'.join(final_keywords)
    
    return url_format_keywords

def getting_data(keywords):
    jobs_list = []
    jobs_found = 0
    page = 1
    
    print(f"I LOOK FOR JOBS w {keywords}") #keywords.replace('%2C', ', ')
    
    while True:
        try:
            #GET UR URL/PAGE TO SCRAPE---------------------------------
            url = f'https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords={keywords}&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords={keywords}&pDate=I&sequence={page}&startPage=1'            #
            #https://www.linkedin.com/jobs/search-results/?keywords=analyst&start= EMPTY! 25! 50! 
            #https://www.indeed.com/jobs?q=analyst&l=Notre%20Dame%2C%20IN
            #https://www.usajobs.gov/search/results/?k=analyst

            print(f"Scraping page {page}...")
            response = requests.get(url, timeout=12)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            #maybe try a diff section of texT?

            ''' try and get TOTAl jobs from first page
            if page == 1:
                total_element = soup.find('span', id="totolResultCountsId")
                if total_element:
                    total = int(total_element.text.strip())
                    print(f"THIS MANY JOBS W KEYWORDS {total}")
                else:
                    print("Could not find total job count")
                    total = 0
            '''
            
            #SCRAPE ACTUAL JOBS -----------------------------------------------
            jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
            """ALSO TRY -- 
              <div class="d-flex d-flex-l-r d-flex-align-item">…</div>flex
            """

            if not jobs:
                print("no jobs")
                break
            
            jobs_found += len(jobs)
            print(f"so far we have found {jobs_found} jobs!")
            
            # Extract data from each job
            for job in jobs:
                try:

                    h2_tag = job.find('h2') #u already put all jobs in list based on class_='clearfix job-bx wht-shd-bx' so just find by tags within
                    if h2_tag:
                        name = h2_tag.text.strip() #i think u should strip everything bc ppl r using it for apps/analytics... #CHECK W SOMEONE ABT DATA CLEANLINESS IDRK 
                    else:
                        name = 'N/A'

                    company = job.find('h3', class_="joblist-comp-name").text.strip() if job.find('h3', class_="joblist-comp-name") else 'N/A'

                    #location = job.find('span').text.strip() if job.find('span') else 'N/A'

                    skills_div = job.find('div', class_="srp-skills")
                    if skills_div:
                        skills_span = skills_div.find_all("span")
                        skills = []
                        for skill in skills_span:
                            cleaned_skill = skill.text.strip()
                            skills.append(cleaned_skill)
                    else:
                        skills = 'N/A'

                    
                    #job.find('li', class_="job-description") if job.find("li") else "N/A"


                    #job.find('h3', class_= "joblist-comp-name" )
                    # Get job link

                    
                    job_data = {
                        'Position': name,
                        'Company': company,
                        #'Location': location,
                        'Skills': skills,
                    }
                    jobs_list.append(job_data)
                    
                except Exception as e:
                    print(f"{e}")
                    continue
                        
            page += 1  

        except Exception as e:
            print(f"Unexpected error on page {page}: {e}")
            break
    
    # Convert to DataFrame
    df = pd.DataFrame(jobs_list)
    return df

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
df = getting_data("Data Analyst")
print(df)
df.head(20)




def save_to_database(df, db_name='jobs.db', table_name='job_listings'):
    """Save DataFrame to SQLite database"""
    if df.empty:
        print("No data to save!")
        return
    
    try:
        # Connect to SQLite database (creates if doesn't exist)
        conn = sqlite3.connect(db_name)
        
        # Save DataFrame to database
        # if_exists='append' adds to existing data, use 'replace' to overwrite
        df.to_sql(table_name, conn, if_exists='append', index=False)
        
        print(f"\nSuccessfully saved {len(df)} jobs to database: {db_name}")
        print(f"Table name: {table_name}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error saving to database: {e}")

def save_to_excel(df, filename='jobs.xlsx'):
    """Optional: Also save to Excel file"""
    try:
        df.to_excel(filename, sheet_name='Job Listings', index=False)
        print(f"Data also saved to {filename}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

def view_database(db_name='jobs.db', table_name='job_listings'):
    """View the contents of the database"""
    try:
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        
        print(f"\nDatabase contains {len(df)} total jobs:")
        print(df.head(10))  # Show first 10 rows
        
    except Exception as e:
        print(f"Error reading database: {e}")

def main():
    print("=== Job Scraper ===\n")
    
    # Get keywords from user
    keywords = user_input()
    
    # Scrape job data
    df = getting_data(keywords)
    
    if not df.empty:
        # Save to database
        save_to_database(df)
        
        # Optionally save to Excel too
        save_to_excel(df)
        
        # View what's in the database
        view_database()
    else:
        print("No jobs were found. Try different keywords.")

if __name__ == '__main__':
    main()

print("Hello")