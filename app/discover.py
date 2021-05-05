"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""

import sys
import requests
from bs4 import BeautifulSoup
from app import LinkFinder, LinkGuesser, URLParser, FormParser


def discover(args, printing):
    # Session to store history
    session = requests.Session()

    # Set up custom_auth
    if args.custom_auth is not None:
        if args.custom_auth.lower() == "dvwa":
            # Login and set security level to Low
            if printing:
                print("CHANGING SECURITY TO LOW")
            if args.url[-1] != '/':
                args.url += "/"
            session.post(args.url + "setup.php", data={'create_db': "Create / Reset Database",
                                                       'user_token': getToken(session, args.url + "login.php")})
            session.post(args.url + "login.php", data={'Login': 'Login', 'username': 'admin', 'password': 'password',
                                                       'user_token': getToken(session, args.url + "login.php")})
            session.post(args.url + "security.php", data={'seclev_submit': 'Submit', 'security': 'low',
                                                          'user_token': getToken(session, args.url + "security.php")})
            # Print Home Screen HTML <Iteration 0>
            # print(session.get(args.url).text)
        else:
            # Invalid auth
            if printing:
                print(args.custom_auth + " is an invalid authentication input.\nAvailable options include : dvwa\n")
            sys.exit()

    # Link Discovery
    if printing:
        print("_________________________________________________________")
        print("DISCOVERING LINKS...")
    found_links = sorted(LinkFinder.search(args.url, session, printing))

    if printing:
        print("_________________________________________________________")
        print("GUESSING LINKS...")
    guessed_links = sorted(LinkGuesser.guess(found_links, session, args.common_words, args.extensions, printing))
    final = list(set(found_links) | set(guessed_links))
    final_urls = sorted(final)

    if printing:
        print("_________________________________________________________")
        print("CRAWLING ALL LINKS...")
    for link in final_urls:
        if printing:
            print("Searching: " + link)
        crawled_links = sorted(LinkFinder.search(link, session, False))
        empty = True
        for found in crawled_links:
            if found not in final_urls:
                empty = False
                if printing:
                    print("Discovered: " + found)
        if empty:
            if printing:
                print("No links found.")

    if printing:
        print("_________________________________________________________")
        print("PARSING URLs...")
    param_dict = URLParser.parse(final_urls, printing)

    if printing:
        print("_________________________________________________________")
        print("DISCOVERING FORM PARAMETERS...")
    form_dict = FormParser.parse(final_urls, session, printing)

    if printing:
        print("_________________________________________________________")
        print("DISPLAYING COOKIES...")
    if len(session.cookies) > 0:
        for cookie in session.cookies:
            if printing:
                print(cookie)
    else:
        if printing:
            print("No Cookies found.")

    return param_dict, form_dict, session


def getToken(session, url):
    soup = BeautifulSoup(session.get(url).text, features="html.parser")
    return soup.find("input", {"name": "user_token"})["value"]
