import time
import argparse
import pickle as pkl
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
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
        default='https://ugadmissions.northeastern.edu/transfercredit/TransferCreditEvaluatedStudent2.asp',
        type=str,
        required=False,
        help="URL which has the list of colleges, i.e. the first page from where the scraping should begin",
    )
    parser.add_argument(
        '--nupath-names',
        default=['NUpath Difference/Diversity', 'NUpath Interpreting Culture'],
        type=str,
        nargs='+',
        required=False,
        help="NUPath name(s) which is to be satisfied. CASE SENSITIVE",
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
PROCEED_BTN_XP = '//*[(@id = "button1")]'
INSTITUTES_DRPDWN_XP = '//*[(@id = "FICE")]'
DEPARTMENT_DRPDWN_XP = '//*[(@id = "tseg")]'
NUPATH_CSS_SEL = 'tr+ tr td:nth-child(5)'
NUCORE_CSS_SEL = 'tr+ tr td:nth-child(4)'
EFF_DATE_CSS_SEL = 'tr+ tr td:nth-child(3)'
HOME_COURSE_CSS_SEL = 'table+ table tr+ tr td:nth-child(2)'
AWAY_COURSE_CSS_SEL = 'table+ table tr+ tr td:nth-child(1)'

# init chrome driver
driver = webdriver.Chrome(args.chromedriver_path)
driver.get(args.start_url)

# click on proceed to rules search
driver.find_element_by_xpath(PROCEED_BTN_XP).click()

# get a list of available colleges
colleges_dropdown = driver.find_element_by_xpath(INSTITUTES_DRPDWN_XP)
college_dropdown_opts = colleges_dropdown.find_elements_by_tag_name("option")
college_names = []
for c in tqdm(college_dropdown_opts):
    college_names.append(c.text)
    
# with open('college_names.pkl', 'wb') as f:
#     pkl.dump(college_names, f)
# with open('../college_names.pkl', 'rb') as f:
#     college_names = pkl.load(f)

# list of dictionaries, each dictionary contains details of a match
results = []

# iterate through all colleges and see if NUPath contains *all* of the matching paths
# NOTE: skip the first one since its an empty string
for ci in range(1, len(college_names)):
    colleges_dropdown = Select(driver.find_element_by_xpath(INSTITUTES_DRPDWN_XP))
    
    # click on college
    colleges_dropdown.select_by_index(ci)

    # get all departmets in this college
    departments = [
        i.text for i in driver.find_element_by_xpath(DEPARTMENT_DRPDWN_XP).find_elements_by_tag_name("option")
    ]
    
    # iterate through all departments
    # NOTE: skip the first one since its an empty string
    for di in range(1, len(departments)):
        # get the list of courses in this department
        departments_dropdown = Select(driver.find_element_by_xpath(DEPARTMENT_DRPDWN_XP))
        departments_dropdown.select_by_index(di)

        # see if any course matches the conditons
        courses_nupaths = driver.find_elements_by_css_selector(NUPATH_CSS_SEL)
        if len(courses_nupaths) > 0:
            # get other course metadata
            courses_away_names = driver.find_elements_by_css_selector(AWAY_COURSE_CSS_SEL)
            courses_home_names = driver.find_elements_by_css_selector(HOME_COURSE_CSS_SEL)
            courses_effective_dates = driver.find_elements_by_css_selector(EFF_DATE_CSS_SEL)
            courses_nu_cores = driver.find_elements_by_css_selector(NUCORE_CSS_SEL)
            for course_i, course_nupath in enumerate(courses_nupaths):
                if all(to_match in course_nupath.text for to_match in args.nupath_names):
                    # add coures name, neu name, effective dates, nucore
                    results.append(
                        {
                            'college': college_names[ci],
                            'department': departments[di],
                            'transfer_course': courses_away_names[course_i].text,
                            'neu_course': courses_home_names[course_i].text,
                            'effective_dates': courses_effective_dates[course_i].text,
                            'nu_core': courses_nu_cores[course_i].text,
                            'nupath': course_nupath.text,
                        }
                    )

    # save data every iteration, in case it gets stopped in the middle
    with open(args.save_fname, "wb") as f:
        pkl.dump(results, f)

# exit
driver.close()
