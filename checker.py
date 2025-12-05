import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


def accessibility_check(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    print("HAS MAIN:", bool(soup.find("main")))
    print("HAS ROLE=MAIN:", bool(soup.find(attrs={"role": "main"})))
    print("HAS NAV:", bool(soup.find("nav")))
    print("HAS HEADER:", bool(soup.find("header")))
    print("HAS FOOTER:", bool(soup.find("footer")))

    issues = []

    # 1. <title> in <head>
    if not soup.title or not soup.title.text.strip():
        issues.append(["Missing or empty <title> tag in <head>."])

    # 2. lang attribute in <html>
    html_tag = soup.find("html")
    if html_tag and not html_tag.has_attr("lang"):
        issues.append(["Missing 'lang' attribute in the <html> tag."])

    # 3. <img> alt attribute
    for img in soup.find_all("img"):
        if not img.get("alt"):
            img_src = img.get("src", "")
            full_img_url = urljoin(base_url, img_src)
            issues.append(
                [f"Image missing alt attribute: {full_img_url}, HTML: {str(img)}"]
            )

    # 4. Form labels (ignore hidden / type=button / submit / reset)
    for input_tag in soup.find_all(["input", "select", "textarea"]):
        if input_tag.get("type") in ["hidden", "button", "submit", "reset"]:
            continue
        label = None
        if input_tag.get("id"):
            label = soup.find("label", attrs={"for": input_tag["id"]})
        if not label:
            issues.append([f"Form element missing label: {str(input_tag)}..."])

    # 5. Skipped heading order
    heading_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
    last_level = 0
    for h in soup.find_all(heading_tags):
        level = int(h.name[1])
        if last_level and level - last_level > 1:
            issues.append([f"Skipped heading level from h{last_level} to h{level}"])
        last_level = level

    # 6. ARIA attributes check (only check empties)
    for tag in soup.find_all(True):
        for attr in list(tag.attrs.keys()):
            if attr.startswith("aria-") and not str(tag.get(attr)).strip():
                issues.append(
                    [f"{tag.name} missing value or has empty ARIA attribute '{attr}'"]
                )

    # 7. Tabindex and tab order
    tab_tags = soup.find_all(attrs={"tabindex": True})
    tab_indices = [
        int(tag.get("tabindex", 0))
        for tag in tab_tags
        if str(tag.get("tabindex", "")).lstrip("-").isdigit()
    ]
    if tab_indices and sorted(tab_indices) != tab_indices:
        issues.append(["Tabindex values are not in logical/tab order sequence."])

    # 8. Empty roles
    for tag in soup.find_all(attrs={"role": True}):
        if not str(tag["role"]).strip():
            issues.append([f"{tag.name} tag has empty 'role' attribute."])

    # 9. Suggest using landmarks (explicit + implicit)
    roles_needed = {"banner", "main", "navigation", "contentinfo"}
    roles_present = set()

    # Explicit roles
    for tag in soup.find_all(attrs={"role": True}):
        roles_present.add(str(tag.get("role")).strip())

    # Implicit roles from native HTML landmarks
    if soup.find("header"):
        roles_present.add("banner")
    # if soup.find("main"):
    #     roles_present.add("main")
    # if soup.find("nav"):
    #     roles_present.add("navigation")
    if soup.find("footer"):
        roles_present.add("contentinfo")
    if soup.find("nav") or soup.find(attrs={"role": "navigation"}):
        roles_present.add("navigation")

    main_like = soup.find("main") or soup.find(attrs={"role": "main"}) \
            or soup.find(id="main") or soup.find(id="content")
    if main_like:
        roles_present.add("main")


    # >>> DEBUG HERE <<<
    print("HEADER:", bool(soup.find("header")))
    print("MAIN:",   bool(soup.find("main")))
    print("NAV:",    bool(soup.find("nav")))
    print("FOOTER:", bool(soup.find("footer")))
    print("roles_present before suggestions:", roles_present)

    # Suggest only truly missing ones
    for req_role in roles_needed:
        if req_role not in roles_present:
            issues.append(
                [
                    f"Suggested: Consider a landmark region for '{req_role}' "
                    f"(e.g., <header>, <main>, <nav>, <footer>, or role='{req_role}')."
                ]
            )

    return issues



def check_url_and_generate_csv(url, csv_filename="accessibility_report.csv"):
    response = requests.get(url)
    if response.status_code == 200:
        issues = accessibility_check(response.text, url)
        with open(csv_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Issue"])
            for issue in issues:
                writer.writerow(issue)
        print(f"Accessibility issues saved to {csv_filename}")
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")


website_url = "https://weaversweb.com/"
check_url_and_generate_csv(website_url, "report.csv")
