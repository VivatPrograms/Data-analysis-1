import random
import datetime
import csv

def create_random_csv():
    # define a list of products
    products = ["banana", "benis", "apple", "joe biden", "trump"]

    # open a file for writing
    with open("sample_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "product", "quantity", "price"])
        for i in range(100):
            # generate a random date
            date = datetime.date.today() - datetime.timedelta(days=random.randint(0, 365))
            # select a random product from the list
            product = random.choice(products)
            # generate a random quantity
            quantity = random.randint(1, 10)
            #generate a random price
            price = random.uniform(10, 100)
            # write a row to the CSV file
            writer.writerow([date, product, quantity, round(price)])
