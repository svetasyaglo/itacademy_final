from flask import Flask, jsonify, request, make_response, render_template, abort, flash, redirect, url_for, session
import time
from final_coffee_db import DataBase
from logs import logger



app = Flask(__name__, template_folder='templates')

db = DataBase()

@app.route('/')
def home():
    logger.info("Web - selecting user role")
    return render_template('position_selection_new.html')

@app.route('/salesman')
def login_salesman():
    logger.info("Web - salesman role selected")
    return render_template('salesman.html')


@app.route('/salesman', methods=['POST'])
def validate_salesman():
    name = request.form['sname']
    logger.info("Web - salesman {} logged in".format(name))
    if db.check_salesman_in_db(name):
        return redirect(url_for('select_beverage', name=name))

@app.route('/<name>/beverage', methods=["GET"])
def select_beverage(name):
    to_send = db.get_beverage_types()
    logger.info("Web - beverage selection")
#    print('beverages from bd {}  '.format(to_send))
    return render_template('beverage_selection.html', to_send=to_send, name=name)


bev_types = [i[0] for i in db.get_beverage_types()]

@app.route('/<name>/<bev>', methods=['GET'])
def additionals_to_beverages(name, bev):
    if bev in bev_types:
#        print('beverage selected in GET {}  '.format(bev))
        to_send1 = db.get_additionals_types()
#        print('additionals from bd {}  '.format(to_send1))
        logger.info("Web - additionals selection")
        return render_template('additional_selection.html', to_send1=to_send1, beverage=bev, name=name)


addit_types = [i[0] for i in db.get_additionals_types()]

@app.route('/<name>/<bev>/<addit>', methods=['GET'])
def addit_bill(name, addit, bev):
    if addit in addit_types and bev in bev_types:
#        print('additional selected in GET {}  '.format(addit))
        logger.info("Web - requesting bill")
        return render_template('items_selected_bill.html', additional=addit, beverage=bev, name=name)


@app.route('/<name>/<bev>/<addit>/bill', methods=['GET'])
def get_bill(name, addit, bev):
    bev_price = db.get_beverage_price(bev)[0][0]
#    print("beverage price {}".format(bev_price))
    addit_price = db.get_additinal_price(addit)[0][0]
#    print("additional price {}".format(addit_price))
    bill = bev_price + addit_price
#    print("bill {}".format(bill))
    logger.info("Web - for beverage {} and additional {} price {} ".format(bev, addit, bill))
    return render_template('bill.html', bill=bill, additional=addit, beverage=bev, name=name)

@app.route('/<name>/<bev>/<addit>/bill', methods=['POST'])
def send_bill(name, addit, bev):
    bev_price = db.get_beverage_price(bev)[0][0]
    addit_price = db.get_additinal_price(addit)[0][0]
    bill = bev_price + addit_price
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    bill_info = (name, bill, date)
    db.send_bill_to_db(bill_info)
    logger.info("order sent to db, bill {}".format(bill_info))
    return redirect(url_for('select_beverage', name=name))


@app.route('/manager')
def login_manager():
    logger.info("Web - manager role selected")
    return render_template('manager.html')


@app.route('/manager', methods=['POST'])
def validate_manager():
    _mname = request.form['mname']
    logger.info('Web -- manager from site {}  '.format(_mname))
    if db.check_manager_in_db((_mname)):
        return redirect(url_for('manage_sales'))


@app.route('/manager/sales', methods=["GET"])
def manage_sales():
    salesman_list = [i[0] for i in db.get_salesmans_names()]
#    print("salesman_list {}".format(salesman_list))
    salesman_count = db.count_salesmans()[0][0]
#    print("salesman_count {}".format(salesman_count))

    bill_count = [db.salesnumber_of_salesman(salesman)[0][0] for salesman in salesman_list]
#    print("bill counts {} ".format(bill_count))

#    total_sum_salesman = [db.salessum_of_manager(salesman)[0][0] for salesman in salesman_list]
    total_sum_salesman = [round(db.salessum_of_salesman(salesman)[0][0], 2) for salesman in salesman_list]
#    print("total sum for every salesman {} ".format(total_sum_salesman))

    total_number_of_sales = sum(bill_count)
#    print("total number of sales {} ".format(total_number_of_sales))

    total_sum = round(sum(total_sum_salesman),2)
#    print("total sum {} ".format(total_sum))

    data = [[salesman_list[i], bill_count[i], total_sum_salesman[i]] for i in range(salesman_count)]

    data.append(['Total', total_number_of_sales, total_sum])
    print("data {}".format(data))

    logger.info('Web -- manager requested sales data {}  '.format(data))
    return render_template('manager_sales.html', table_rows=data)



if __name__ == '__main__':
    app.run(debug=True)
