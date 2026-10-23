import requests
from bs4 import BeautifulSoup
import csv


url = "https://en.wikipedia.org/wiki/FIFA_World_Cup"


request_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


try:
    response = requests.get(
        url,
        headers=request_headers,
        timeout=15
    )

    response.raise_for_status()

    print("Status:", response.status_code)


except requests.exceptions.RequestException as error:

    print("Request failed:")
    print(error)
    exit()


# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")


# Find the Results heading
results_heading = soup.find(
    lambda tag: tag.name in ["h2", "h3"]
    and tag.get_text(strip=True) == "Results"
)


# Find the first table after the Results heading
table = results_heading.find_next(
    "table",
    class_="wikitable"
)


# Extract column headers
table_headers = []

for header in table.find_all("th"):

    table_headers.append(
        header.get_text(" ", strip=True)
    )


# Extract the table rows
data = []

rows = table.find_all("tr")


for row in rows[3:]:  # Skip the header rows

    cells = row.find_all(["td", "th"])

    # Extract text from each cell
    values = [
        cell.get_text(" ", strip=True)
        for cell in cells
    ]


    # Skip empty rows
    if not values:
        continue


    # Start with no year found
    year = None


    # Check the first two columns for a valid year
    for value in values[:2]:

        if value.isdigit():

            possible_year = int(value)

            # Check if it looks like a World Cup year
            if 1900 <= possible_year <= 2100:

                year = possible_year
                break


    # Skip the row if no year was found
    if year is None:
        continue


    # Stop when the year goes beyond 1975
    if year > 1975:
        break


    # Store the row
    data.append(values)


# Print the scraped data
for row in data:
    print(row)


# Write data to CSV
with open(
    "Fifa_WC_Results.csv",
    mode="w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    # Write column names
    writer.writerow(table_headers)

    # Write all rows
    writer.writerows(data)