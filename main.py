import csv
import matplotlib.pyplot as plt
import numpy as np


class Business:
    def __init__(self, id, name, rev_cnt, cat, rat, lat, lon, price):
        self.id = id
        self.sys_id = name
        self.review_count = rev_cnt
        self.category = cat
        self.rating = rat
        self.latitude = lat
        self.longitude = lon
        self.price = price


def prepare_data(file):
    business_list = list()
    with open(file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='~')
        next(csv_reader, None)
        for row in csv_reader:
            business_list.append(Business(row[0], row[1], row[4], row[5], row[6], row[7], row[8], row[9]))
    return business_list


def quasi_heatmap(data):
    coords = list()
    for business in data:
        coords.append((float(business.longitude), float(business.latitude)))
    df = np.array(coords)
    plt.plot(df[:, 0], df[:, 1], 'o')
    plt.title('Lokale w Warszawie'), plt.xlabel('Longitude'), plt.ylabel('Latitude'), plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    data = prepare_data("restaurants_test_view.csv")
    quasi_heatmap(data)
    print(len(data))

