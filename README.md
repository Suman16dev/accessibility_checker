Accessibility Checker
A simple web app to check website accessibility issues and generate CSV reports, supporting both direct URL entry and sitemap.xml upload. Built with Python, Flask, and BeautifulSoup.

Features
Enter a website URL or sitemap.xml link OR upload a sitemap.xml file.

Checks multiple accessibility rules page-by-page:

Missing <title> or <html lang="">

Images missing alt attributes (with full image URLs)

Form elements missing labels (with full HTML)

Heading level skips

ARIA attributes, roles, and tab order

Generates a downloadable CSV report.

Modern, clean web interface.

Simple to run with a batch file.

Getting Started
Prerequisites
Python 3.7+

Pip (Python package manager)

Chrome browser (optional, if using Selenium for screenshots)

Installation
Clone or download this repo

Install dependencies:

bash
pip install flask beautifulsoup4 lxml requests
Project structure:

text
accessibility_checker/
├── app.py
├── checker.py
├── templates/
│   └── index.html
├── run_web.bat
└── README.md
Usage
Open a terminal or double-click run_web.bat (if provided):

bash
python app.py
This will launch the web server and open your default browser to http://localhost:5000.

On the web page:

Enter a website URL or sitemap.xml link

or upload a sitemap.xml file

Click Check Accessibility

Wait for processing (progress bar coming soon!)

Download your CSV report

Batch File (optional)
If you want to run the app with one click, use the following batch file:

run_web.bat:

text
@echo off
python app.py
pause
Troubleshooting
FeatureNotFound (xml parser):

Install lxml: pip install lxml

requests not defined:

Ensure import requests is at the top of any module that uses it.

accessibility_check not defined:

Make sure to import your function from checker.py into app.py.

Customization
Change or extend accessibility checks in checker.py.

Style your interface by editing templates/index.html.
