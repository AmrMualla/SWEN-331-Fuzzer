"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""

from urllib.parse import urljoin
from bs4 import BeautifulSoup


def search(url, session, printing):
    # Initialize URL stack
    url_stack = set()
    url_stack.add(url)
    found_links = set()
    found_links.add(url)

    while len(url_stack) > 0:
        current_url = url_stack.pop()

        # avoid logout links
        if "logout" not in current_url:
            request = session.get(current_url)
            if printing:
                print("Searching: " + current_url)

            # make partial link complete
            soup = BeautifulSoup(request.text, features="html.parser")
            all_links = soup.findAll('a')
            for link in all_links:
                current_link = urljoin(current_url, link.get('href'))

                if current_link not in found_links:
                    # check for base url
                    if url in current_link and "logout" not in current_link:
                        url_stack.add(current_link)
                        found_links.add(current_link)
                        if printing:
                            print("Discovered: " + current_link)
    return found_links
