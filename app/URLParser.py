"""
    Fuzzer Project
    SWEN-331
    Kyle McCoy
"""


def parse(urls, printing):
    # Dictionary of dictionaries (Key: URL, Value: parameter dictionary)
    param_dict = dict()

    # Check each URL for parameters
    for current_url in urls:
        if printing:
            print("Searching Parameters: " + current_url)
        base, current_url_params = parse_url(current_url, printing)
        param_dict[base] = current_url_params

    return param_dict


def parse_url(url, printing):
    url_params = dict()
    sub_divide = url.split('?')

    # Check for URL parameters
    if len(sub_divide) > 1:
        # Get parameter key/value pairs
        if '#' in sub_divide[1]:
            # Check for additional URL fragments after parameters
            parameters = sub_divide[1].split('#')
            url_parameters = parameters[0].split('&')
        else:
            url_parameters = sub_divide[1].split('&')

        for key_value in url_parameters:
            if len(key_value.split('=')) == 2:
                key, value = key_value.split('=')
                url_params[key] = value
                if printing:
                    print("Found Parameter: " + key + "\n Found Value: " + value)
    else:
        if printing:
            print("No parameters found.")

    # Returning base url and parameter dictionary
    return sub_divide[0], url_params
