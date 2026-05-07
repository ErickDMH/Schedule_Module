-- Full Schema Snapshot

CREATE SCHEMA IF NOT EXISTS schedule_module;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DO $$ BEGIN
    CREATE TYPE schedule_module.recurrency_type AS ENUM (
        'daily',
        'weekly',
        'biweekly',
        'monthly',
        'custom_days'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE schedule_module.register_type AS ENUM (
        'event',
        'schedule'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS schedule_module.schema_version (
    version INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schedule_module.category (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    color VARCHAR(50),
    icon VARCHAR(255),
    image VARCHAR(255),
    note TEXT,
    creation_date_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_date_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schedule_module.scheduled_routine (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    category_id UUID REFERENCES schedule_module.category(id) ON DELETE SET NULL,
    start_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    description TEXT,
    note TEXT,
    recurrency schedule_module.recurrency_type NOT NULL,
    creation_date_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_date_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schedule_module.date_register (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type schedule_module.register_type NOT NULL,
    name VARCHAR(255) NOT NULL,
    start_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    description TEXT,
    note TEXT,
    category_id UUID REFERENCES schedule_module.category(id) ON DELETE SET NULL,
    scheduled_routine_id UUID REFERENCES schedule_module.scheduled_routine(id) ON DELETE SET NULL,
    relationship_field VARCHAR(255),
    creation_date_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    update_date_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_date_register_relationship ON schedule_module.date_register(relationship_field);
CREATE INDEX IF NOT EXISTS idx_date_register_start_end ON schedule_module.date_register(start_date_time, end_date_time);
CREATE INDEX IF NOT EXISTS idx_scheduled_routine_start_end ON schedule_module.scheduled_routine(start_date_time, end_date_time);
