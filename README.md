# Equivalent Course Finder

This repo contains python scripts to scrape some web pages at Boston University. The reason this was created was to help find courses at external colleges that satisfy requirements at Boston University. That is, if you're a student trying to find out which courses are available at external colleges, that could give you credits for a specific course (e.g. `CAS WR 150`) at BU, then instead of clicking and search through 100's of colleges manually ([page](https://www.bu.edu/reg/students/transfer-equivalency/), [page](https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=f3c0908c-8809-4592-a06a-2ec9c2c3acc8&aid=adbaa968-6ce9-47a6-9b99-43d30cdd2d67)), use this one python script instead.

Of course, this problem could have been solved by having a better website, but that doesn't seem to have happened in >2 years. I have recently found other people would find this script helpful, so I'm open sourcing it.

## Installation

1. Download `chromedriver` from their [downloads](https://chromedriver.chromium.org/downloads) page.
2. Clone this repo
    ```
    git clone https://github.com/chauhankaranraj/EquivalentCourseFinder.git
    ```
**NOTE** The next two steps are more of personal preferences, feel free to use `conda` or something else in place of `pipenv` if you so prefer.

3. Install `pipenv`, if you don't have it already
    ```
    pip3 install pipenv
    ```
3. Change directory to where you cloned this repo. And then setup the virtual environent using `pipenv`.
    ```
    cd path/to/where/you/cloned/EquivalentCourseFinder
    pipenv shell
    pipenv install
    ```

## Usage
Example: I want to find courses at external colleges that can satisfy my `CAS WR 150` requirements at BU.
```
pipenv shell
cd src
python TESCourseScraper.py --target-course CAS\ WR\ 150 --chromedriver-path /home/kachau/Downloads/chromedriver
```

To see what other arguments you can pass to the script, run
```
python TESCourseScraper.py --help
```
```
  --chromedriver-path CHROMEDRIVER_PATH
                        path to chromedriver for selenium
  --start-url START_URL
                        URL which has the list of colleges, i.e. the first
                        page from where the scraping should begin
  --target-course TARGET_COURSE
                        BU course name for which equivalent courses are to be
                        searched, or external college course name for which
                        equivalent BU courses are to be search
  --course-type {home,away,both}
                        Specify whether target course provided as input is BU
                        course or external college course or search for both
  --effective-date {active,inactive,both}
                        Specify whether results should be for active courses,
                        inactive courses or both
  --num-pages NUM_PAGES
                        Number of pages to scrape, one page being the `list of
                        colleges` page
  --save-fname SAVE_FNAME
                        Path + filename where results pickle should be stored

```