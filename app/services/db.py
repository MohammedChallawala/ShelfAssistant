import sqlite3
from typing import List, Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime

class DatabaseService:
    def __init__(self, db_path: str = "shelf_assistant.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                price REAL,
                stock_quantity INTEGER DEFAULT 0,
                shelf_location TEXT,
                barcode TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_product(self, product_data: Dict[str, Any]) -> int:
        """Create a new product and return its ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Remove id if present in product_data
        product_data.pop('id', None)
        product_data['created_at'] = datetime.now().isoformat()
        product_data['updated_at'] = datetime.now().isoformat()
        
        columns = ', '.join(product_data.keys())
        placeholders = ', '.join(['?' for _ in product_data])
        values = list(product_data.values())
        
        query = f"INSERT INTO products ({columns}) VALUES ({placeholders})"
        cursor.execute(query, values)
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_product(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get a product by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all products"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM products ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> bool:
        """Update a product by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Remove id and timestamps from update data
        product_data.pop('id', None)
        product_data.pop('created_at', None)
        product_data['updated_at'] = datetime.now().isoformat()
        
        if not product_data:
            conn.close()
            return False
        
        set_clause = ', '.join([f"{key} = ?" for key in product_data.keys()])
        values = list(product_data.values()) + [product_id]
        
        query = f"UPDATE products SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        rows_affected = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search products by name or description"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        search_query = f"%{query}%"
        cursor.execute("""
            SELECT * FROM products 
            WHERE name LIKE ? OR description LIKE ? OR category LIKE ?
            ORDER BY id
        """, (search_query, search_query, search_query))
        
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        return []

# Global database service instance
db_service = DatabaseService()
