import sqlite3

con = sqlite3.connect("CoffeeForMeDB.db")
c = con.cursor()
# creating db structure + intial data

CoffeeForMeDB_intial = """
    create table if not exists employees(employee_id primary key, name VARCHAR(24), position INT);
    create table if not exists beverage_type(bev_type VARCHAR(36), price_bev REAL);
    create table if not exists additionals_type(addit_type VARCHAR(36), price_addit REAL);
    create table if not exists sales(employee_id INT, name VARCHAR(24), bill REAL, salesdate DATE);

    insert into employees values (1, 'John', 1);
    insert into employees values (3, 'Ann', 1);
    insert into employees values (4, 'Ted', 1);
    insert into employees values (2, 'Mary', 2);
    insert into beverage_type values ('coffee Espresso', 1);
    insert into beverage_type values ('coffee Americano', 2);
    insert into beverage_type values ('coffee Raf', 3);
    insert into beverage_type values ('coffee Cappuccino', 4);
    insert into beverage_type values ('coffee Latte', 5);
    insert into beverage_type values ('tea Black', 0.5);
    insert into beverage_type values ('tea Green', 0.5);
    insert into additionals_type values ('Sugar', 0.1);
    insert into additionals_type values ('Double Sugar', 0.2);
    insert into additionals_type values ('Cream', 0.3);
    insert into additionals_type values('Cinnamon', 0.4);
    insert into additionals_type values('Lemon', 0.1);
    insert into additionals_type values('Cognac', 1.3);
    insert into additionals_type values('Cherry liqueur', 0.8);
    insert into additionals_type values('none', 0.0);
    """

c.executescript(CoffeeForMeDB_intial)

