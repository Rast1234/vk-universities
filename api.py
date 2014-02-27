# -*- coding: UTF-8 -*-
import requests, json, logging, time
requests_log = logging.getLogger('requests')
requests_log.setLevel(logging.CRITICAL)

api_version = 5.10

def callVkApi(method, params):
    logging.debug("calling api: {} - {}".format(method, params))
    requestParams = {'v': api_version}
    requestParams.update(params)
    url  = 'http://api.vk.com/method/{}'.format(method)
    r = getGetGet(url, requestParams)
    data = json.loads( r )
    if 'error' in data:
        logging.exception("api call failed")
        raise Exception(data)
    return data['response']

def getGetGet(url, params, attempts=10):
    for i in range(1, attempts+1):
        try:
            r = requests.get(url, params=params, timeout=10)
            return r.text
        except Exception:
            logging.warn("Api call failed at {} attempt, sleep {}s".format(i, 2**i))
            time.sleep(2**i)

    raise Exception("Failed to execute call {} - {}".format(url, params))

def getCountry(isoCode):
    method = "database.getCountries"
    params = {'code': isoCode, 'count': 1}
    result = callVkApi(method, params)
    cid = result['items'][0]['id']
    name = result['items'][0]['title']
    return (cid, name)

def getAllCities(countryId, stopAtOffset=None):
    method = "database.getCities"
    params = {'country_id': countryId, 'need_all': 1, 'count': 1}
    citiesCount = callVkApi(method, params)['count']
    logging.debug("total cities: {}".format(citiesCount))

    maxItemsPerRequest = 1000
    params['count'] = maxItemsPerRequest
    cities = {}
    for offset in range(0, citiesCount, maxItemsPerRequest):
        if(stopAtOffset is not None and offset > stopAtOffset):
            break
        params['offset'] = offset
        currentCities = callVkApi(method, params)['items']
        # id, important?, title, area, region
        for city in currentCities:
            cid = city['id']
            name = city['title'].strip()
            area = ''
            region = ''
            if 'area' in city.keys():
                area = city['area'].strip()
            if 'region' in city.keys():
                region = city['region'].strip()
            cities[cid] = {'name': name, 'area': area, 'region': region}
        percent = len(cities)/citiesCount*100
        logging.info("Fetched {:.2f}% cities".format(percent))
        print("Fetched {:.2f}% cities".format(percent))
    return cities

def getAllUniversities(countryId, cityId):
    method = "database.getUniversities"
    params = {'country_id': countryId, 'city_id': cityId, 'count': 1}
    uniCount = callVkApi(method, params)['count']
    logging.debug("total universities:{}".format(uniCount))

    maxItemsPerRequest = 10000
    params['count'] = maxItemsPerRequest
    universities = {}
    for offset in range(0, uniCount, maxItemsPerRequest):
        params['offset'] = offset
        currentUnis = callVkApi(method, params)['items']
        # id, title
        for uni in currentUnis:
            uid = uni['id']
            name = uni['title'].strip()
            universities[uid] = {'name': name}
    return universities

def getAllFaculties(universityId):
    method = "database.getFaculties"
    params = {'university_id': universityId, 'count': 1}
    fCount = callVkApi(method, params)['count']
    logging.debug("total faculties:{}".format(fCount))

    maxItemsPerRequest = 10000
    params['count'] = maxItemsPerRequest
    faculties = {}
    for offset in range(0, fCount, maxItemsPerRequest):
        params['offset'] = offset
        currentFaculties = callVkApi(method, params)['items']
        # id, title
        for faculty in currentFaculties:
            fid = faculty['id']
            name = faculty['title'].strip()
            faculties[fid] = {'name': name}
    return faculties



# TODO:
# get universities in each city
# get faculties in each university
# store in mongodb?
# then merge somehow 
