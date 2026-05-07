-- Seed data (optional)
-- Useful for testing or base categories

INSERT INTO schedule_module.category (id, name, description, color, icon)
VALUES 
  ('00000000-0000-0000-0000-000000000001', 'Default', 'Default category', '#cccccc', 'default-icon'),
  ('00000000-0000-0000-0000-000000000002', 'Work', 'Work related events', '#0000ff', 'work-icon')
ON CONFLICT DO NOTHING;
