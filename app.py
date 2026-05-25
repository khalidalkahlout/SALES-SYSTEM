from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('store_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. جلب المنتجات (GET)
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    
    output = []
    for p in products:
        output.append({
            "product_id": p['product_id'],
            "product_name": p['product_name'],
            "category": p['category'],
            "price": p['price'],
            "stock": p['stock']
        })
    return jsonify(output)

# 2. بيع المنتج وتسجيل البيع (POST)
@app.route('/sell_product/<int:product_id>', methods=['POST'])
def sell_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT stock, price FROM products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    
    if product and product['stock'] > 0:
        # خصم من المخزن
        new_stock = product['stock'] - 1
        cursor.execute("UPDATE products SET stock = ? WHERE product_id = ?", 
                      (new_stock, product_id))
        
        # تسجيل البيع في جدول Sales
        cursor.execute("""
            INSERT INTO Sales (product_id, employee_id, quantity, total_price) 
            VALUES (?, ?, ?, ?)
        """, (product_id, 101, 1, product['price']))
        
        conn.commit()
        conn.close()
        return jsonify({
            "status": "success", 
            "message": "تم البيع وتسجيله في السجلات!",
            "new_stock": new_stock
        }), 200
    else:
        conn.close()
        return jsonify({
            "status": "error", 
            "message": "المنتج غير متوفر أو نفذ!"
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)