CREATE SCHEMA IF NOT EXISTS schedule_module;

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
