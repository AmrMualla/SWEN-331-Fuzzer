"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""

from bs4 import BeautifulSoup


def parse(urls, session, printing):
    # Form Dictionary
    forms = {}

    for url in urls:
        if printing:
            print("Parsing Form Inputs: " + url)
        request = session.get(url)
        soup_parse = BeautifulSoup(request.text, features="html.parser")
        forms[url] = soup_parse.findAll('form')

        if len(forms[url]) == 0:
            if printing:
                print("No forms found.")
        else:
            for form in forms[url]:
                if printing:
                    print("Form Method: " + form["method"])
                for tag in form.recursiveChildGenerator():
                    if tag.name == "input":
                        if "name" in tag.attrs:
                            if printing:
                                print("Input Tag Name: " + tag["name"])
                        if "value" in tag.attrs:
                            if printing:
                                print("Input Tag Value: " + tag["value"])

    # Returning Forms Dictionary (URL -> Form(s))
    return forms
