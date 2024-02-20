# Usage: python3 ./dependents.py github.com/some/repo

import requests
import sys
from bs4 import BeautifulSoup
import math

score = 0

if len(sys.argv) > 1:
  argument = sys.argv[1]
  # Split on the first occurrence of '/'
  parts = argument.split('/', 1)  # The second parameter specifies the max number of splits
# URL of the GitHub page
url = 'https://'+ parts[0] + '/' + parts[1] + '/network/dependents'

# Send a GET request to the URL
response = requests.get(url)

# If the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the a element first (this example uses a hypothetical class name or id, you will need to adjust it)
    # and then find the span inside it. You might need to adjust the selector based on the actual page structure.
    a_href = '/' + parts[1] + '/network/dependents?dependent_type=REPOSITORY'
    a_element = soup.find('a', href = a_href)
    if a_element:
      number_of_dependents = a_element.text.strip()
      number_of_dependents = number_of_dependents.split('\n', 1)
      number_of_dependents = number_of_dependents[0].replace(",", "")
      number_of_dependents = int(number_of_dependents)
      if (number_of_dependents > 275):
        score = 10
      else:
          score = number_of_dependents / 2.75
          score = math.ceil(score) / 10
    else:
        print("Error: Anchor element not found.")
else:
    print(f"Failed to fetch the page, status code: {response.status_code}")

### READ IN THE SCORE FROM SCORECARDS ###
# Specify the path to your file
file_path = 'tmp.txt'

# Open the file and read its lines
with open(file_path, 'r') as file:
    lines = file.readlines()

scorecard_scores = lines[0].strip()
scorecard_scores = float(scorecard_scores)
total = scorecard_scores * 8
all_together = ((score * 10) + total) / 9
all_together = round(all_together, 2)

# print("The average scorecard score is", scorecard_scores)
# print("The total from the scorecard is", total)
# print("The avg score from the scorecard and dependents is", all_together)

if all_together >= 7.5:
    print("Low Risk")
elif all_together >= 5:
    print("Medium Risk")
else:
    print("High Risk")