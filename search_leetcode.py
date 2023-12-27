import json
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from datetime import datetime
import dataSheet

# Setup Selenium Webdriver
options = Options()
options.headless = True
# Disable Warning, Error and Info logs
# Show only fatal errors
options.add_argument("--log-level=3")
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

global ratio
ratio = 1.0


def getDifficulty():
    dt = datetime.now()
    day = dt.weekday()
    if (day == 0 or day == 1 or day ==2 or day ==3):
        return 1
    elif(day == 4 or day == 5):
        return 2
    else:
        return 3


def getDescriptionAndRatio(url):  
    # print(Fore.BLACK + Back.CYAN + f"Fetching problem num " + Back.YELLOW + f" {problem_num} " + Back.CYAN + " with url " + Back.YELLOW + f" {url} ")

    try:

        driver.get(url)

        # Wait 20 secs or until div with id initial-loading disappears
        element = WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.ID, "initial-loading"))
        )
        # Get current tab page source
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")
        button_html = soup.find_all(class_="btn__r7r7 css-1rdgofi")
        likes_html = button_html[0]
        dislikes_html = button_html[1]
        problem_description_html = soup.find(class_="content__u3I1 question-content__JfgR")

        likes = int(likes_html.get_text())
        dislikes = int(dislikes_html.get_text())
        ratio = likes/dislikes

        # get text
        text = problem_description_html.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text= '\n'.join(chunk for chunk in chunks if chunk)

        problem_description = ""
        for line in text.split("\n"):
            if ("Example" in line or "Constraints" in line):
                problem_description += "\n" + line + "\n"
            else:
                problem_description += line + "\n"
    
       
    except Exception as e:
        print(f" Failed Writing!!  {e} ")
        driver.quit()
    
    return problem_description, ratio



    


def getQuestionDeets():
    global ratio
    # Leetcode API URL to get json of problems on algorithms categories
    ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

    # Problem URL is of format ALGORITHMS_BASE_URL + question__title_slug
    # If question__title_slug = "two-sum" then URL is https://leetcode.com/problems/two-sum
    ALGORITHMS_BASE_URL = "https://leetcode.com/problems/"

    # Load JSON from API
    algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
    algorithms_problems_json = json.loads(algorithms_problems_json)



    # List to store question_title_slug
    links = []
    for child in algorithms_problems_json["stat_status_pairs"]:
            # Only process free problems
            if not child["paid_only"]:
                question__title_slug = child["stat"]["question__title_slug"]
                question__article__slug = child["stat"]["question__article__slug"]
                question__title = child["stat"]["question__title"]
                frontend_question_id = child["stat"]["frontend_question_id"]
                difficulty = child["difficulty"]["level"]
                links.append((question__title_slug, difficulty, frontend_question_id, question__title, question__article__slug))

    # Sorted by problem number
    links = sorted(links, key=lambda x: (x[2], x[1]))
    diff = {
        1: "Easy",
        2: "Medium",
        3: "Hard"
    }

    dt = datetime.now()
    date = dt.date()
    while True:
        num = random.randint(0, len(links)-1)
        if (links[num][1] == getDifficulty() and dataSheet.numberBeenUsed(links[num][2]) == False and getDescriptionAndRatio(ALGORITHMS_BASE_URL + links[num][0])[1] >= ratio):
            dataSheet.writeToDataSheet(int(links[num][2]), diff[links[num][1]], date)
            break

    

    question__title_slug, _ , frontend_question_id, question__title, question__article__slug = links[num]
    url = ALGORITHMS_BASE_URL + question__title_slug
    title = "**"+question__title+"**"


    question_description = getDescriptionAndRatio(url)[0]
    question_description = '```' + question_description + '```'


    
    return title, url, question_description