# import pprint
#
# import selenium.common.exceptions
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from random import randint
# from math import ceil
# from time import sleep
#
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("headless")
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15")
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.get("https://cz.indeed.com/jobs?q=&l=Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha&rbl=Praha&jlid=316ca9ce842785a8&fromage=14&lang=en&vjk=e1a02caeeabb8b7f")
# driver.maximize_window()
# url_template = "https://cz.indeed.com/jobs?q=&l=Praha%2C+Hlavn%C3%AD+m%C4%9Bsto+Praha&rbl=Praha&jlid=316ca9ce842785a8&fromage=14&lang=en&vjk=e1a02caeeabb8b7f"+"&start={offset}"
#
# def get_page_count(url):
#     driver.get(url)
#     products_count = driver.find_elements(by=By.CSS_SELECTOR, value=".jobsearch-JobCountAndSortPane-jobCount > span:nth-child(1)")[0].text
#     products_count = products_count.replace("Nabídky práce: ", "").replace(",", "")
#     products_count = int(products_count)
#
#     return ceil(products_count / 15) if ceil(products_count / 15) <= 66 else 66
#
# def search_all(url):
#     driver.get(url)
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-ResultsList .cardOutline"))
#     )
#
#
#     click = "document.querySelector('#onetrust-accept-btn-handler')?.click()"
#     driver.execute_script(click)
#
#     click = "document.querySelector('.icl-CloseButton')?.click()"
#     driver.execute_script(click)
#
#     cards = driver.find_elements(by=By.CSS_SELECTOR, value=".jobsearch-ResultsList .cardOutline")
#     links_to_click = driver.find_elements(by=By.CSS_SELECTOR, value=".jobsearch-ResultsList .cardOutline .resultContent")
#     action = ActionChains(driver)
#     for i in range(len(cards)):
#         card = cards[i]
#         link = links_to_click[i]
#         action.move_to_element(card).click(link).perform()
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-JobInfoHeader-title-container span"))
#         )
#         sleep(randint(1, 3))
#         posted_days_ago = "".join(filter(str.isdigit,driver.find_element(by=By.CSS_SELECTOR, value=".date").text))
#
#         name = driver.find_elements(by=By.CSS_SELECTOR, value=".jobsearch-JobInfoHeader-title-container span")
#         description = driver.find_elements(by=By.CSS_SELECTOR, value=".jobsearch-jobDescriptionText")
#         link_element = driver.find_elements(by=By.CSS_SELECTOR, value=".jobsearch-CompanyInfoContainer a")
#         location = driver.find_elements(by=By.CSS_SELECTOR, value=".jobsearch-JobInfoHeader-subtitle>div:nth-child(2)")
#         link = ""
#         link_name = ""
#         job_type = ""
#         try:
#             logo = driver.find_element(by=By.CSS_SELECTOR, value=".jobsearch-HeaderContainer")
#             logo.click()
#             image = driver.find_element(by=By.CSS_SELECTOR, value=".jobsearch-JobInfoHeader-logo").get_attribute("src")
#         except:
#             image = "https://cdn-icons-png.flaticon.com/512/306/306424.png"
#
#         if not isinstance(posted_days_ago, int):
#             posted_days_ago = randint(1, 4)
#
#
#
#         if name:
#             name = name[0].text.split("\n")[0]
#         else:
#             name = ""
#
#         if description:
#             description = description[0].get_attribute('innerHTML')
#         else:
#             description = ""
#
#         if location:
#             location = location[0].text
#         else:
#             location = "Prague"
#         if link_element:
#             link = link_element[0].get_attribute("href")
#             link_name = link_element[0].text
#         try:
#             job_type_list = ["Plný úvazek","Částečný úvazek","Trvalý","Praxe","Smlouva","Dočasný úvazek"]
#
#             job_type_ele = driver.find_element(by=By.CSS_SELECTOR, value=".attribute_snippet").text
#
#             for i in job_type_list:
#                 if job_type_ele in i:
#                     job_type = i
#                 else:
#                     job_type = "No job type"
#         except selenium.common.exceptions.NoSuchElementException:
#             job_type = "No job type"
#
#
#
#
#
#         if location is None:
#             location = "Prague"
#
#         if image is None:
#             image = "https://cdn-icons-png.flaticon.com/512/306/306424.png"
#
#
#         entity = {
#             "name": name,
#             "link": link,
#             "company_name": link_name,
#             "job_type": job_type,
#             "location": location,
#             "description": description,
#             "logo": image,
#             "post_days_ago": int(posted_days_ago)
#         }
#
#         return entity
#
#
# def get_jobs():
#     jobs = []
#     page_id = 0
#
#
#     page_count = get_page_count(url_template.replace("{offset}", "0"))
#     for k in range(30):
#         url = url_template.replace("{offset}", str(page_id))
#         jobs.append(search_all(url))
#         sleep(2)
#         page_id += 10
#         sleep(3)
#     return jobs
#
#
