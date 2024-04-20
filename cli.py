import os
import time
from fetchers.events import EventFetcher
from fetchers.matches import MatchesFetcher
from fetchers.competitions import CompetitionsFetcher
from db import init_db

RAW_DATA_DIR=os.path.join(os.getcwd(),"raw_data")

OPEN_DATA_PATHS = {
    "competitions": "https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json",
    "matches": "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{competition_id}/{season_id}.json",
    "lineups": "https://raw.githubusercontent.com/statsbomb/open-data/master/data/lineups/{match_id}.json",
    "events": "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json",
}

def main():
    start = time.time()
    conn = init_db()

    print("Running competition fetcher...")
    comp_fetcher = CompetitionsFetcher(OPEN_DATA_PATHS['competitions'], conn)
    comps = comp_fetcher.fetch()

    print("Running matches fetcher...")
    matches_fetcher = MatchesFetcher(OPEN_DATA_PATHS["matches"], conn)

    for comp in comps:
        matches_fetcher.fetch(comp['competition_id'], comp['season_id'])

    print("Running event fetcher...")
    event_fetcher = EventFetcher(OPEN_DATA_PATHS['events'], conn)
    event_fetcher.download(RAW_DATA_DIR)

    end = time.time()

    print(f"data-fetcher ended in {end - start} seconds")

if __name__ == '__main__':
    main()