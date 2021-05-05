# Fuzzer

SWEN 331  
Kyle McCoy
---------------------------------------------

Project Description  
http://www.se.rit.edu/~swen-331/projects/fuzzer/

---------------------------------------------
**Dependencies**

Python 3.8

To install dependencies do:
`pip install -r requirements.txt`

---------------------------------------------
How To Run:
---------------------------------------------

This project can be run from the terminal inside the Fuzzer directory.  
All output will be printed to stdout

### Discover:

Generic run:  
`python fuzz.py discover [url] --custom-auth=dvwa --common-words=[filename] --extensions=[filename]`  

Example run:  
`python fuzz.py discover http://127.0.0.1/dvwa/ --custom-auth=dvwa --common-words=common_words.txt --extensions=common_extensions.txt`

### Discover:
Generic run:  
`python fuzz.py test [url] --custom-auth=dvwa --common-words=[filename] --extensions=[filename] --vectors=[filename] --sanitized-chars=[filename] --sensitive=[filename] --slow=[number]`  

Example run:  
`python fuzz.py test http://127.0.0.1/dvwa/ --custom-auth=dvwa --common-words=common_words.txt --extensions=common_extensions.txt --vectors=vectors.txt --sanitized-chars=sanitized.txt --sensitive=sensitive.txt --slow=500` 

