class Store:

    def __init__(self, name, deliveries, comission):
        self.name = name 
        self.deliveries = deliveries # Array of integers, where each integer is the delivery price
        self.comission = comission  # Delivery price percentage that the store pays to the motoboys
    
class Motoboy:
    
    def __init__(self, name, tax, stores):
        self.name = name
        self.tax = tax # Fixed value charged by the motoboy
        self.stores = stores # Stores that the motoboy can attend to.

        # Default attributes
        self.stores_attended_to = [] # Stores that the motoboy effectively made deliveries for.
        self.delivery_count = 0 # Number of deliveries made by the motoboy
        self.profit = 0 # Motoboy profit

    def make_delivery(self, delivery, store):
        """ 
        Calculates motoboy profit and delivery count 
        based on the delivery and store parameters
        """
        if store in self.stores:
            comission_profit = delivery * store.comission
            self.profit += self.tax + comission_profit
            self.delivery_count += 1
            if store not in self.stores_attended_to:
                self.stores_attended_to.append(store)

    def report_results(self):
        stores_attended_to = ', '.join([store.name for store in self.stores_attended_to])
        return f"Motoboy name: {self.name} - Stores attended to: {stores_attended_to} - " + \
               f"Delivery count: {self.delivery_count} - Profit: {self.profit}"


# Store setup
stores_list = [
    Store('Store 1', [50, 50, 50], 0.05),
    Store('Store 2', [50, 50, 50, 50], 0.05),
    Store('Store 3', [50, 50, 100], 0.15)
]

# Motoboy setup
motoboys_list = [
    Motoboy('Motoboy 1', 2, stores_list),
    Motoboy('Motoboy 2', 2, stores_list),
    Motoboy('Motoboy 3', 2, stores_list),
    Motoboy('Motoboy 4', 2, [stores_list[0]]),
    Motoboy('Motoboy 5', 3, stores_list)
]
# Motoboy look up dict, used to filter for a specific motoboy when displaying the results
lookup_moto_dict = {str(index): motoboy for index, motoboy in enumerate(motoboys_list, 1)}


def sort_motoboys(motoboy_array):
    """
    Sort an array of Motoboy objects using 3 criteria, in this priority order:
    1. Delivery count: motoboys with less deliveries made are always placed first, favoring
       a more balanced distribution of deliveries between motoboys.
    2. Motoboy exclusivity/priority: between motoboys with the same amount of deliveries made, 
       those that work exclusively for one store are prioritized by that store. This is achieved by evaluating
       the length of the motoboy stores attribute. Since the evaluated motoboy array is always an array of
       eligible motoboys for a specific store, those motoboys with less stores that they can attend
       to are those that work exclusively to said store.
    3. Motoboy tax: motoboys that charge less for each delivery are prioritized.
    """
    return sorted(motoboy_array, key=lambda m: (m.delivery_count, len(m.stores), m.tax))

def process_deliveries(stores_list, motoboys_list):
    """
    Evaluates all the stores deliveries and distribute them to the motoboys
    """
    for store in stores_list:
        # motoboys allowed to deliver for the current evaluated store
        eligible_motoboys = [motoboy for motoboy in motoboys_list if store in motoboy.stores] 
        for delivery in store.deliveries:
            sorted_motoboys = sort_motoboys(eligible_motoboys)
            chosen_motoboy = sorted_motoboys[0]
            chosen_motoboy.make_delivery(delivery, store)


if __name__ == '__main__':
    process_deliveries(stores_list, motoboys_list)
    chosen_motoboy = input('Choose the motoboy by inserting an integer between 1 and 5 or leave it blank to see the full report: ')
    moto_obj = lookup_moto_dict.get(chosen_motoboy)
    if moto_obj:
        print(moto_obj.report_results())
    else:
        [print(motoboy.report_results()) for motoboy in motoboys_list]
