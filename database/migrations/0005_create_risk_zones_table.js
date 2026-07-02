exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("risk_zones", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    code: { type: "varchar(10)", notNull: true, unique: true },
    name: { type: "varchar(120)", notNull: true },
    hazard_type: { type: "varchar(30)" },
    severity: { type: "varchar(10)" },
    geom: { type: "geometry(Polygon,4326)", notNull: true },
    created_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    updated_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") }
  });

  pgm.addConstraint("risk_zones", "risk_zones_hazard_type_check", {
    check: "hazard_type IN ('flood','landslide','other')"
  });

  pgm.addConstraint("risk_zones", "risk_zones_severity_check", {
    check: "severity IN ('low','medium','high')"
  });

  pgm.createIndex("risk_zones", "geom", {
    method: "gist",
    name: "idx_risk_zones_geom"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("risk_zones");
};
