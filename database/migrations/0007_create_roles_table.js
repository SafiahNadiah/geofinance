exports.shorthands = undefined;

exports.up = (pgm) => {
  pgm.createTable("roles", {
    id: {
      type: "uuid",
      primaryKey: true,
      notNull: true,
      default: pgm.func("gen_random_uuid()")
    },
    name: { type: "varchar", notNull: true, unique: true },
    permissions: { type: "jsonb", notNull: true }
  });
};

exports.down = (pgm) => {
  pgm.dropTable("roles");
};
