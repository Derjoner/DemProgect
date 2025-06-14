import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='toor',
    database='furniture_company',
    charset='utf8mb4'
)

cursor = conn.cursor()

def import_material_types(filename):

    df = pd.read_excel(filename, sheet_name='Material_type_import')
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO materials_type (material_type, loss_percentage)
            VALUES (%s, %s)
        """, (row['Тип материала'].strip(), row['Процент потерь сырья'] * 100 ))
    conn.commit()

def import_materials(filename):

    cursor.execute("SELECT id_material_type, material_type FROM materials_type")
    type_map = {name: mid for mid, name in cursor.fetchall()}

    df = pd.read_excel(filename, sheet_name='Materials_import')
    df['Тип материала'] = df['Тип материала'].str.strip()
    df['id_material_type'] = df['Тип материала'].map(type_map)
    df = df.rename(columns={
        'Наименование материала': 'name',
        'Цена единицы материала': 'unit_price',
        'Количество на складе': 'in_stock',
        'Минимальное количество': 'min_stock',
        'Количество в упаковке': 'pack_size',
        'Единица измерения': 'unit'
    })
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO materials
            (name, id_material_type, unit_price, in_stock, min_stock, pack_size, unit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['name'], row['id_material_type'], row['unit_price'],
            row['in_stock'], row['min_stock'], row['pack_size'], row['unit']
        ))
    conn.commit()

def import_product_types(filename):
    df = pd.read_excel(filename, sheet_name='Product_type_import')
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO products_type (product_type, type_coefficient)
            VALUES (%s, %s)
        """, (row['Тип продукции'].strip(), row['Коэффициент типа продукции']))
    conn.commit()

def import_products(filename):
    cursor.execute("SELECT id_product_type, product_type FROM products_type")
    type_map = {name: pid for pid, name in cursor.fetchall()}

    df = pd.read_excel(filename, sheet_name='Products_import')
    df['id_product_type'] = df['Тип продукции'].str.strip().map(type_map)
    df = df.rename(columns={
        'Наименование продукции': 'name',
        'Артикул': 'article',
        'Минимальная стоимость для партнера': 'min_partner_price'
    })
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO products
            (id_product_type, name, article, min_partner_price)
            VALUES (%s, %s, %s, %s)
        """, (row['id_product_type'], row['name'], row['article'], row['min_partner_price']))
    conn.commit()


def import_material_products(filename):
    cursor.execute("SELECT id_material, name FROM materials")
    material_map = {name.strip(): mid for mid, name in cursor.fetchall()}

    cursor.execute("SELECT id_product, name FROM products")
    product_map = {name.strip(): pid for pid, name in cursor.fetchall()}

    df = pd.read_excel(filename, sheet_name='Material_products__import')
    df['id_material'] = df['Наименование материала'].str.strip().map(material_map)
    df['id_product'] = df['Продукция'].str.strip().map(product_map)
    df = df.rename(columns={
        'Необходимое количество материала': 'qty_per_unit'
    })
    for _, row in df.iterrows():
        if pd.notnull(row['id_material']) and pd.notnull(row['id_product']):
            cursor.execute("""
                INSERT INTO material_products (id_material, id_product, qty_per_unit)
                VALUES (%s, %s, %s)
            """, (row['id_material'], row['id_product'], row['qty_per_unit']))
    conn.commit()

import_material_types('C:\\Users\\admin\\Desktop\\№6-ДЭМ 25\\2 смена\\Прил_В5_КОД 09.02.07-2-2025-ПУ (3)\\Прил_В5_КОД 09.02.07-2-2025-ПУ\\Ресурсы\\Material_type_import.xlsx')
import_materials('C:\\Users\\admin\\Desktop\\№6-ДЭМ 25\\2 смена\\Прил_В5_КОД 09.02.07-2-2025-ПУ (3)\\Прил_В5_КОД 09.02.07-2-2025-ПУ\\Ресурсы\\Materials_import.xlsx')
import_product_types('C:\\Users\\admin\\Desktop\\№6-ДЭМ 25\\2 смена\\Прил_В5_КОД 09.02.07-2-2025-ПУ (3)\\Прил_В5_КОД 09.02.07-2-2025-ПУ\\Ресурсы\\Product_type_import.xlsx')
import_products('C:\\Users\\admin\\Desktop\\№6-ДЭМ 25\\2 смена\\Прил_В5_КОД 09.02.07-2-2025-ПУ (3)\\Прил_В5_КОД 09.02.07-2-2025-ПУ\\Ресурсы\\Products_import.xlsx')
import_material_products('C:\\Users\\admin\\Desktop\\№6-ДЭМ 25\\2 смена\\Прил_В5_КОД 09.02.07-2-2025-ПУ (3)\\Прил_В5_КОД 09.02.07-2-2025-ПУ\\Ресурсы\\Material_products__import.xlsx')

cursor.close()
conn.close()
