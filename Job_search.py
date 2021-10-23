from selenium import webdriver
from password import username, password
from time import sleep
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process

import csv
import re
from keywords import prog_languages, prog_languages_count

with open('BLC.csv', 'a', newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(
        ['S_no', 'job_company', 'job_role', 'job_level', 'job_experience_min', 'job_experience_max', 'job_industry',
         'job_functions', 'job_skills'])

    count_keywords = [0] * len(prog_languages)
    job_details = []
    job_id = 0
    S_no = 1
    page = 1
    num_jobs = 194
    count_keywords = prog_languages_count
    driver = webdriver.Firefox()

    # open linkedin
    driver.get('https://www.linkedin.com/uas/login')
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_xpath('/html/body/div/main/div[2]/form/div[3]/button').click()

    # job search
    sleep(2)
    keyword = "Back end developer"
    driver.get('https://www.linkedin.com/jobs/search/?f_E=2%2C3%2C4%2C5%2C6&f_JT=F&f_TPR=r604800&keywords=' + keyword)
    sleep(2)

    # navigate to job
    while S_no < num_jobs:
        #change page
        if job_id and job_id % 25 == 0:
            page = job_id
            driver.get(
                'https://www.linkedin.com/jobs/search/?f_E=2%2C3%2C4%2C5%2C6&f_JT=F&f_TPR=r604800&keywords=' + keyword + '&start=' + str(
                    page))
            sleep(2)
        sleep(2)

        #click job ad
        try:
            try:
                element = driver.find_element_by_xpath(
                    '/html/body/div[8]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[' + str(
                        job_id % 25 + 1) + ']/div').click()
                ''
            except:
                element = driver.find_element_by_xpath(
                    '/html/body/div[7]/div[3]/div[3]/div/div/section[1]/div/div/ul/li[' + str(
                        job_id % 25 + 1) + ']/div').click()


        #if the element clicks the company name instead (1/200 chance)
        except:
            print("Some error")

        sleep(2)
        # get details
        try:
            src = driver.page_source
            soup = BeautifulSoup(src, 'lxml')

            #get job details
            job_role = soup.find("h2",
                                 {'class': 'jobs-details-top-card__job-title t-20 t-black t-normal'}).get_text().strip()
            job_company = soup.find("a", {
                'class': 'jobs-details-top-card__company-url t-black--light t-normal ember-view'}).get_text().strip()
            try:
                job_level = soup.find_all("span", {'class': 'jobs-details-job-summary__text--ellipsis'})[
                    1].get_text().strip()
            except:
                job_level = "NA"
            try:
                job_industry = soup.find_all("span", {'class': 'jobs-details-job-summary__text--ellipsis'})[
                    3].get_text().strip()
            except:
                job_industry = "NA"
            try:
                job_functions = soup.find("ul", {
                    'class': 'jobs-box__list jobs-description-details__list js-formatted-job-functions-list'}).get_text()
                if '\n' in job_functions:
                    job_functions = job_functions.split('\n')
                    job_functions = ",".join(job_functions)
                    job_functions = re.sub(' +', ' ', job_functions)
                    job_functions = re.sub(',+', '', job_functions)
                    job_functions = job_functions.split('  ')
                job_functions = " ".join(job_functions)
            except:
                job_functions = "NA"

            #get job description
            job_description = soup.find('div', {'id': 'job-details'}).get_text().strip()
            job_skills = []

            #search for keywords
            for i in range(len(prog_languages)):
                if i == 2:
                    if prog_languages[i]+ ' ' in job_description:
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
                    elif prog_languages[i] + '.' in job_description:
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
                    elif prog_languages[i] + ',' in job_description:
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
                    elif prog_languages[i] + '/' in job_description:
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
                else:
                    if prog_languages[i].lower() + ' ' in job_description.lower():
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
                    elif prog_languages[i].lower() + '.' in job_description.lower():
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
                    elif prog_languages[i].lower() + ',' in job_description.lower():
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
                    elif prog_languages[i].lower() + '/' in job_description.lower():
                        count_keywords[i] += 1
                        job_skills.append(prog_languages[i])
            job_skills = " ".join(job_skills)

            #get experience : Search for numbers in sentences in the job description, where both "years" and "experience" strings are present
            temp_sentences = re.split(r' *[\.\?!][\'"\)\]]* *', job_description)
            job_experience = re.findall(r'\d+', process.extractOne("years experience", temp_sentences,
                                                                   scorer=fuzz.token_set_ratio)[0])
            job_experience_min = 'NA'
            job_experience_max = 'NA'
            try:
                if isinstance(job_experience, list):
                    job_experience_min = "".join(job_experience[0])
                    job_experience_max = "".join(job_experience[1])
                elif job_experience == []:
                    pass
                else:
                    job_experience_min = "".join(job_experience)
            except:
                try:
                    job_experience_min = "".join(job_experience)
                except:
                    pass

            job_details = [S_no, job_company, job_role, job_level, job_experience_min, job_experience_max, job_industry,
                           job_functions, job_skills]
            #write to CSV file
            thewriter.writerow(job_details)

            print(S_no)
            print(job_company)
            print(job_role)
            print(job_experience)
            print(count_keywords)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            S_no = S_no + 1
        #if company name, job role not present; skip job
        except:
            print(job_id)
            print("Passed")

            pass
        job_id += 1
    thewriter.writerow([" "])

    #keywords & count of keywords occur in the end
    thewriter.writerow(prog_languages)
    thewriter.writerow(count_keywords)
