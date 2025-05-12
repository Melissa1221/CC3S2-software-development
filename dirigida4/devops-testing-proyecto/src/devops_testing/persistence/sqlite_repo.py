"""Implementación de repositorios con SQLite."""

import os
import sqlite3
from decimal import Decimal
from typing import List
from ..models import User, Payment
from ..repositories import UserRepository, PaymentRepository

class SQLitePaymentRepository:
    """Repositorio de pagos que usa SQLite."""
    
    def __init__(self, db_path: str):
        """
        Inicializa el repositorio.
        
        Args:
            db_path: Ruta al archivo SQLite
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializa la base de datos si no existe."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla de pagos si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id TEXT PRIMARY KEY,
            amount TEXT,
            currency TEXT,
            user_id TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add(self, payment: Payment) -> None:
        """
        Añade un pago al repositorio.
        
        Args:
            payment: Pago a añadir
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO payments (id, amount, currency, user_id) VALUES (?, ?, ?, ?)",
            (payment.id, str(payment.amount), payment.currency, payment.user_id)
        )
        
        conn.commit()
        conn.close()
    
    def list_by_user(self, user_id: str) -> List[Payment]:
        """
        Obtiene todos los pagos de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de pagos del usuario
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, amount, currency, user_id FROM payments WHERE user_id = ?",
            (user_id,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            Payment(
                id=row[0],
                amount=Decimal(row[1]),
                currency=row[2],
                user_id=row[3]
            )
            for row in results
        ]

class SQLiteUserRepository:
    """Repositorio de usuarios que usa SQLite."""
    
    def __init__(self, db_path: str):
        """
        Inicializa el repositorio.
        
        Args:
            db_path: Ruta al archivo SQLite
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Inicializa la base de datos si no existe."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla de usuarios si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add(self, user: User) -> None:
        """
        Añade un usuario al repositorio.
        
        Args:
            user: Usuario a añadir
            
        Raises:
            KeyError: Si el usuario ya existe
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (id, username, email) VALUES (?, ?, ?)",
                (user.id, user.username, user.email)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise KeyError(f"Usuario duplicado: {user.username}")
        finally:
            conn.close()
    
    def get(self, username: str) -> User:
        """
        Obtiene un usuario por su nombre de usuario.
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Usuario encontrado
            
        Raises:
            KeyError: Si el usuario no existe
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ?",
            (username,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result is None:
            raise KeyError(f"Usuario no encontrado: {username}")
        
        return User(
            id=result[0],
            username=result[1],
            email=result[2]
        ) 