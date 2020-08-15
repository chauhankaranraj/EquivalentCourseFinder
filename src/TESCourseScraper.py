import time
import argparse
import pickle as pkl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


def parse_scrape_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--chromedriver-path',
        default='/home/kachau/Downloads/chromedriver',
        type=str,
        required=False,
        help="path to chromedriver for selenium",
    )
    parser.add_argument(
        '--start-url',
        default='https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=f3c0908c-8809-4592-a06a-2ec9c2c3acc8&aid=adbaa968-6ce9-47a6-9b99-43d30cdd2d67',
        type=str,
        required=False,
        help="URL which has the list of colleges, i.e. the first page from where the scraping should begin",
    )
    parser.add_argument(
        '--target-course',
        default='QST AC 1**',
        type=str,
        required=False,
        help="BU course name for which equivalent courses are to be searched, or external college course name for which equivalent BU courses are to be search",
    )
    parser.add_argument(
        '--course-type',
        default='home',
        type=str,
        required=False,
        choices=['home', 'away', 'both'],
        help="Specify whether target course provided as input is BU course or external college course or search for both",
    )
    parser.add_argument(
        '--effective-date',
        default='both',
        type=str,
        required=False,
        choices=['active', 'inactive', 'both'],
        help="Specify whether results should be for active courses, inactive courses or both",
    )
    parser.add_argument(
        '--num-pages',
        default=10,
        type=int,
        required=False,
        help="Number of pages to scrape, one page being the `list of colleges` page",
    )
    parser.add_argument(
        '--save-fname',
        default=f'../reports/results_{time.time()}.pkl',
        type=str,
        required=False,
        help='Path + filename where results pickle should be stored',
    )

    return parser.parse_args()

# get args
args = parse_scrape_args()

# xpaths for various elements on the page to be scraped
# NOTE: these can be easily obtained using google chrome plugins
COLLEGES_XP = '//a[contains(concat( " ", @class, " " ), concat( " ", "gdv_boundfield_uppercase", " " ))]'
SEARCH_POPUP_BUTTON_XP = '//*[(@id = "btnSearchEQ")]'
SEARCH_POPUP_TEXTBOX_XP = '//*[(@id = "tbxCourseCode")]'
SEARCH_POPUP_EFF_DATE_ACTIVE_XP = '//*[(@id = "rblEffectiveDate_0")]'
SEARCH_POPUP_EFF_DATE_INACTIVE_XP = '//*[(@id = "rblEffectiveDate_1")]'
SEARCH_POPUP_EFF_DATE_BOTH_XP = '//*[(@id = "rblEffectiveDate_2")]'
SEARCH_POPUP_COURSETYPE_AWAY_XP = '//*[(@id = "rblCourseCodeType_0")]'
SEARCH_POPUP_COURSETYPE_HOME_XP = '//*[(@id = "rblCourseCodeType_1")]'
SEARCH_POPUP_COURSETYPE_BOTH_XP = '//*[(@id = "rblCourseCodeType_2")]'
SEARCH_POPUP_SEARCH_BUTTON_XP = '//*[(@id = "btnCourseEQSearch")]'
SEARCH_MATCHES_XP = '//*[contains(concat( " ", @class, " " ), concat( " ", "gdv_boundfield_uppercase", " " )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]'
get_page_css_selector = lambda x: f'.pagination-tes td:nth-child({x}) a'

# init chrome driver
driver = webdriver.Chrome(args.chromedriver_path)
driver.get(args.start_url)

# list of dictionaries, each dictionary contains details of a match
results = []

# scan colleges on all pages one by one
for page_num in range(args.num_pages-1):
    # go the the current page number
    if page_num > 0:
        driver.find_element_by_css_selector(get_page_css_selector(page_num+1)).click()

    # total colleges on the current page
    num_colleges = len(driver.find_elements_by_xpath(COLLEGES_XP))

    # iterate through each college on current page
    # NOTE: we'll have to find element every time, since elements seem to become "stale"
    # so we can't find all beforehand and then iterate through them
    for college_num in range(num_colleges):
        # status bar
        print('{:2d} / {:2d} college on page {:2d}'.format(college_num + 1, num_colleges, page_num + 1), end='\r')

        # get college link and name for current college
        college = driver.find_elements_by_xpath(COLLEGES_XP)[college_num]
        college_name = college.text

        # open the page linked for that college
        college.send_keys(Keys.ENTER)

        # click search button to open search popup tool
        search_box = driver.find_element_by_xpath(SEARCH_POPUP_BUTTON_XP)
        search_box.send_keys(Keys.ENTER)

        # wait until elements xpath is visible then enter course name
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, SEARCH_POPUP_TEXTBOX_XP)))
        search_textbox_input = driver.find_element_by_xpath(SEARCH_POPUP_TEXTBOX_XP)
        search_textbox_input.send_keys(args.target_course)    

        # set effective date according to input
        if args.effective_date == 'active':
            search_course_effective_date = driver.find_element_by_xpath(SEARCH_POPUP_EFF_DATE_ACTIVE_XP)
        elif args.effective_date == 'inactive':
            search_course_effective_date = driver.find_element_by_xpath(SEARCH_POPUP_EFF_DATE_INACTIVE_XP)
        elif args.effective_date == 'both':
            search_course_effective_date = driver.find_element_by_xpath(SEARCH_POPUP_EFF_DATE_BOTH_XP)
        search_course_effective_date.send_keys(Keys.ENTER)
        search_course_effective_date.send_keys(Keys.SPACE)

        # set search settings to search for "home" or  "away" or both
        if args.course_type == 'home':
            search_course_type = driver.find_element_by_xpath(SEARCH_POPUP_COURSETYPE_HOME_XP)
        elif args.course_type == 'away':
            search_course_type = driver.find_element_by_xpath(SEARCH_POPUP_COURSETYPE_AWAY_XP)
        elif args.course_type == 'both':
            search_course_type = driver.find_element_by_xpath(SEARCH_POPUP_COURSETYPE_BOTH_XP)
        # search_course_type = driver.find_element_by_xpath('//*[(@id = "rblCourseCodeType_1")]')
        search_course_type.send_keys(Keys.ENTER)
        search_course_type.send_keys(Keys.SPACE)

        # course code search box. enter target home course name
        search_button = driver.find_element_by_xpath(SEARCH_POPUP_SEARCH_BUTTON_XP)
        search_button.send_keys(Keys.ENTER)

        # get all matches
        matches = driver.find_elements_by_xpath(SEARCH_MATCHES_XP)
        for m in matches:
            results.append(
                {
                    'college_name': college_name,
                    'course_name': m.text
                }
            )

        # click back to get back to college list
        driver.back()

# save data from current search
with open(args.save_fname, "wb") as f:
    pkl.dump(results, f)

# exit
driver.close()
