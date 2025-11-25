from flask import Flask, request, render_template, send_file
from bs4 import BeautifulSoup
import csv, os
import requests
from checker import accessibility_check

app = Flask(__name__)
REPORT_FILE = "report.csv"

def get_links_from_sitemap_xml(xml_content):
    soup = BeautifulSoup(xml_content, 'xml')
    return [loc.text.strip() for loc in soup.find_all('loc')]

@app.route('/', methods=['GET', 'POST'])
def home():
    csv_ready = False
    if request.method == 'POST':
        links = []
        # If a file is uploaded, use it
        if 'sitemap_file' in request.files and request.files['sitemap_file'].filename:
            uploaded_file = request.files['sitemap_file']
            xml_content = uploaded_file.read()
            links = get_links_from_sitemap_xml(xml_content)
        else:
            url = request.form['url'].strip()
            if url:
                if url.endswith('.xml'):
                    res = requests.get(url)
                    links = get_links_from_sitemap_xml(res.text)
                else:
                    links = [url]

        with open(REPORT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Issue"])
            for page_url in links:
                try:
                    resp = requests.get(page_url, timeout=10)
                    # Use your accessibility_check function here!
                    issues = accessibility_check(resp.text, page_url)
                    for issue in issues:
                        writer.writerow([page_url] + issue)
                except Exception as e:
                    writer.writerow([page_url, f"Fetch Error: {e}"])
        csv_ready = True
    return render_template('index.html', csv_ready=csv_ready)

@app.route('/download')
def download():
    return send_file(REPORT_FILE, as_attachment=True)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://localhost:5000')
    app.run(debug=True)
