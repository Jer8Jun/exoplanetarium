import requests
import random

#https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
query = """
SELECT
    hostname,
    disc_year,
    pl_name,
    pl_orbper,
    pl_orbsmax,
    pl_rade,
    pl_masse,
    pl_eqt,
    sy_pnum,
    sy_dist
FROM pscomppars
WHERE
    pl_controv_flag = 0
"""

def get_random_planet():
    response = requests.get(
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
        params={
            "query": query,
            "format": "json"
        }
    )
    response.raise_for_status()
    return random.choice(response.json())