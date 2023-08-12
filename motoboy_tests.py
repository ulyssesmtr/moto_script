import unittest
from motoboys import Motoboy, Store, sort_motoboys, process_deliveries


class TestStore(unittest.TestCase):

    def setUp(self):
        self.store = Store('Store 1', [50, 50, 50], 0.05)
        
    def test_store_obj_attributes(self):
        """Store objects must have these specific attributes"""
        self.assertEqual(
            set(self.store.__dict__.keys()),
            set(('name', 'deliveries', 'comission'))
        )
    
    def test_store_obj_attribute_values(self):
        """
        Store object attribute values should be the same
        as the ones used when instanciating it
        """
        expected_values = {
            'name': 'Store 1',
            'deliveries': [50, 50, 50],
            'comission': 0.05
        }
        for attribute, value in expected_values.items():
            with self.subTest():
                self.assertEqual(
                    getattr(self.store, attribute),
                    value
                )


class TestMotoboy(unittest.TestCase):

    def setUp(self):
        self.store = Store('Store 1', [50, 50, 50], 0.05)
        self.motoboy = Motoboy('Motoboy 1', 2, [self.store])

    def test_motoboy_obj_attributes(self):
        """Motoboy objects must have these specific attributes"""
        self.assertEqual(
            set(self.motoboy.__dict__.keys()),
            set(('stores_attended_to', 'stores', 'name', 'tax', 'profit', 'delivery_count')) 
        )

    def test_motoboy_obj_attribute_values(self):
        """
        Motoboy object attribute values should be the same
        as the ones used when instanciating it
        """
        expected_values = {
            'name': 'Motoboy 1',
            'tax': 2,
            'stores': [self.store],
            'stores_attended_to': [],
            'delivery_count': 0,
            'profit': 0
        }
        for attribute, value in expected_values.items():
            with self.subTest():
                self.assertEqual(
                    getattr(self.motoboy, attribute),
                    value
                )

    def test_motoboy_make_delivery(self):
        """
        After making a delivery, the motoboy profit 
        and delivery count should be updated correctly
        """
        self.motoboy.make_delivery(50, self.store)
        self.assertListEqual(
            [self.motoboy.delivery_count, self.motoboy.profit],
            [1, 4.5])
    
    def test_motoboy_make_delivery_not_allowed_store(self):
        """
        A motoboy cannot be allowed to make a delivery to store 
        he does not work for.
        """
        new_store = Store('Store 2', [50, 50, 50, 50], 0.05)
        self.motoboy.make_delivery(50, new_store)
        self.assertListEqual(
            [self.motoboy.delivery_count, self.motoboy.profit],
            [0, 0])

    def test_motoboy_report_results(self):
        self.motoboy.make_delivery(50, self.store)
        expected_value = "Motoboy name: Motoboy 1 - Stores attended to: Store 1 - " + \
                         "Delivery count: 1 - Profit: 4.5"

        self.assertEqual(self.motoboy.report_results(), expected_value) 


class TestSortMotoboys(unittest.TestCase):

    def setUp(self):
        self.stores_list = [
            Store('Store 1', [50, 50, 50], 0.05),
            Store('Store 2', [50, 50, 50, 50], 0.05),
            Store('Store 3', [50, 50, 100], 0.15)
        ]
        self.motoboy_list = [
            Motoboy('Motoboy 1', 2, self.stores_list),
            Motoboy('Motoboy 2', 2, self.stores_list),
            Motoboy('Motoboy 3', 2, self.stores_list),
            Motoboy('Motoboy 4', 2, [self.stores_list[0]]),
            Motoboy('Motoboy 5', 3, self.stores_list)
        ]

    def test_sort_delivery_count(self):
        """Motoboys with less deliveries should be placed first"""
        store = self.stores_list[0]
        for motoboy in self.motoboy_list[:-1]:
            motoboy.make_delivery(50, store)
        sorted_motoboys = sort_motoboys(self.motoboy_list)
        first_motoboy = sorted_motoboys[0]
        for motoboy in sorted_motoboys[1:]:
            with self.subTest():
                self.assertTrue(first_motoboy.delivery_count <= motoboy.delivery_count)

    def test_sort_store_priority(self):
        """
        When all the motoboys have the same delivery count, the second paramater
        evaluated when ordering should be the store priority/exclusivity.
        For store 1, the first motoboy in this case should be Motoboy 4.
        """
        eligible_motoboys = [motoboy for motoboy in self.motoboy_list if self.stores_list[0] in motoboy.stores] 
        sorted_motoboys = sort_motoboys(eligible_motoboys)
        self.assertEqual(sorted_motoboys[0].name, 'Motoboy 4')
    
    def test_sort_tax(self):
        """
        After delivery count and store priority, the last parameter evaluated
        should be the motoboy tax. Motoboys that charge more should be placed last
        """
        sorted_motoboys = sort_motoboys(self.motoboy_list)
        last_motoboy = sorted_motoboys[-1]
        for motoboy in sorted_motoboys[:-1]:
            with self.subTest():
                self.assertTrue(last_motoboy.tax >= motoboy.delivery_count)


class TestProcessDeliveries(unittest.TestCase):
    
    def setUp(self):
        self.stores_list = [
            Store('Store 1', [50, 50, 50], 0.05),
            Store('Store 2', [50, 50, 50, 50], 0.05),
            Store('Store 3', [50, 50, 100], 0.15)
        ]
        self.motoboys_list = [
            Motoboy('Motoboy 1', 2, self.stores_list),
            Motoboy('Motoboy 2', 2, self.stores_list),
            Motoboy('Motoboy 3', 2, self.stores_list),
            Motoboy('Motoboy 4', 2, [self.stores_list[0]]),
            Motoboy('Motoboy 5', 3, self.stores_list)
        ]
    
    def test_process_deliveries_result(self):
        process_deliveries(self.stores_list, self.motoboys_list)
        expected_result = {
            'Motoboy 1': "Motoboy name: Motoboy 1 - Stores attended to: Store 1, Store 2, Store 3 - Delivery count: 3 - Profit: 26.0",
            'Motoboy 2': "Motoboy name: Motoboy 2 - Stores attended to: Store 1, Store 2 - Delivery count: 2 - Profit: 9.0",
            'Motoboy 3': "Motoboy name: Motoboy 3 - Stores attended to: Store 2, Store 3 - Delivery count: 2 - Profit: 14.0",
            'Motoboy 4': "Motoboy name: Motoboy 4 - Stores attended to: Store 1 - Delivery count: 1 - Profit: 4.5",
            'Motoboy 5': "Motoboy name: Motoboy 5 - Stores attended to: Store 2, Store 3 - Delivery count: 2 - Profit: 16.0",
        }
        for motoboy in self.motoboys_list:
            with self.subTest():
                self.assertEqual(motoboy.report_results(), expected_result[motoboy.name])
                

if __name__ == '__main__':
    unittest.main()



