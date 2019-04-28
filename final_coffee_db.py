import sqlite3
from logs import logger



COFEE_DB = "CoffeeForMeDB.db"
BEVERAGE_TYPES = 'select bev_type from beverage_type'
ADDITIONALS_TYPES = 'select addit_type from additionals_type'
COUNT_SALESMANS = 'select count(*) from employees where position = 1'
SALESMAN_NAMES = 'SELECT name from employees where position = 1'
BEVERAGE_PRICE = 'SELECT price_bev from beverage_type where bev_type = ?'

class DataBase(object):

    def __init__(self, db=COFEE_DB):
        self.database = db
        try:
            self.conn = sqlite3.connect(db, check_same_thread=False)
        except sqlite3.Error as error:
            logger.error("Cannot connect to db {}".format(error))
        self.cursor = self.conn.cursor()


    def execute_query_get(self, query, param=None):
        info = 'Executing get query: {}, {}'.format(query, param)
        logger.info(info)
        with self.conn:
            if param:
                self.cursor.execute(query, param)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            logger.info('query successful')
            return result

    def get_beverage_types(self):
        query = BEVERAGE_TYPES
        res = self.execute_query_get(query)
        logger.info("On get_beverage_types -- result {}".format(res))
        return res

    def get_additionals_types(self):
        query = ADDITIONALS_TYPES
        res = self.execute_query_get(query)
        logger.info("On get_additionals_types -- result {}".format(res))
        return res

    def get_beverage_price(self, bev):
        query = 'SELECT price_bev from beverage_type where bev_type = ?'
        param = bev,
        res = self.execute_query_get(query, param)
        logger.info("On get_beverage_price -- result {}".format(res))
        return res

    def get_additinal_price(self, addit):
        query = 'SELECT price_addit from additionals_type where addit_type = ?'
        param = addit,
        res = self.execute_query_get(query, param)
        logger.info("On get_additinal_price -- result {}".format(res))
        return res

    def get_salesmans_names(self):
        query = SALESMAN_NAMES
        res = self.execute_query_get(query)
        logger.info("On get_salesmans_names -- result {}".format(res))
        return res

    def execute_query_post(self, query, param):
        info = 'Executing post query: {}, {}'.format(query, param)
        logger.info(info)
        self.cursor.execute(query, param)
        logger.info('post query successful')
        self.conn.commit()

    def check_user_in_db(self, user_name):
        name = user_name
        query = 'SELECT * FROM employees WHERE name = ?'
        param = name,
        result = self.execute_query_get(query, param)
        logger.info('User {}   '.format(user_name, 'exists' if result else 'does not exist'))
        return bool(result)

    def check_salesman_in_db(self, salesman_name):
        name = salesman_name
        query = 'SELECT * FROM employees WHERE name = ? and position = 1'
        param = name,
        result = self.execute_query_get(query, param)
        logger.info('Salesman  {} '.format(salesman_name, 'exists' if result else 'does not exist'))
        return bool(result)

    def check_manager_in_db(self, manager_name):
        name = manager_name
        query = 'SELECT * FROM employees WHERE name = ? and position = 2'
        param = name,
        result = self.execute_query_get(query, param)
        logger.info('Manager  {} '.format(manager_name, 'exists' if result else 'does not exist'))
        return bool(result)

    def add_user(self, user_info):
        if not self.check_user_in_db(user_info):
            query = 'INSERT INTO employees (name, position) VALUES (?,?)'
            param = user_info
            self.execute_query_post(query, param)
            logger.info('User {} position: {} was successfully added to db!'.format(user_info[0], user_info[1]))
        else:
            print('User {} already exist'.format(user_info[1]))


    def send_bill_to_db(self, bill_info):
        query = 'INSERT INTO sales (name, bill, salesdate) VALUES (?, ?, ?)'
        self.execute_query_post(query, bill_info)
        logger.info('Salesman {}, bill {}.'.format(bill_info[0], bill_info[1]))

    def count_salesmans(self):
        query = COUNT_SALESMANS
        res = self.execute_query_get(query)
        logger.info("On count_salesmans -- result {}".format(res))
        return res

    def salesnumber_of_salesman(self, salesman_name):
        query = 'SELECT COUNT(*) FROM sales where name = ?'
        param = salesman_name,
        res = self.execute_query_get(query, param)
        logger.info("On salesnumber_of_salesman -- result {}".format(res))
        return res

    def total_number_of_sales(self):
        query = 'SELECT COUNT(*) FROM sales'
        res = self.execute_query_get(query)
        logger.info("On total_number_of_sales -- result {}".format(res))
        return res

    def salessum_of_salesman(self, salesman_name):
        query = 'SELECT SUM(bill) FROM sales where name = ?'
        param = salesman_name,
        res = self.execute_query_get(query, param)
        if self.execute_query_get(query, param)[0][0] == None:
            res = [(0,)]
        logger.info("On salessum_of_manager -- result {}".format(res))
        return res

    def total_sum(self):
        query = 'SELECT SUM(bill) FROM sales'
        res = self.execute_query_get(query)
        logger.info("On total sum -- result {}".format(res))
        return res

