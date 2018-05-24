import pickle as pkl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# load previous page results, if any
try:
	results = pkl.load(open("results.pkl", "rb"))
except:
	results = []


# target metadata and selectors
target_course = "CAS BI 422"
target_url = "https://tes.collegesource.com/view/TES_view01.asp?aid={ADBAA968-6CE9-47A6-9B99-43D30CDD2D67}&rid={F3C0908C-8809-4592-A06A-2EC9C2C3ACC8}&pg=3&ac="
colleges_xpath = "//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"pageheader\", \" \" ))]//a"
# num_pages_xpath = "//*+[contains(concat( \" \", @class, \" \" ), concat( \" \", \"bodysmallbold\", \" \" ))]//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"bodysmallbold\", \" \" ))]"
num_pages_xpath = "//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"bodysmallbold\", \" \" ))]"
course_code_xpath = "//*[(@id = \"coursecode\")]"
# code_type_xpath = "//*[(@id = \"coursecodetype\")]"
code_type_xpath = ".//input[@type=\"radio\" and @value=\"2\"]"
course_match_xpath = "//td//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"bodysmall\", \" \" ))]//*[contains(concat( \" \", @class, \" \" ), concat( \" \", \"bodysmaller\", \" \" ))]"
college_state_xpath = "//font"


# init chrome driver
chromedriver_path = "/Users/karanraj/Downloads/chromedriver"
driver = webdriver.Chrome(chromedriver_path)
driver.get(target_url)

# num_pages = 32
# # scan colleges on all pages one by one
# for _ in range(num_pages-1):
# 	// *[contains(concat(" ", @
#
#
# 	class , " " ), concat( " ", "bodysmall", " " ))] // *[contains(concat( " ", @ class, " " ), concat( " ", "bodysmall", " " ))] // *[contains(concat( " ", @ class, " " ), concat( " ", "bodysmall", " " ))] // a

# all colleges in current page and their states
num_colleges = len(driver.find_elements_by_xpath(colleges_xpath))

for i in range(num_colleges):

	# get college metadata then go to the college courses page
	college = driver.find_elements_by_xpath(colleges_xpath)[i]
	college_name = college.text
	college_loc = driver.find_elements_by_xpath(college_state_xpath)[i].text
	college.send_keys(Keys.ENTER)

	# course code type - away, home, both. select home
	driver.find_element_by_xpath(code_type_xpath).click()

	# course code search box. enter target home course name
	search_box = driver.find_element_by_xpath(course_code_xpath)
	search_box.send_keys(target_course)
	search_box.send_keys(Keys.ENTER)

	# check if there are any matches
	is_match = driver.find_elements_by_xpath(course_match_xpath)

	if is_match:
		print("found a match")
		results.append({"name": college_name, "location": college_loc})

	# click back two times to get back to college list
	driver.back()
	driver.back()


# save data from current page search
pkl.dump(results, open("results.pkl", "wb"))


# exit
driver.close()
