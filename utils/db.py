from sqlalchemy import create_engine, text
from utils.config import DB_URL
from datetime import datetime

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

    def sms_verify(self, phone_number: str, otp: str, expires_at: datetime):
        """Inserting OTP verification record into the database."""
        with self.conn.connect() as connection:
            connection.execute(
                text("INSERT INTO sms_verifications (phone, otp, expires_at) VALUES (:phone, :otp, :expires_at)"),
                {"phone": phone_number, "otp": otp, "expires_at": expires_at}
            )
        return True
