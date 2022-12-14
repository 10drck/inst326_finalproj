import pandas as pd
import csv
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import re
import sys


class RestaurantData:
    """
    Sarah Peng
    Takes in the dataframe and analyzes it, byt getting the total for each
    bill and the orders per hour.

    Attributes:
      data_frame (str): the data frame that is passed in by the restaurant
    """

    def __init__(self, data_frame):
        """Sarah Peng
        creates the data_frame to be analyzed

        Args:
            data_frame: the dataframe for analysis

        Side effects:
            Creates RestaurantData attribute
        """

        self.df = data_frame

    def order_total(self):
        """ Sarah Peng
        - conditional statements 
        Takes in the customers order and checks if it is available
        and calculates the total cost of their bill

        Args:
            dataframe (str): the orders and costs of the products

        Returns: the total cost of each bill
        """
        order_id = self.df.loc[0, "Order Number"]
        order_ids = []
        order_total = []
        for index in range(len(self.df)):
            if index == 0:
                order_id = self.df.loc[index, "Order Number"]
                quantity = self.df.loc[index, "Quantity"]
                product_price = self.df.loc[index, "Product Price"]
                total = quantity * product_price
            else:
                if order_id == self.df.loc[index, "Order Number"]:
                    quantity = self.df.loc[index, "Quantity"]
                    product_price = self.df.loc[index, "Product Price"]
                    total = total + (quantity * product_price)
                else:
                    order_ids.append(order_id)
                    order_total.append(total)
                    order_id = self.df.loc[index, "Order Number"]
                    quantity = self.df.loc[index, "Quantity"]
                    product_price = self.df.loc[index, "Product Price"]
                    total = 0
                    total = total + (quantity * product_price)
        orderTotals_list = [order_ids, order_total]
        return orderTotals_list

    def peak_hours(self):
        """Sarah Peng
        - regex formula 
        Summary: calculates the total orders for each hour

        Args:
            data_frame(str): has the hour of the orders and each order

        Returns:
          a dictionary with the hours and the number of orders
        """

        times_list = []

        for index in range(len(self.df)):
            if index == 0:
                order_id = self.df.loc[index, "Order Number"]
                date = self.df.loc[index, "Order Date"]
                match = re.search(
                    r"(\d{1,2}\/)(\d{1,2}\/\d{2,4} )(\d{1,2})(:\d{1,2})", date
                )
                hour = match.group(3)
                times_list.append(hour)
            else:
                if order_id != self.df.loc[index, "Order Number"]:
                    date = self.df.loc[index, "Order Date"]
                    match = re.search(
                        r"(\d{1,2}\/)(\d{1,2}\/\d{2,4} )(\d{1,2})(:\d{1,2})", date
                    )
                    hour = match.group(3)
                    times_list.append(hour)
                    order_id = self.df.loc[index, "Order Number"]

        elements_count = {}

        for element in times_list:
            if element in elements_count:
                elements_count[element] += 1
            else:
                elements_count[element] = 1

        return elements_count

    def create_customer_bill(first_list, second_list):
        """creates a list of tuples with the orders and prices

        Args:
            first_list (list): a list of all the orders
            second_list (list): list of all the prices

        Returns:
            bill_list (list of tuples): a list of the orders and the price
        """
        bill_list = [(first_list[i], second_list[i]) for i in range(0, len(first_list))]
        return bill_list

    def __str__(bill_list):
        """returns the orders and totals

        Args:
            bill_list (list of tuples): the list of bills created above

        Returns:
            order_id : the formal representation of the order id 
            order_total: the total of each order
        """
        for bills in bill_list:
            for order_id in bills:
                return f"{order_id}"


def time_analysis(elements_count):
    """take in elements_count dictionary run min() and max();
    Args:
        elements_count (dict): the number of orders per hour
    returns:
        max_hour (list): list of the busiest hour
        min_hour (list): list of the slowest hour"""
    # iterate through the dictionary; print the key with the highest value
    # iterate through the dictionary; print the key with the lowest value
    max_hour = [
        time
        for time, value in elements_count.items()
        if value == max(elements_count.values())
    ]
    min_hour = [
        time
        for time, value in elements_count.items()
        if value == min(elements_count.values())
    ]
    return f"Busiest Time(s): {max_hour} Slowest Time(s): {min_hour}"


def write_file(list_of_idtotals):
    """Be able to write to a csv to allow for spread sheet view of order totals. Kendrick M

    args:
      list_of_idtotals (list): a list containing two different lists. One list being order ids and the other being the combined totals for each id.
    """
    ids = list_of_idtotals[0]
    totals = list_of_idtotals[1]

    df = pd.DataFrame({"ids": ids, "totals": totals})
    df.to_csv("order_totals.csv")  # <- allocated file


def plot_data(data_csv):
    """Using the data that is passed through, plot a cohesive diagram for the owner to indicate trends in their restaurant. Kendrick M
    Args:
      data_csv (csv file): .csv file that is provided from the restaurant of accumulated orders from x amount of time
    """
    plt.figure(figsize=(10, 10), dpi=100)  # figure size for plotting

    df = pd.read_csv(data_csv)
    df = df.drop(
        ["Order Number", "Order Date", "Product Price", "Total products"], axis=1
    )  # drops columns for reading

    df = (
        df.groupby(["Item Name"], as_index=False, sort=False)
        .sum()
        .sort_values(by=["Quantity"], ascending=False)
    )  # grouping to view quantities
    plt.bar(x=df["Item Name"].head(7), height=df["Quantity"].head(7))
    plt.savefig("data.png")  # saves to directory as 'data.png'
    print("Done with the graph, view it in 'data.png!'")


def main(ordersFile):
    """intialize objects in this code, and calls for the different functions in the code.

    args:
      ordersFile(str): path of file.
    """
    # open the given file which is a csv
    with open(ordersFile, "r") as file:
        df = pd.read_csv(file)

    # call Restaurant class to pass in the csv file
    restaurantdata = RestaurantData(df)

    write_file(RestaurantData.order_total(restaurantdata))

    print(time_analysis(RestaurantData.peak_hours(restaurantdata)))

    print(RestaurantData.__str__(RestaurantData.order_total(restaurantdata)))
    customerinput = input(f"Would you like to see {args} as a plot? Yes or No: ")
    if customerinput.lower() == "yes":
        plot_data(ordersFile)
    elif customerinput.lower() == "no":
        pass
    else:
        print("That was an invalid input")


def parse_args(argslist):
    """Parse command line arguments
    Args:
        argslist (list): command line arguments

    Returns:
        args: parsed arguments
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file containing food items and stocks")

    return parser.parse_args(argslist)


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    main(args.file)
