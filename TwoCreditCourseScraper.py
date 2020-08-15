import pickle as pkl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

filename = "twocred.pkl"

# load previous page results, if any
try:
    results = pkl.load(open(filename, "rb"))
except:
    results = []


# target metadata and selectors
target_course = "CAS CH 422"
start_url = "https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1527269926?College=CAS&Dept=&Course=&Section=&ModuleName=reg%2Fadd%2Fbrowse_schedule.pl&AddPreregInd=&AddPlannerInd=Y&ViewSem=Fall+2018&KeySem=20193&PreregViewSem=&PreregKeySem=&SearchOptionCd=S&SearchOptionDesc=Class+Number&MainCampusInd=&BrowseContinueInd=&ShoppingCartInd=&ShoppingCartList="
next_page_xpath = "//input[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]"
credits_xpath = "//td[(((count(preceding-sibling::*) + 1) = 7) and parent::*)]"
courses_xpath = "//td[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]//a"

colleges_xpath = "//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"pageheader\", \" \" ))]//a"
course_code_xpath = "//*[(@id = \"coursecode\")]"
code_type_xpath = ".//input[@type=\"radio\" and @value=\"2\"]"
course_match_xpath = "//td//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"bodysmall\", \" \" ))]//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"bodysmaller\", \" \" ))]"
college_state_xpath = "//font"


# init chrome driver
chromedriver_path = "/Users/karanraj/Downloads/chromedriver"
driver = webdriver.Chrome(chromedriver_path)
driver.get(start_url)


# number of pages of list of colleges
num_pages = 1000

# scan colleges on all pages one by one
for _ in range(num_pages-1):

    # courses on current page
    curr_page_courses = driver.find_elements_by_xpath(courses_xpath)

    # credits for courses on current page
    curr_page_credits = driver.find_elements_by_xpath(credits_xpath)

    # check for matches
    for i in range(len(curr_page_credits)):
        print(curr_page_credits[i].text)
        if curr_page_credits[i].text == "2.0":
            results.append(curr_page_courses[i].text)
            print(curr_page_courses[i].text)

    # go to next page
    driver.find_elements_by_xpath(next_page_xpath)[-1].click()

# save data from current search
pkl.dump(results, open(filename, "wb"))

# exit
driver.close()
