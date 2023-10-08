CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(10) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    gst_number varchar(20),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE delivery_personnels (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    vehicle_type VARCHAR(20),
    vehicle_registration VARCHAR(20),
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    line VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    pincode VARCHAR(6),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
