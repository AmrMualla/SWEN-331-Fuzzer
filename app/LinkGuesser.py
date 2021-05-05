"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""

import requests


def guess(found_links, session, common_words, extensions, printing):
    # Initialize stack
    guessed_links = set()

    # Check for extensions file
    f = open(extensions, 'r')
    endings = f.read().split()

    if printing:
        print("FUZZER WILL CHECK FOR THE FOLLOWING EXTENSIONS:")
        print(endings)

    # Get common words
    f = open(common_words, 'r')
    words = f.read().split()

    if printing:
        print("FUZZER WILL CHECK FOR THE FOLLOWING COMMON WORDS:")
        print(words)

    # Check for non-file pages
    for link in found_links:
        if link[-1] == '/':
            # Check each word combination
            for word in words:
                # Check each ending combination
                for end in endings:
                    combo_guess = link + word + end

                    # Check if valid page
                    if valid_page(combo_guess, session):
                        guessed_links.add(combo_guess)
                        if printing:
                            print("Guessed: " + combo_guess)
    return guessed_links


def valid_page(link, session):
    request = session.get(link)
    return request.status_code == requests.codes.ok
