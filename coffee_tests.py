import unittest
from unittest import mock
from final_coffee_db import DataBase
from coffee_web import app


COFEE_DB = "CoffeeForMeDB.db"
fake_db = 'final_coffee_db.COFEE_DB'

def not_a_db_hit():
    print('I did not hit the db')

class Test_DB(unittest.TestCase):

    @mock.patch(fake_db)
    def test_execute_query_get(self, mock_db):
        expected_info =  [('Sugar',)]
        query = 'select bev_type from beverage_type'
        self.assertFalse(mock_db.execute_query_get(query) == expected_info, "Get method is wrong")

    @mock.patch(fake_db)
    def test_execute_query_post(self, mock_db):
        query = 'INSERT INTO sales (name, bill, salesdate) VALUES (?, ?, ?)'
        bill_info = ('John', 3.2, '2019-04-14')
        self.assertFalse(mock_db.send_bill_to_db(bill_info) == True, "Post query is wrong")

    @mock.patch(fake_db)
    def test_get_beverage_types(self, mock_db):
        expected_info =  [('Raf',)]
        print(mock_db.get_beverage_types())
        self.assertFalse(mock_db.get_beverage_types() == expected_info, "Beverage types are wrong")

    @mock.patch(fake_db)
    def test_get_additionals_types(self, mock_db):
        expected_info = [('Sugar',)]
        self.assertFalse(mock_db.get_additionals_types() == expected_info, "Additionals types are wrong")

    @mock.patch(fake_db)
    def test_get_beverage_price(self, mock_db):
        query = 'SELECT price_bev from beverage_type where bev_type = ?'
        param = ('Raf')
        self.assertFalse(mock_db.get_beverage_price(query, param) == 3, "Requesting price is wrong")

    @mock.patch(fake_db)
    def test_salessum_of_salesman(self, mock_db):
        query = 'SELECT SUM(bill) FROM sales where name = ?'
        param = ('John')
        self.assertFalse(mock_db.salessum_of_salesman(query, param) == 3, "Requesting sales sum for a salesman is wrong")

    @mock.patch('coffee_web.db')
    def test_start_page(self, mock_db_web):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('coffee_web.db')
    def test_salesman(self, mock_db_web):
        mock_db_web.side_effect = not_a_db_hit
        response = app.test_client().get('/salesman')
        self.assertEqual(response.status_code, 200)

    @mock.patch('coffee_web.db')
    def test_beverage(self, mock_db_web):
        mock_db_web.side_effect = not_a_db_hit
        response = app.test_client().get('/John/beverage')
        self.assertEqual(response.status_code, 200)


    @mock.patch('coffee_web.db')
    def test_additional(self, mock_db_web):
        mock_db_web.side_effect = not_a_db_hit
        response = app.test_client().get('/Ann/coffee Raf')
        self.assertEqual(response.status_code, 200)

    @mock.patch('coffee_web.db')
    def test_price(self, mock_db_web):
        mock_db_web.side_effect = not_a_db_hit
        response = app.test_client().get('/Ann/coffee Raf/Sugar')
        self.assertEqual(response.status_code, 200)

    @mock.patch('coffee_web.db')
    def test_make_order(self, mock_db_web):
        mock_db_web.side_effect = not_a_db_hit
        response = app.test_client().get('/Ann/coffee Raf/Sugar/bill')
        self.assertEqual(response.status_code, 200)

    @mock.patch('coffee_web.db')
    def test_manager(self, mock_db_web):
        mock_db_web.side_effect = not_a_db_hit
        response = app.test_client().get('/manager')
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()