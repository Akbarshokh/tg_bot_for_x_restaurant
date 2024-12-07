import logging
from sqlalchemy import create_engine, text

from utils.config import DB_URL
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class PgConn:
    def __init__(self):
        self.conn = create_engine(DB_URL)
    
    def create_tables(self):
        self.conn.execute("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            name VARCHAR(50) NOT NULL,
            phone VARCHAR(15) NOT NULL UNIQUE,
            language VARCHAR(10) DEFAULT 'ru',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS sms_verifications (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            phone VARCHAR(15) NOT NULL,
            otp VARCHAR(6) NOT NULL,
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL
        );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS admins (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE,
            name VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW() NOT NULL
        );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS addresses (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            user_id UUID REFERENCES users ON DELETE CASCADE,
            address TEXT NOT NULL,
            latitude NUMERIC(9, 6),
            longitude NUMERIC(9, 6),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")


        self.conn.execute("""CREATE TABLE IF NOT EXISTS categories (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")


        self.conn.execute("""CREATE TABLE IF NOT EXISTS dishes (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            category_id UUID REFERENCES categories ON DELETE CASCADE,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price NUMERIC(10, 2) NOT NULL,
            weight INTEGER NOT NULL,
            image_url VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            user_id UUID REFERENCES users ON DELETE CASCADE,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")


        self.conn.execute("""CREATE TABLE IF NOT EXISTS orders (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            user_id UUID REFERENCES users ON DELETE CASCADE,
            status VARCHAR(20) DEFAULT 'новый',
            total_price NUMERIC(10, 2) NOT NULL,
            address_id UUID REFERENCES addresses,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")


        self.conn.execute("""CREATE TABLE IF NOT EXISTS order_items (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            order_id UUID REFERENCES orders ON DELETE CASCADE,
            dish_id UUID REFERENCES dishes ON DELETE CASCADE,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            price NUMERIC(10, 2) NOT NULL
        );""")


        self.conn.execute("""CREATE TABLE IF NOT EXISTS promo_codes (
            id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
            code VARCHAR(20) NOT NULL UNIQUE,
            discount_type VARCHAR(10) NOT NULL CHECK (discount_type IN ('fixed', 'percent')),
            discount_value NUMERIC(10, 2) NOT NULL CHECK (discount_value > 0),
            valid_until TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );""")


    def generate_otp(self, phone_number: str, otp: str, expires_at: datetime):
        """Inserting OTP verification record into the database."""
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    connection.execute(
                        text(
                            "INSERT INTO sms_verifications (phone, otp, expires_at) VALUES (:phone, :otp, :expires_at)"),
                        {"phone": phone_number, "otp": otp, "expires_at": expires_at}
                    )
                logging.info("OTP record inserted successfully.")
            except Exception as e:
                logging.error(f"Error inserting OTP: {e}")
                return False

        return True

    def update_otp(self, phone_number: str, otp: str, expires_at: datetime):
        """
        Update the OTP and expiration time for the most recent record of a given phone number.
        """
        query = """
        UPDATE sms_verifications
        SET otp = :otp, expires_at = :expires_at
        WHERE phone = :phone AND created_at = (
            SELECT MAX(created_at) FROM sms_verifications WHERE phone = :phone
        )
        """
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    connection.execute(
                        text(query),
                        {"phone": phone_number, "otp": otp, "expires_at": expires_at}
                    )
                logging.info("Most recent OTP record updated successfully.")
            except Exception as e:
                logging.error(f"Error updating OTP: {e}")
                return False

        return True

    def get_otp_by_phone(self, phone_number: str):
        """Getting OTP verification record from the database."""
        with self.conn.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT otp, expires_at, is_verified FROM sms_verifications WHERE phone = :phone ORDER BY created_at DESC LIMIT 1"),
                {"phone": phone_number}
            ).fetchone()

        return result


    def verify_otp(self, phone_number: str, otp: str):
        """Verifying OTP verification record from the database."""
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    result = connection.execute(
                        text("UPDATE sms_verifications SET is_verified = true WHERE phone = :phone AND otp = :otp"),
                        {"phone": phone_number, "otp": otp}
                    )
                if result.rowcount == 0:
                    logging.error("OTP not found or already verified.")
                    return False
                logging.info("OTP verified successfully.")
                return True
            except Exception as e:
                logging.error(f"Error verifying OTP: {e}")
                return False

    def save_user(self, user_data: dict):
        """Saves or updates a user in the database."""
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    result = connection.execute(
                        text("SELECT name, phone, language FROM users WHERE telegram_id = :telegram_id"),
                        {"telegram_id": user_data["telegram_id"]}
                    ).fetchone()

                    if result:
                        # Extract existing user details
                        existing_name, existing_phone, existing_language = result

                        # Check if the data is the same
                        if (
                                existing_name == user_data["name"]
                                and existing_phone == user_data["phone"]
                                and existing_language == user_data["language"]
                        ):
                            return "already_registered"

                        # Update the user if the data is different
                        connection.execute(
                            text(
                                "UPDATE users SET name = :name, phone = :phone, language = :language "
                                "WHERE telegram_id = :telegram_id"
                            ),
                            user_data
                        )
                        return "updated"
                    else:
                        # Insert a new user
                        connection.execute(
                            text(
                                "INSERT INTO users (telegram_id, name, phone, language) VALUES (:telegram_id, :name, :phone, :language)"
                            ),
                            user_data
                        )
                        return "inserted"
            except Exception as e:
                logging.error(f"Error saving user: {e}")
                return "error", str(e)

    def get_user_lang(self, telegram_id: int):
        """Getting User preferred language from the database."""
        with self.conn.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT language FROM users WHERE telegram_id = :telegram_id"),
                {"telegram_id": telegram_id}
            ).fetchone()

        return result

    def get_user_data(self, telegram_id: str):
        """Getting users data from the database."""
        with self.conn.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT id, name, language, phone FROM users WHERE telegram_id = :telegram_id"),
                {"telegram_id": telegram_id}
            ).fetchone()

        return result

    def update_user_name(self, telegram_id: int, new_name: str):
        """Updating users name from the database."""
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    result = connection.execute(
                        text("UPDATE users SET name = :new_name WHERE telegram_id = :telegram_id"),
                        {"new_name": new_name, "telegram_id": telegram_id}
                    )
                if result.rowcount == 0:
                    logging.error(f"No user found, {new_name}, {telegram_id}")
                    return False
                logging.info(f"Name {new_name}, {telegram_id} updated successfully.")
                return True
            except Exception as e:
                logging.error(f"Error: {e}, {telegram_id}, {new_name}")
                return False

    def update_user_phone(self, telegram_id: int, new_phone: str):
        """Updating users phone from the database."""
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    result = connection.execute(
                        text("UPDATE users SET phone = :new_phone WHERE telegram_id = :telegram_id"),
                        {"new_phone": new_phone, "telegram_id": telegram_id}
                    )
                if result.rowcount == 0:
                    logging.error(f"No user found, {new_phone}, {telegram_id}")
                    return False
                logging.info(f"Phone {new_phone}, {telegram_id} updated successfully.")
                return True
            except Exception as e:
                logging.error(f"Error: {e}, {telegram_id}, {new_phone}")
                return False

    def update_user_language(self, telegram_id: int, new_language: str):
        """Updating users language from the database."""
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    result = connection.execute(
                        text("UPDATE users SET language = :new_language WHERE telegram_id = :telegram_id"),
                        {"new_language": new_language, "telegram_id": telegram_id}
                    )
                if result.rowcount == 0:
                    logging.error(f"No user found, {new_language}, {telegram_id}")
                    return False
                logging.info(f"Language {new_language}, {telegram_id} updated successfully.")
                return True
            except Exception as e:
                logging.error(f"Error: {e}, {telegram_id}, {new_language}")
                return False

    def save_feedback(self, db_user_id: str, user_name: str, message: str):
        """Inserting feedback into the database."""
        with self.conn.connect() as connection:
            try:
                with connection.begin():
                    connection.execute(
                        text(
                            "INSERT INTO feedback (user_id, user_name, message) VALUES (:user_id, :user_name, :message)"),
                        {"user_id": db_user_id, "user_name": user_name, "message": message}
                    )
                logging.info(f"Feedback inserted successfully. User: {user_name}, Feedback: {message}")
            except Exception as e:
                logging.error(f"Error inserting: {e}, User: {user_name}, Feedback: {message}")
                return False

        return True
