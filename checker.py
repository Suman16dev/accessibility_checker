import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def accessibility_check(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    issues = []

    # 1. <title> in <head>
    if not soup.title or not soup.title.text.strip():
        issues.append(["Missing or empty <title> tag in <head>."])

    # 2. lang attribute in <html>
    html_tag = soup.find('html')
    if html_tag and not html_tag.has_attr('lang'):
        issues.append(["Missing 'lang' attribute in the <html> tag."])

    # 3. <img> alt attribute
    for img in soup.find_all('img'):
        if not img.get('alt'):
            img_src = img.get('src', '')
            full_img_url = urljoin(base_url, img_src)
            issues.append([f"Image missing alt attribute: {full_img_url}, HTML: {str(img)}"])

    # 4. Form labels
    for input_tag in soup.find_all(['input', 'select', 'textarea']):
        label = None
        if input_tag.get('id'):
            label = soup.find('label', attrs={'for': input_tag['id']})
        if not label:
            issues.append([f"Form element missing label: {str(input_tag)}..."])

    # 5. Skipped heading order
    heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    last_level = 0
    for h in soup.find_all(heading_tags):
        level = int(h.name[1])
        if level - last_level > 1:
            issues.append([f"Skipped heading level from h{last_level} to h{level}"])
        last_level = level

    # 6. ARIA attributes check
    for tag in soup.find_all(True):
        for attr in tag.attrs.keys():
            if attr.startswith('aria-') and not tag.get(attr):
                issues.append([f"{tag.name} missing value or has empty ARIA attribute '{attr}'"])
        # Warn if interactive elements lack appropriate ARIA roles
        if tag.name in ['nav', 'main', 'aside', 'header', 'footer']:
            if not tag.get('role'):
                issues.append([f"{tag.name} tag missing 'role' attribute (consider roles for assistive tech)"])

    # 7. Tabindex and tab order
    tab_tags = soup.find_all(attrs={'tabindex': True})
    tab_indices = [int(tag.get('tabindex', 0)) for tag in tab_tags if tag.get('tabindex', '').isdigit()]
    if tab_indices and sorted(tab_indices) != tab_indices:
        issues.append(["Tabindex values are not in logical/tab order sequence."])

    # 8. Empty roles
    for tag in soup.find_all(attrs={"role": True}):
        if not tag['role'].strip():
            issues.append([f"{tag.name} tag has empty 'role' attribute."])

    # 9. Example: Suggest using ARIA landmarks
    roles_needed = {'banner', 'main', 'navigation', 'contentinfo'}
    roles_present = {tag.get('role') for tag in soup.find_all(attrs={'role': True})}
    for req_role in roles_needed:
        if req_role not in roles_present:
            issues.append([f"Suggested: Consider landmark role '{req_role}' for layout structure."])

    return issues

def check_url_and_generate_csv(url, csv_filename="accessibility_report.csv"):
    response = requests.get(url)
    if response.status_code == 200:
        issues = accessibility_check(response.text, url)
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Issue"])
            for issue in issues:
                writer.writerow(issue)
        print(f"Accessibility issues saved to {csv_filename}")
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")

# Example usage:
website_url = "https://weaversweb.com/"  # Replace with your target URL
check_url_and_generate_csv(website_url, "report.csv")