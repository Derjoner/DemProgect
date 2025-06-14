import db
from math import floor

def calculate_product_quantity(product_type_id, material_type_id, material_quantity, param1, param2):

    if not isinstance(product_type_id, int) or not isinstance(material_type_id, int) or not isinstance(material_quantity, int):
        return -1
    if material_quantity < 0 or param1 <= 0 or param2 <= 0:
        return -1
    
    try:

        conn = db.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT type_coefficient FROM products_type WHERE id_product_type = %s", (product_type_id,))
        product_result = cursor.fetchone()
        if not product_result:
            cursor.close()
            conn.close()
            return -1
        product_coefficient = float(product_result[0])
        
        cursor.execute("SELECT loss_percentage FROM materials_type WHERE id_material_type = %s", (material_type_id,))
        material_result = cursor.fetchone()
        if not material_result:
            cursor.close()
            conn.close()
            return -1
        material_loss_percent = float(material_result[0])
        
        cursor.close()
        conn.close()
        
        material_per_unit = param1 * param2 * product_coefficient
        
        effective_material_quantity = material_quantity * (1 - material_loss_percent / 100)
        
        product_quantity = floor(effective_material_quantity / material_per_unit)
        
        return product_quantity
    
    except db.mysql.connector.Error:
        return -1

product_type_id = int(input("ID типа продукции: "))
material_type_id = int(input("ID типа материала: "))
material_quantity = int(input("Количество сырья: "))
param1 = float(input("Первый параметр: "))
param2 = float(input("Второй параметр: "))
print(calculate_product_quantity(product_type_id, material_type_id, material_quantity, param1, param2))