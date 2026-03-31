# SI 201 HW4 (Library Checkout System)
# Your name: Alia Somero
# Your student id: 9567 7398
# Your email: aliasome@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): I worked on my own, and used chat GPT.
# If you worked with generative AI also add a statement for how you used it.
# e.g.: Used to help me outline my functions.
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
# Yes.
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
# 
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit part



# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    html_file = html_path
    with open(html_file, 'r', encoding="utf-8-sig") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    lst = []
    listings = soup.find_all('div', class_ = 't1jojoys')
    for i in range(len(listings)):
        listing = ' '.join(listings[i].text.split())
        id = listings[i].get('id')[6:]
        lst.append((listing, id))
    return lst
# modified, list instead




   
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    
    
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    
    html_file = os.path.join("html_files", f"listing_{listing_id}.html")
    with open(html_file, 'r', encoding="utf-8-sig") as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
    d = {}
    in_d ={}
    d[listing_id] = in_d

    host = soup.find('div', class_ = '_1k8vduze')
    if not host:
        host = soup.find('ul', class_ = 'fhhmddr')
        
        policy_num = host.find('span', class_ = 'll4r2nl').text
    else:
        policy_num = host.find('span', class_ = 'll4r2nl').text
    if policy_num:
        in_d['policy_number'] = policy_num
    
    host_type = soup.find('span', class_ = "_1mhorg9")
    if host_type:
        in_d['host_type'] = "Superhost"
    else:
        in_d['host_type'] = 'regular'

    host_tag = soup.find('div', class_ = 'c6y5den')
    host = host_tag.find('h2', class_ = 'hnwb2pb').text
    in_d['host_name'] = host.strip()[10:]

    room_type = soup.find('div', class_ = '_kh3xmo')
    
    if not room_type:
        room_tag = soup.find('div', class_ = '_cv5qq4')
        room_type = room_tag.find('h2', class_ = '_14i3z6h').text.strip()
    else:
        room_type = room_type.text.strip()
    
    if 'private' in room_type.lower():
        in_d['room_type'] = 'Private Room'
    elif 'shared' in room_type.lower():
        in_d['room_type'] = 'Shared Room'
    else:
        in_d['room_type'] = 'Entire Room'

    ratings_tag = soup.find_all('div', class_ = '_a3qxec')
    
    rating_val = 0.0
    for tag in ratings_tag:
            
            rating = tag.find('div', class_ = '_y1ba89')
            
            if rating and rating.text.strip() == "Location":
                rating_val = tag.find('span', class_='_4oybiu').text
                
    in_d['location_rating'] = float(rating_val)
    d[listing_id] = inner_d
   
    return d
# finished, modified get listing details

    
    


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    totals = {}
    counts = {}

    for row in data:
        room = row[5]
        rating = row[6]

        if rating == 0.0:
            continue

        if room not in totals:
            totals[room] = 0
            counts[room] = 0

        totals[room] += rating
        counts[room] += 1

    result = {}

    for room in totals:
        result[room] = round(totals[room] / counts[room], 1)

    return result

   
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
   
    invalid = []

    for row in data:
        listing_id = row[1]
        policy = row[2]

        if policy == "Pending" or policy == "Exempt":
            continue

        if not (re.fullmatch(r"\d{4}-\d+STR", policy) or re.fullmatch(r"STR-\d+", policy)):
            invalid.append(listing_id)

    return invalid
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    
    url = "https://scholar.google.com/scholar?q=" + query.replace(" ", "+")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = []

    for h3 in soup.find_all("h3"):
        title = h3.get_text(strip=True)
        if title:
            titles.append(title)

    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        #print(self.listings)
        #self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))


    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
       

        results = [get_listing_details(i) for i in html_list]

        self.assertEqual(results[0]["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(results[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(results[2]["1944564"]["room_type"], "Entire Room")
        self.assertEqual(results[2]["1944564"]["location_rating"], 4.9)

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        for row in self.detailed_data:
            self.assertEqual(len(row), 7)

        self.assertEqual(
        self.detailed_data[-1],
        ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
    )


    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        
        
      

        

       

        # 1. Call output_csv() to create the file
        output_csv(self.detailed_data, out_path)

        # 2. Read the CSV back in
        rows = []
        with open(out_path, "r", encoding="utf-8-sig") as f:
            for line in f:
                rows.append(line.strip().split(","))

        # 3. Check the first data row (skip header → rows[1])
        self.assertEqual(
            rows[1],
            ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        )

        # 4. Clean up
        os.remove(out_path)
            

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        result = avg_location_rating_by_room_type(self.detailed_data)
        self.assertEqual(result["Private Room"], 4.9)


    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        self.assertEqual(invalid_listings, ["16204265"])
    
def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    #main()
    unittest.main(verbosity=2)