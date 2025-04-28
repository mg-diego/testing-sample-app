import psycopg2
from psycopg2 import sql
from typing import List, Optional, Dict

class LanguageManagementDatabase:
    def __init__(self):
        # Configuración de la base de datos
        self.db_host = "postgres"
        self.db_port = "5432"
        self.db_name = "testing-sample-app"
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

    def get_active_language(self) -> Optional[Dict]:
        """Obtiene el idioma activo."""
        query = sql.SQL("SELECT language FROM public.languages WHERE active = TRUE;")
        
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, )
                language_data = cursor.fetchone()  # Devuelve la primera fila
                if language_data:
                    return language_data[0]
                return None  # Si no se encuentra el usuario
        except Exception as e:
            print(f"Error al obtener el idioma activo: {e}")
        finally:
            if conn:
                conn.close()

    def set_active_language(self, language_code: str) -> bool:
        """
        Establece el idioma activo al proporcionado y desactiva los demás.
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                # Set all languages to inactive
                cursor.execute("UPDATE public.languages SET active = FALSE;")
                
                # Set the selected language to active
                cursor.execute(
                    "UPDATE public.languages SET active = TRUE WHERE language = %s;",
                    (language_code,)
                )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al establecer el idioma activo: {e}")
            return False
        finally:
            if conn:
                conn.close()