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
        countryId = getCountry("ru")[0]
        cities = getAllCities(countryId, stopAtOffset=1000 if debug else None)
        i = 0
        for (cid, city) in cities.items():
            i += 1
            print("Processing cid {} city {}".format(cid, city)) if debug else None
            city['universities'] = getAllUniversities(countryId, cid)
            for (uid, uni) in city['universities'].items():
                print("Processing city {} university {}".format(city, uni)) if debug else None
                uni['faculties'] = getAllFaculties(uid)
                if len(city) % PrintEveryUni == 0 or len(city) == len(city['universities']):
                    percent = len(city)/len(city['universities'])*100
                    logging.info("Processed {:.2f}% universities in {}".format(percent, city))
                    print("Processed {:.2f}% universities in {}".format(percent, city))

            print("{} / {}".format(i, len(cities)))
            if i % PrintEveryCity == 0 or i == len(cities):
                percent = i/len(cities)*100
                logging.info("Processed {:.2f}% cities".format(percent))
                print("Processed {:.2f}% cities".format(percent))

    except KeyboardInterrupt:
        logging.critical("Interrupted from keyboard")
    finally:
        save(cities)
        pass
    logging.info("====== Work complete ======")

def save(data):
    filename = "result.json"
    with open(filename, 'w') as f:
        json.dump(data, f)
        print("Result saved to {}".format(filename))
        logging.debug("Result saved to {}".format(filename))


if __name__ == '__main__':
    main()