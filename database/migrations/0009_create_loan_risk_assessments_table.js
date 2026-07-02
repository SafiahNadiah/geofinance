exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("loan_risk_assessments", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    loan_id: { type: "uuid", notNull: true, references: "loans(id)" },
    nearest_risk_zone_id: { type: "uuid", references: "risk_zones(id)" },
    distance_to_risk_zone_km: { type: "numeric(6,2)" },
    risk_score: { type: "numeric(5,1)" },
    risk_tier: { type: "varchar(10)" },
    score_breakdown: { type: "jsonb" },
    computed_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") }
  });

  pgm.addConstraint("loan_risk_assessments", "loan_risk_assessments_risk_score_check", {
    check: "risk_score BETWEEN 0 AND 100"
  });

  pgm.addConstraint("loan_risk_assessments", "loan_risk_assessments_risk_tier_check", {
    check: "risk_tier IN ('low','medium','high')"
  });

  pgm.createIndex("loan_risk_assessments", "loan_id", {
    method: "btree",
    name: "idx_loan_risk_assessments_loan_id"
  });

  pgm.createIndex("loan_risk_assessments", "nearest_risk_zone_id", {
    method: "btree",
    name: "idx_loan_risk_assessments_nearest_risk_zone_id"
  });

  pgm.createIndex("loan_risk_assessments", "risk_tier", {
    method: "btree",
    name: "idx_loan_risk_assessments_risk_tier"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("loan_risk_assessments");
};
