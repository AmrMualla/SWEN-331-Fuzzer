"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""


def testForms(form_dict, vectors, session, timeout, sensitive_words, sanitized):
    key_list = list(form_dict.keys())

    for url in key_list:
        print("Testing forms on: " + url + "\n")
        forms = form_dict[url]

        for form in forms:
            form_method = str(form['method']).lower()

            for vector in vectors:
                inputs = form.findAll('input')
                print("Testing Vector: " + vector.__str__())

                request_params = {}

                for inputCheck in inputs:
                    if 'name' in inputCheck.attrs:
                        name = inputCheck['name']
                        if name.lower().strip() == 'submit':
                            request_params[name] = "Submit"
                        else:
                            request_params[name] = vector.rstrip()
                    elif 'type' in inputCheck.attrs:
                        name = inputCheck['type']
                        if name.lower().strip() == 'submit':
                            request_params[name] = "Submit"
                        else:
                            request_params[name] = vector.rstrip()

                if form_method == "post":
                    post_response = session.post(url, data=request_params)

                    analyze_response_time(post_response, timeout)
                    analyze_status_code(post_response)
                    analyze_sensitive_data(post_response, sensitive_words)
                    analyze_sanitization(post_response, vector, sanitized)

                elif form_method == "get":
                    get_response = session.get(url, data=request_params)

                    analyze_response_time(get_response, timeout)
                    analyze_status_code(get_response)
                    analyze_sensitive_data(get_response, sensitive_words)
                    analyze_sanitization(get_response, vector, sanitized)
                print("")
        print("")


# Attack all url params with vectors
def testURLs(param_dict, vectors, session, timeout, sensitive_words, sanitized):
    key_list = list(param_dict.keys())

    for url in key_list:
        print("Testing URL Parameters on: " + url)
        curr_param_d = param_dict[url]
        parameters = curr_param_d.keys()  # ignore values
        request_param_d = {}

        for vector in vectors:
            for param in parameters:
                request_param_d[param] = vector
                response = session.get(url, params=request_param_d)
                analyze_response_time(response, timeout)
                analyze_status_code(response)
                analyze_sensitive_data(response, sensitive_words)
                analyze_sanitization(response, vector, sanitized)


# Detects responses that take longer than expected
def analyze_response_time(response, timeout):
    load_time = response.elapsed.total_seconds() * 1000
    if load_time > timeout:
        print("Response took " + load_time.__str__() + " ms; Potential Denial Of Service Vulnerability")


# Detects unusual response codes and reports them
def analyze_status_code(response):
    print("Return code: " + get_status_code(response.status_code))


# Detects if sensitive data may have been leaked on a page
def analyze_sensitive_data(response, sensitive_words):
    for sensitive_word in sensitive_words:
        if sensitive_word in response.text:
            print("Response contained the following sensitive word: " + sensitive_word)


# Detects if vector was sanitized properly
def analyze_sanitization(response, vector, sanitizer):
    for sanitized in sanitizer:
        if sanitized in vector and sanitized not in response.text and vector in response.text:
            print("The following vector wasn't sanitized correctly: " + vector)
            print("This page may be vulnerable!")


# Returns a string representing the response code (only common codes)
def get_status_code(code):
    if code == 200:
        return "200 --> Successful (OK)"
    if code == 303:
        return "303 --> Redirection (See Other)"
    if code == 400:
        return "400 --> Client Error (Bad Request)"
    if code == 401:
        return "401 --> Client Error (Unauthorized)"
    if code == 403:
        return "403 --> Client Error (Forbidden)"
    if code == 404:
        return "404 --> Client Error (Not Found)"
    if code >= 500:
        return code.__str__() + " --> Server Error"
    else:
        return code.__str__() + " --> Unknown Code"
