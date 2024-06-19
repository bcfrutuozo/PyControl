from database.db_base import DBBase
import sqlite3
from functions import encrypt_passphrase


class DBCliente(DBBase):

    def __init__(self, path):
        super().__init__(path)

    def selecionar_todos(self):
        db, cursor = self.open()
        try:

            # Check if the provided username and password match a record in the Users table
            cursor.execute("SELECT id_cliente, nome, email, ddd, telefone FROM clientes ORDER BY id_cliente")
            result = cursor.fetchall()

            # If a matching record is found, return True for a successful login
            if result:
                return result

        except sqlite3.Error as e:
            # Handle any potential database errors here
            print("SQLite error:", e)

        finally:
            # Close the database connection
            self.close()

        # Return False for an unsuccessful login
        return None

    def selecionar_todas_fotos(self):
        db, cursor = self.open(bytes) # Open with byte stream
        try:

            # Check if the provided username and password match a record in the Users table
            cursor.execute("SELECT foto FROM clientes ORDER BY id_cliente")
            result = cursor.fetchone()

            # If a matching record is found, return True for a successful login
            if result:
                return result

        except sqlite3.Error as e:
            # Handle any potential database errors here
            print("SQLite error:", e)

        finally:
            # Close the database connection
            self.close()

        # Return False for an unsuccessful login
        return None

    def register_user(self, name, username, email, password, security_question, security_answer, photo):
        db, cursor = self.open()
        try:
            # Create a Users table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS "Users" (
                    "id_user"	INTEGER NOT NULL,
                    "name"	TEXT NOT NULL,
                    "username"	TEXT NOT NULL UNIQUE,
                    "email"	TEXT NOT NULL UNIQUE,
                    "password"	TEXT NOT NULL,
                    "security_question"	TEXT NOT NULL,
                    "security_answer"	TEXT NOT NULL,
                    "photo"	BLOB NOT NULL,
                    PRIMARY KEY("id_user" AUTOINCREMENT)
                )
            ''')

            # Insert user data into the Users table
            cursor.execute('''
                INSERT INTO Users (name, username, email, password, security_question, security_answer, photo)
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
            cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
            user = cursor.fetchone()

            return user

        finally:
            # Close the database connection
            self.close()

    def update_password(self, email, temporary_password):
        db, cursor = self.open()
        try:
            # Update the user's password with the temporary password
            update_query = "UPDATE Users SET password = ? WHERE email = ?"
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
            cursor.execute("SELECT security_question FROM users WHERE email = ?", (email,))
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
            cursor.execute("SELECT security_answer FROM users WHERE email = ?", (email,))
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


DATABASE_CLIENTE = DBCliente("database\\data.db")