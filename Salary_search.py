from selenium import webdriver
from password import fb_password,fb_username
from time import sleep
from bs4 import BeautifulSoup
import csv
import re

driver = webdriver.Firefox()

#open glassdoor
driver.get('https://glassdoor.com')

#login
sleep(2)
driver.find_element_by_id('FbButton').click()
driver.switch_to.window(driver.window_handles[1])
sleep(2)
driver.find_element_by_id('email').send_keys(fb_username)
driver.find_element_by_id('pass').send_keys(fb_password)
driver.find_element_by_id('loginbutton').click()
driver.switch_to.window(driver.window_handles[0])
sleep(10)

job_company = []
job_role = []
with open('BLC.csv','r') as csv_read:
    csv_reader = csv.reader(csv_read)
    for row in csv_reader:
        job_company.append(row[1])
        job_role.append(row[2])
    #search

    with open('BLC2.csv','a',newline='') as csv_write:
        csv_writer = csv.writer(csv_write)
        csv_writer.writerow(['Sno','Company','Role','Salary'])
        driver.find_element_by_xpath('/html/body/header/nav[1]/div/div/div/div[4]/div[3]/form/div/div[2]/div').click()
        driver.find_element_by_xpath(
            '/html/body/header/nav[1]/div/div/div/div[4]/div[3]/form/div/div[2]/div/div[2]/div/ul/li[2]/span').click()
        driver.find_element_by_id('sc.location').clear()
        driver.find_element_by_id('sc.location').send_keys('India')
        for i in range(1,len(job_company)):
            sleep(2)
            driver.find_element_by_id('sc.keyword').clear()
            driver.find_element_by_id('sc.keyword').send_keys(job_company[i+1])
            driver.find_element_by_xpath('/html/body/header/nav[1]/div/div/div/div[4]/div[3]/form/div/button').click()

            #navigate to company
            sleep(3)
            try:
                try:
                    try:
                        driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/div[2]/div[1]/div[2]/div[1]/a').click()
                        sleep(2)
                    except:
                        driver.find_element_by_xpath('//*[@id="MainCol"]/div/div[1]/div/div[1]/div/div[2]/h2/a').click()
                        sleep(2)
                except:
                    pass

                #click salaries&search
                try:
                    try:
                        driver.find_element_by_css_selector('a.eiCell:nth-child(7)').click()
                        sleep(2)
                        driver.find_element_by_id('filter.jobTitleFTS-JobTitleAC').send_keys(job_role[i+1])
                        driver.find_element_by_css_selector('button.gd-ui-button:nth-child(1)').click()
                        #extract
                        sleep(3)
                        src = driver.page_source
                        GD_soup = BeautifulSoup(src, 'lxml')
                        Sal_div = GD_soup.find('div',{'id':'SalariesRef'}).find_all('div')[8]
                        salary = Sal_div.find_all('strong')[0].get_text().strip()
                        flag = 2
                        print('good')
                    except:
                        driver.find_element_by_css_selector('a.eiCell:nth-child(7)').click()
                        sleep(2)
                        driver.find_element_by_id('filter.jobTitleFTS-JobTitleAC').send_keys(job_role[i+1].split()[0])
                        driver.find_element_by_css_selector('button.gd-ui-button:nth-child(1)').click()
                        # extract
                        sleep(3)
                        src = driver.page_source
                        GD_soup = BeautifulSoup(src, 'lxml')
                        Sal_div = GD_soup.find('div',{'id':'SalariesRef'}).find_all('div')[8]
                        salary = Sal_div.find_all('strong')[0].get_text().strip()
                        flag = 1
                except:
                    try:
                        driver.find_element_by_css_selector('a.eiCell:nth-child(7)').click()
                        sleep(2)
                        driver.find_element_by_id('filter.jobTitleFTS-JobTitleAC').send_keys("Blockchain")
                        driver.find_element_by_css_selector('button.gd-ui-button:nth-child(1)').click()
                        # extract
                        sleep(3)
                        src = driver.page_source
                        GD_soup = BeautifulSoup(src, 'lxml')
                        Sal_div = GD_soup.find('div',{'id':'SalariesRef'}).find_all('div')[8]
                        salary = Sal_div.find_all('strong')[0].get_text().strip()
                        flag = 0
                    except:
                        driver.find_element_by_css_selector('a.eiCell:nth-child(7)').click()
                        sleep(2)
                        driver.find_element_by_id('filter.jobTitleFTS-JobTitleAC').send_keys("Software")
                        driver.find_element_by_css_selector('button.gd-ui-button:nth-child(1)').click()
                        # extract
                        sleep(3)
                        src = driver.page_source
                        GD_soup = BeautifulSoup(src, 'lxml')
                        Sal_div = GD_soup.find('div',{'id':'SalariesRef'}).find_all('div')[8]
                        salary = Sal_div.find_all('strong')[0].get_text().strip()
                        flag = 0


                print(salary)
                #salary processing

                if 'K' in salary:
                    salary.replace('K','000')
                if 'M' in salary:
                    salary.replace('M','000000')
                if '-' in salary:
                    salary.split('-')
                    salary = (int("".join(re.findall(r'\d+',salary[0])))+int("".join(re.findall(r'\d+',salary[1]))))/2
                else:
                    salary = re.findall(r'\d+',salary)
                    salary = "".join(salary)
                    salary = int(salary)/100000
                    if salary < 2:
                        salary = salary * 12
            except:
                flag = -1
                salary = ''


            print(i)
            print(job_role[i+1])
            print(job_company[i+1])
            print(salary)
            print(flag)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            job_details = [str(i), job_company[i+1], job_role[i+1], str(salary), flag]
            csv_writer.writerow(job_details)






