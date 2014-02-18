#!/usr/bin/python

import logging, json, sys
from api import *

def main():
    logging.basicConfig(
        filename='log.log',
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s   %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        )
    logging.info("====== Start ======")

    debug = False
    if len(sys.argv) == 2 and sys.argv[1] == "debug":
        debug = True

    PrintEveryCity = 20
    PrintEveryUni = 50

    try:
        result = {}
        countryId = getCountry("ru")[0]
        cities = getAllCities(countryId, stopAtOffset=1000 if debug else None)
        for (cid, city) in cities.items():
            print("Processing city {}".format(city)) if debug else None
            result[city] = {}
            universities = getAllUniversities(countryId, cid)
            for (uid, uni) in universities.items():
                # result[city][uni] = []
                print("Processing city {} university {}".format(city, uni)) if debug else None
                faculties = getAllFaculties(uid)
                result[city][uni] = list(faculties.values())
                if len(result[city]) % PrintEveryUni == 0 or len(result[city]) == len(universities):
                    percent = len(result[city])/len(universities)*100
                    logging.info("Processed {:.2f}% universities in {}".format(percent, city))
                    print("Processed {:.2f}% universities in {}".format(percent, city))
            if len(result) % PrintEveryCity == 0 or len(result) == len(cities):
                percent = len(result)/len(cities)*100
                logging.info("Processed {:.2f}% cities".format(percent))
                print("Processed {:.2f}% cities".format(percent))

    except KeyboardInterrupt:
        logging.critical("Interrupted from keyboard")
    finally:
        save(result)
    logging.info("====== Work complete ======")

def save(data):
    filename = "result.json"
    with open(filename, 'w') as f:
        json.dump(data, f)
        print("Result saved to {}".format(filename))
        logging.debug("Result saved to {}".format(filename))


if __name__ == '__main__':
    main()