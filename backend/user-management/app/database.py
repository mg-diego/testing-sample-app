import psycopg2
from psycopg2 import sql
from typing import List, Optional, Dict

class UserManagementDatabase:
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

    def get_user(self, username: str) -> Optional[Dict]:
        query = sql.SQL("SELECT username, password, permissions FROM public.users WHERE username = %s;")
        
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()
                if user_data:
                    return {
                        "success": True,
                        "detail": {
                            "username": user_data[0],
                            "password": user_data[1],
                            "permissions": user_data[2]
                        }
                    }
                return {"success": False, "error": "User not found."}
        except Exception as e:
            return {"success": False, "error": e}
        finally:
            if conn:
                conn.close()

    def get_user_list(self) -> Optional[List[Dict]]:
        query = sql.SQL("SELECT username, password, permissions FROM public.users;")
        users = []
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query)
                user_data = cursor.fetchall()
                for row in user_data:
                    users.append({
                        "username": row[0],
                        "password": row[1],
                        "permissions": row[2]
                    })
            return {"success": True, "detail": users}
        except Exception as e:
            return {"success": False, "error": e}
        finally:
            if conn:
                conn.close()
    

    def create_user(self, username: str, password: str, permissions: str):
        query = sql.SQL("""
            INSERT INTO public.users (username, password, permissions)
            VALUES (%s, %s, %s);
        """)
        
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, (username, password, permissions))
                conn.commit()
                return {
                    "success": True,
                    "detail": {
                        "username": username,
                        "password": password,
                        "permissions": permissions
                    }
                }
        except Exception as e:
            return {"success": False, "error": e}
        finally:
            if conn:
                conn.close()

    def delete_user(self, username: str):
        query = sql.SQL("""
            DELETE FROM public.users
            WHERE username = %s;
        """)

        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, (username,))
                conn.commit()

                if cursor.rowcount == 0:
                    return {"success": False, "error": "User not found."}

                return {"success": True, "detail": ""}

        except Exception as e:
            return {"success": False, "error": str(e)}

        finally:
            if conn:
                conn.close()