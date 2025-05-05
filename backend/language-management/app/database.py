import psycopg2
from psycopg2 import sql
from typing import Optional, Dict

class LanguageManagementDatabase:
    def __init__(self):
        self.db_host = "postgres"
        self.db_port = "5432"
        self.db_name = "testing-sample-app"
        self.db_user = "user"
        self.db_password = "password"

    def get_connection(self):
        return psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )

    def get_active_language(self) -> Optional[Dict]:
        query = sql.SQL("SELECT language FROM public.languages WHERE active = TRUE;")
        
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, )
                language_data = cursor.fetchone()  # Devuelve la primera fila
                if language_data:
                    return {"success": True, "detail": language_data[0] }
                else:
                    return {"success": False, "error": "No language is configured." }
                
        except Exception as e:
            return {"success": False, "error": e}
        finally:
            if conn:
                conn.close()

    def set_active_language(self, language_code: str) -> bool:
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
            return {"success": True, "detail": "" }
        except Exception as e:
            return {"success": False, "error": e}
        finally:
            if conn:
                conn.close()