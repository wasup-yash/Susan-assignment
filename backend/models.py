from pydantic import BaseModel
from typing import List
from datetime import datetime
import mysql.connector
from mysql.connector import Error

# MySQL connection setup
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='susans_sushi_shop',
            user='susan',  
            password='SushiShopOfSusan' 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

class Product(BaseModel):
    name: str
    description: str
    price: float

#The cart_items table stores individual items in each order to maintain the persistance of DB tables
class CartItem(BaseModel):
    product: Product
    quantity: int

class Order(BaseModel):
    customer_name: str
    items: List[CartItem] = []

def add_to_cart(order: Order):
    order_date = datetime.now()
    total_price = 0
    total_quantity = 0

    for item in order.items:
        quantity = item.quantity
        price = 3 if item.sushi_type == 'Sushi A' else 4
        total_price += quantity * price
        total_quantity += quantity
        items.append((item.sushi_type, quantity, price))

    discount_name, discount_amount, final_price = calculate_discount(total_quantity, total_price)

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO orders (customer_name, order_date, total_price, discount_applied, final_price) 
        VALUES (%s, %s, %s, %s, %s)
        ''', (order.customer_name, order_date, total_price, discount_name, final_price))
        order_id = cursor.lastrowid

        for item in items:
            cursor.execute('''
            INSERT INTO order_items (order_id, sushi_type, quantity, price) 
            VALUES (%s, %s, %s, %s)
            ''', (order_id, item[0], item[1], item[2]))

        connection.commit()
        cursor.close()
        connection.close()

        return {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "items": items,
        "total_price": total_price,
        "discount_applied": discount_name,
        "final_price": final_price
        }
    else:
        raise HTTPException(status_code=500, detail="Database connection failed")


def remove_product(self, product_name: Order):
        self.items = [item for item in self.items if item.Order.name != product_name]

# for calculating the discounts of the sushi and we are considering applying the discount consecutively not stacking the discounts
def calculate_discount(quantity, total_price):
    discount = 0
    discount_name = ""
    
    if quantity >= 20:
        discount = 0.20
        discount_name = "20 Deal"
    elif quantity >= 10:
        discount = 0.10
        discount_name = "10 Deal"

    now = datetime.now()
    if 11 <= now.hour < 14:
        discount += 0.20
        discount_name += " & Lunch Deal"

    final_price = total_price * (1 - discount)
    return discount_name, total_price * discount, final_price 

def fetch_orders_from_db():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        
        result = []
        for order in orders:
            cursor.execute('SELECT * FROM order_items WHERE order_id = %s', (order['id'],))
            items = cursor.fetchall()
            order_details = {
                "order_id": order['id'],
                "customer_name": order['customer_name'],
                "order_date": order['order_date'],
                "items": items,
                "total_price": order['total_price'],
                "discount_applied": order['discount_applied'],
                "final_price": order['final_price']
            }
            result.append(order_details)

        cursor.close()
        connection.close()
        return result
    else:
        raise HTTPException(status_code=500, detail="Database connection failed")