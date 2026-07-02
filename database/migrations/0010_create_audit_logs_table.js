exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("audit_logs", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    actor_user_id: { type: "uuid", references: "users(id)" },
    action: { type: "varchar" },
    entity_type: { type: "varchar" },
    entity_id: { type: "uuid" },
    before_state: { type: "jsonb" },
    after_state: { type: "jsonb" },
    created_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") }
  });

  pgm.createIndex("audit_logs", "actor_user_id", {
    method: "btree",
    name: "idx_audit_logs_actor_user_id"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("audit_logs");
};
