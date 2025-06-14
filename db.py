import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost', user='root', password='toor',
        database='furniture_company', charset='utf8mb4'
    )

def fetch_all_materials():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.id_material, m.name, mt.material_type AS type,
               m.in_stock, m.min_stock, m.pack_size AS pack_qty,
               m.unit, m.unit_price AS price,
               IFNULL(SUM(mp.qty_per_unit),0) AS required
        FROM materials m
        JOIN materials_type mt ON m.id_material_type = mt.id_material_type
        LEFT JOIN material_products mp ON m.id_material = mp.id_material
        GROUP BY m.id_material
        ORDER BY m.name
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            'id': mid, 'type': mtype, 'name': name, 'stock': float(stock),
            'min_stock': float(min_stock), 'pack_qty': float(pack_qty),
            'unit': unit, 'price': float(price), 'required': float(required)
        } for mid, name, mtype, stock, min_stock, pack_qty, unit, price, required in rows
    ]
    
def fetch_products_by_material(id_material):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name, mp.qty_per_unit
        FROM products p
        JOIN material_products mp ON p.id_product = mp.id_product
        WHERE mp.id_material = %s
        ORDER BY p.name
    """, (id_material,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'name': name, 'qty_per_unit': float(qty)} for name, qty in rows]

def fetch_material_types():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_material_type, material_type FROM materials_type")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return {name: mid for mid, name in rows}

def fetch_material_product(id_material, id_product):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.name, m.name as mname, mp.qty_per_unit
        FROM products p
        JOIN material_products mp ON p.id_product = mp.id_product
        JOIN materials m ON m.id_material = mp.id_material
        WHERE mp.id_material = %s AND mp.id_product = %s
        ORDER BY p.name
    """, (id_material, id_product,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'name': name, 'mname': mname, 'qty_per_unit': float(qty)} for name, mname, qty in rows]