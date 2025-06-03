import datetime, json

import requests

UNITY_VERSION = "2022.3.21f1"
DEFAULT_HEADERS = {"user-agent": "Lorcana/2023.1", "x-unity-version": UNITY_VERSION}

class DownloadException(BaseException):
    pass

def retrieveFromUrl(url, maxAttempts = 5, additionalHeaderFields = None):
    """
    Since downloading from the Ravensburger API and CDN can sometimes take a few attempts, this helper method exists.
    It downloads the provided URL, tries a few times if it somehow fails, and if if succeeds, it returns the request
    :param url: The URL to retrieve
    :param maxAttempts: How many times to try to download the file
    :param additionalHeaderFields: Optional extra header fieldss to pass along with the call, on top of the default header fields
    :return: The Requests request with the data from the provided URL
    :raises DowloadException: Raised if the retrieval failed even after several attempts
    """
    headers = DEFAULT_HEADERS

    if additionalHeaderFields:
        headers = DEFAULT_HEADERS.copy()
        headers.update(additionalHeaderFields)

    request = None

    for attempt in range(1, maxAttempts + 1):
        request = requests.get(url, headers=headers, timeout=10)
        if request.status_code == 200:
            return request
	
    raise DownloadException(f"Download of '{url}' failed after {maxAttempts:,}, last attempt's status code: {request.status_code if request else 'missing'}")


def retrieveCardCatalog():
	# First get the token we need for the API, in the same way the official app does
	tokenResponse = requests.post("https://sso.ravensburger.de/token",
        headers={
            # API key captured from the official Lorcana app
            "authorization": "Basic bG9yY2FuYS1hcGktcmVhZDpFdkJrMzJkQWtkMzludWt5QVNIMHc2X2FJcVZEcHpJenVrS0lxcDlBNXRlb2c5R3JkQ1JHMUFBaDVSendMdERkYlRpc2k3THJYWDl2Y0FkSTI4S096dw==",
            "content-type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "client_credentials"},
        timeout=10)

	if tokenResponse.status_code != 200:
		raise ValueError(f"Non-success reply when retrieving token (status code {tokenResponse.status_code}): {tokenResponse.text=}")

	tokenData = tokenResponse.json()

	if "access_token" not in tokenData or "token_type" not in tokenData:
		raise ValueError(f"Missing access_token or token_type in token request: {tokenResponse.text}")

	# Now we can retrieve the card catalog, again just like the official app
	catalogResponse = retrieveFromUrl(f"https://api.lorcana.ravensburger.com/v2/catalog/fr", additionalHeaderFields={"authorization": f"{tokenData['token_type']} {tokenData['access_token']}"})
	cardCatalog = catalogResponse.json()

	if "cards" not in cardCatalog:
		raise ValueError(f"Invalid data in catalog response: {catalogResponse.text}")

	return cardCatalog

data = retrieveCardCatalog()
# json_formatted_str = json.dumps(obj, indent=4)
# print(json_formatted_str)

with open("data/cards.json", "w", encoding='utf8') as write_file:
    json.dump(data, write_file, indent=4, ensure_ascii=False)