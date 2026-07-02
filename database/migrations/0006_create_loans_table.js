exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("loans", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    code: { type: "varchar(12)", notNull: true, unique: true },
    customer_id: { type: "uuid", notNull: true, references: "customers(id)" },
    property_id: { type: "uuid", references: "properties(id)" },
    branch_id: { type: "uuid", notNull: true, references: "branches(id)" },
    loan_type: { type: "varchar(40)" },
    principal_amount_myr: { type: "numeric(14,2)" },
    interest_rate_pct: { type: "numeric(5,2)" },
    tenure_years: { type: "integer" },
    status: { type: "varchar(20)" },
    application_date: { type: "date", notNull: true },
    created_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    updated_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    deleted_at: { type: "timestamptz" }
  });

  pgm.addConstraint("loans", "loans_loan_type_check", {
    check: "loan_type IN ('home_loan','personal_loan','sme_business_loan','auto_loan','renovation_loan')"
  });

  pgm.addConstraint("loans", "loans_principal_amount_myr_check", {
    check: "principal_amount_myr > 0"
  });

  pgm.addConstraint("loans", "loans_interest_rate_pct_check", {
    check: "interest_rate_pct > 0"
  });

  pgm.addConstraint("loans", "loans_tenure_years_check", {
    check: "tenure_years > 0"
  });

  pgm.addConstraint("loans", "loans_status_check", {
    check: "status IN ('pending_approval','active','closed','defaulted','rejected')"
  });

  pgm.createIndex("loans", "customer_id", {
    method: "btree",
    name: "idx_loans_customer_id"
  });

  pgm.createIndex("loans", "property_id", {
    method: "btree",
    name: "idx_loans_property_id"
  });

  pgm.createIndex("loans", "branch_id", {
    method: "btree",
    name: "idx_loans_branch_id"
  });

  pgm.createIndex("loans", "status", {
    method: "btree",
    name: "idx_loans_status"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("loans");
};
