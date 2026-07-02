exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.sql(`
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'loans_customer_id_fkey'
      ) THEN
        ALTER TABLE loans
          ADD CONSTRAINT loans_customer_id_fkey
          FOREIGN KEY (customer_id) REFERENCES customers(id);
      END IF;

      IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'loans_property_id_fkey'
      ) THEN
        ALTER TABLE loans
          ADD CONSTRAINT loans_property_id_fkey
          FOREIGN KEY (property_id) REFERENCES properties(id);
      END IF;
    END
    $$;
  `);
};

exports.down = (pgm) => {
  pgm.sql(`
    ALTER TABLE loans DROP CONSTRAINT IF EXISTS loans_customer_id_fkey;
    ALTER TABLE loans DROP CONSTRAINT IF EXISTS loans_property_id_fkey;
  `);
};
