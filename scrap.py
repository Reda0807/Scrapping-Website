import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

rep = requests.get("https://www.booking.com/searchresults.en-gb.html?ss=Italy&ssne=Italy&ssne_untouched=Italy&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaMIBiAEBmAEJuAEXyAEM2AEB6AEBiAIBqAIDuALHoNC3BsACAdICJDk4ZDFjNTM2LWRkNDMtNGU1ZC1hZWU1LTg0M2QxODkwZjMwZNgCBeACAQ&sid=ead78d14fd9e4d904d89b3da04ea788d&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=104&dest_type=country&group_adults=2&no_rooms=1&group_children=0", headers=headers)
html = rep.text

print(html)