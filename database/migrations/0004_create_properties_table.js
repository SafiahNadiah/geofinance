exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("properties", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    code: { type: "varchar(12)", notNull: true, unique: true },
    owner_customer_id: {
      type: "uuid",
      notNull: true,
      references: "customers(id)"
    },
    type: { type: "varchar(40)" },
    address: { type: "text" },
    geom: { type: "geometry(Point,4326)", notNull: true },
    market_value_myr: { type: "numeric(14,2)" },
    floor_area_sqft: { type: "integer" },
    year_built: { type: "integer" },
    created_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    updated_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    deleted_at: { type: "timestamptz" }
  });

  pgm.addConstraint("properties", "properties_type_check", {
    check: "type IN ('terrace_house','condominium','apartment','semi_detached','bungalow','shop_lot')"
  });

  pgm.addConstraint("properties", "properties_market_value_myr_check", {
    check: "market_value_myr > 0"
  });

  pgm.addConstraint("properties", "properties_floor_area_sqft_check", {
    check: "floor_area_sqft > 0"
  });

  pgm.createIndex("properties", "geom", {
    method: "gist",
    name: "idx_properties_geom"
  });

  pgm.createIndex("properties", "owner_customer_id", {
    method: "btree",
    name: "idx_properties_owner_customer_id"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("properties");
};
