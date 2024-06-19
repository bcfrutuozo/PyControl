from database.db_base import DBBase
import sqlite3
from functions import encrypt_passphrase


class DBLogin(DBBase):

    def __init__(self, path):
        super().__init__(path)

    def check_login(self, username, password):
        db, cursor = self.open()
        try:

            # Check if the provided username and password match a record in the Users table
            cursor.execute("SELECT login, senha FROM usuarios WHERE login = ? AND senha = ?", (username, encrypt_passphrase(password)))
            result = cursor.fetchone()

            # If a matching record is found, return True for a successful login
            if result:
                return True

        except sqlite3.Error as e:
            # Handle any potential database errors here
            print("SQLite error:", e)

        finally:
            # Close the database connection
            self.close()

        # Return False for an unsuccessful login
        return False

    def register_user(self, name, username, email, password, security_question, security_answer, photo):
        db, cursor = self.open()
        try:
            # Create a Users table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS "usuarios" (
                    "id_usuario"	INTEGER NOT NULL,
                    "nome"	TEXT NOT NULL,
                    "login"	TEXT NOT NULL UNIQUE,
                    "email"	TEXT NOT NULL UNIQUE,
                    "senha"	TEXT NOT NULL,
                    "pergunta_secreta"	TEXT NOT NULL,
                    "resposta_secreta"	TEXT NOT NULL,
                    "foto"	BLOB NOT NULL,
                    PRIMARY KEY("id_usuario" AUTOINCREMENT)
                )
            ''')

            # Insert user data into the Users table
            cursor.execute('''
                INSERT INTO usuarios (nome, login, email, senha, pergunta_secreta, resposta_secreta, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, username, email, encrypt_passphrase(password), security_question, security_answer.lower(), photo))

            # Commit the changes and close the database connection
            db.commit()

            return True  # Registration successful

        except sqlite3.IntegrityError:
            return False  # Username or email is already in use

        finally:
            # Close the database connection
            self.close()

    def email_exists(self, email):
        db, cursor = self.open()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            user = cursor.fetchone()

            return user

        finally:
            # Close the database connection
            self.close()

    def update_password(self, email, temporary_password):
        db, cursor = self.open()
        try:
            # Update the user's password with the temporary password
            update_query = "UPDATE usuarios SET senha = ? WHERE email = ?"
            cursor.execute(update_query, (encrypt_passphrase(temporary_password), email))

            # Commit the changes to the database
            db.commit()

            return True  # Password updated successfully

        except Exception as e:
            print("Error updating password:", str(e))
            return False  # Password update failed

        finally:
            # Close the database connection
            self.close()

    def get_security_question(self, email):
        db, cursor = self.open()
        try:
            # Assuming you have a table called 'users' with columns 'email', 'security_question', and 'security_answer'
            cursor.execute("SELECT pergunta_secreta FROM usuarios WHERE email = ?", (email,))
            result = cursor.fetchone()

            if result:
                return result[0]  # Return the security question
            else:
                return None  # User not found or no security question associated with the email

        except sqlite3.Error as e:
            print("Database error:", str(e))
            return None
        finally:
            self.close()

    def check_security_answer(self, email, provided_answer):
        db, cursor = self.open()
        try:
            # Assuming you have a table called 'users' with columns 'email', 'security_question', and 'security_answer'
            cursor.execute("SELECT resposta_secreta FROM usuarios WHERE email = ?", (email,))
            result = cursor.fetchone()

            if result:
                stored_answer = result[0]
                # Compare the provided answer with the stored answer (case-insensitive)
                if provided_answer.lower() == stored_answer.lower():
                    return True  # Security answer matches
                else:
                    return False  # Security answer does not match
            else:
                return False  # User not found or no security answer associated with the email

        except sqlite3.Error as e:
            print("Database error:", str(e))
            return False
        finally:
            self.close()


DATABASE_LOGIN = DBLogin("database\\data.db")