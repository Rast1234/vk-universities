#!/usr/bin/python

__author__ = 'rast'

"""
Reads .csv file
"""
import csv, json

def main():
    all = {}
    with open('unis.csv') as csvfile:
        csvfile.readline()  # skip header
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')  # will it fail at """" ?
        for row in reader:
            # district region main_uni main_uni_short uni uni_short weight
            tmp = [' '.join(x.split()) for x in row]  # get rid of newlines
            (district, region, umain, umain_short, u, u_short, weight) = tmp

            uni = {
                #'parent': umain,
                #'parent_short': umain_short,
                'weight': weight,
                'region': region,
                'district': district,
                'city': None,
                'faculties': [],
            }
            # do not include them if it is the main university already
            if u.lower() != umain.lower():
                uni['parent'] = umain
            if u_short.lower() != umain_short.lower():
                uni['parent_short'] = umain_short

            key = "{} # {}".format(u_short, u)  # not using tuple because of json serializerz
            if (key) in all.keys():
                    raise ValueError("University key duplicate: {}".format(key))
            else:
                all[key] = uni
    filename = "all_unis.json"
    with open(filename, 'w') as f:
        json.dump(all, f)
        print("Result saved to {}".format(filename))


if __name__ == "__main__":
    main()