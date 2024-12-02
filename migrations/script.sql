-- Enable the UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    language VARCHAR(10) DEFAULT 'ru',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sms_verifications table
CREATE TABLE sms_verifications (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    phone VARCHAR(15) NOT NULL,
    otp VARCHAR(6) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- Create admins table
CREATE TABLE admins (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Create addresses table
CREATE TABLE addresses (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    user_id UUID REFERENCES users ON DELETE CASCADE,
    address TEXT NOT NULL,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create categories table
CREATE TABLE categories (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create dishes table
CREATE TABLE dishes (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    category_id UUID REFERENCES categories ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    weight INTEGER NOT NULL,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create feedback table
CREATE TABLE feedback (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    user_id UUID REFERENCES users ON DELETE CASCADE,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create orders table
CREATE TABLE orders (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    user_id UUID REFERENCES users ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'новый',
    total_price NUMERIC(10, 2) NOT NULL,
    address_id UUID REFERENCES addresses,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order_items table
CREATE TABLE order_items (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    order_id UUID REFERENCES orders ON DELETE CASCADE,
    dish_id UUID REFERENCES dishes ON DELETE CASCADE,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price NUMERIC(10, 2) NOT NULL
);

-- Create promo_codes table
CREATE TABLE promo_codes (
    id UUID DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    discount_type VARCHAR(10) NOT NULL CHECK (discount_type IN ('fixed', 'percent')),
    discount_value NUMERIC(10, 2) NOT NULL CHECK (discount_value > 0),
    valid_until TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
