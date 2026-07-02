exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("users", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    email: { type: "varchar(120)", notNull: true, unique: true },
    password_hash: { type: "varchar", notNull: true },
    role_id: { type: "uuid", notNull: true, references: "roles(id)" },
    is_active: { type: "boolean", notNull: true, default: true },
    created_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") },
    updated_at: { type: "timestamptz", notNull: true, default: pgm.func("now()") }
  });

  pgm.createIndex("users", "role_id", {
    method: "btree",
    name: "idx_users_role_id"
  });
};

exports.down = (pgm) => {
  pgm.dropTable("users");
};
