"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""
from app import Tester


def test(param_dict, form_dict, session, args):
    # Read Vectors
    vectors = open(args.vectors).readlines()

    # Read Sensitive
    sensitive = open(args.sensitive).readlines()

    # Read Sanitized
    sanitized = open(args.sanitized_chars).readlines()

    print("_________________________________________________________")
    print("TESTING VECTORS AGAINST FORMS...")
    Tester.testForms(form_dict, vectors, session, args.slow, sensitive, sanitized)

    print("_________________________________________________________")
    print("TESTING VECTORS AGAINST URL PARAMETERS...")
    Tester.testURLs(param_dict, vectors, session, args.slow, sensitive, sanitized)
