import requests
import hashlib  # for various hashing algorithms such as SHA1 and / or MD5
# import sys

print("\n")

# example from the requests module
# r = requests.get('https://api.github.com/events')
# print(r)


# password: 'password123'
# we hashed the password from: https://passwordsgenerator.net/sha1-hash-generator/
# and only used the first 5 characters of the hashed version of our password: password123
# and added to the pwnedpasswords api to get a response:

# url = "https://api.pwnedpasswords.com/range/" + "CBFDA"
# res = requests.get(url)
# print(res)


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {res.status_code}, check the API and try again")
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    # checks password to see if it exists in the API response
    sha1_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    # print(sha1_password)
    first5_chars, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5_chars)
    # print(first5_chars, tail)
    # print(response)
    return get_password_leaks_count(response, tail)


# def main(args):
#     for password in args:
#         count = pwned_api_check(password)
#         if count:
#             print(
#                 f"{password} was found {count} times... you should probably change your password")
#         else:
#             print(f"{password} was not found. carry on!")
#     return "done"


# main(sys.argv[1:])


def main(*args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f"{password} was found {count} times... you should probably change your password")
        else:
            print(f"{password} was not found. carry on!")

    return "done"


print(main("Iftee9007194"))
