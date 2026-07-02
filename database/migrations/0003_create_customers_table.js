exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("customers", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    code: { type: "varchar(12)", notNull: true, unique: true },
    full_name: { type: "varchar(120)", notNull: true },
    email: { type: "varchar(120)", notNull: true, unique: true },
    phone: { type: "varchar(20)" },
    occupation: { type: "varchar(60)" },
    monthly_income_myr: { type: "numeric(12,2)" },
    home_geom: { type: "geometry(Point,4326)" },
    nearest_branch_id: {
      type: "uuid",
      references: "branches(id)"
    },
    customer_since: { type: "date" },
    created_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    updated_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    deleted_at: { type: "timestamptz" }
  });

  pgm.addConstraint("customers", "customers_monthly_income_myr_check", {
    check: "monthly_income_myr >= 0"
  });

  pgm.createIndex("customers", "home_geom", {
    method: "gist",
    name: "idx_customers_geom"
  });

  pgm.createIndex("customers", "nearest_branch_id", {
    method: "btree",
    name: "idx_customers_nearest_branch_id"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("customers");
};
