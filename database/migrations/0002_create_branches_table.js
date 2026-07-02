exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("branches", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    code: { type: "varchar(10)", notNull: true, unique: true },
    name: { type: "varchar(120)", notNull: true },
    type: { type: "varchar(40)" },
    address: { type: "text" },
    geom: { type: "geometry(Point,4326)", notNull: true },
    opened_date: { type: "date" },
    staff_count: { type: "integer" },
    created_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    updated_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    deleted_at: { type: "timestamptz" }
  });

  pgm.addConstraint("branches", "branches_type_check", {
    check: "type IN ('main_branch','retail_branch','sme_centre','priority_banking')"
  });

  pgm.addConstraint("branches", "branches_staff_count_check", {
    check: "staff_count >= 0"
  });

  pgm.createIndex("branches", "geom", {
    method: "gist",
    name: "idx_branches_geom"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("branches");
};
