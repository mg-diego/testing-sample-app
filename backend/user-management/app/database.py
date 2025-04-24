import psycopg2
from psycopg2 import sql
from typing import List, Optional, Dict

class UserManagementDatabase:
    def __init__(self):
        # Configuración de la base de datos
        self.db_host = "postgres"
        self.db_port = "5432"
        self.db_name = "users"
        self.db_user = "user"
        self.db_password = "password"

    def get_connection(self):
        """Obtiene una conexión a la base de datos PostgreSQL."""
        return psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

    def get_user(self, username: str) -> Optional[Dict]:
        """Obtiene los datos de un usuario por su nombre de usuario."""
        query = sql.SQL("SELECT id, username, password, permissions FROM public.users WHERE username = %s;")
        
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()  # Devuelve la primera fila
                if user_data:
                    return {
                        "id": user_data[0],
                        "username": user_data[1],
                        "password": user_data[2],
                        "permissions": user_data[3]
                    }
                return None  # Si no se encuentra el usuario
        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
        finally:
            if conn:
                conn.close()

    def get_user_list(self) -> Optional[List[Dict]]:
        query = sql.SQL("SELECT id, username, password, permissions FROM public.users;")
        users = []
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query)
                user_data = cursor.fetchall()
                for row in user_data:
                    users.append({
                        "id": row[0],
                        "username": row[1],
                        "password": row[2],
                        "permissions": row[3]
                    })
            return users if users else None
        except Exception as e:
            print(f"Error al obtener la lista de usuarios: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def create_user(self, username: str, password: str, permissions: str) -> bool:
        """Crea un nuevo usuario en la base de datos."""
        query = sql.SQL("""
            INSERT INTO public.users (username, password, permissions)
            VALUES (%s, %s, %s);
        """)
        
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, (username, password, permissions))
                conn.commit()  # Realiza la transacción
                return True
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
            return False
        finally:
            if conn:
                conn.close()
