const defaultDatabaseUrl = "postgresql://postgres:postgres@localhost:5432/geofinance";

module.exports = {
  db: {
    connectionString: process.env.DATABASE_URL ?? defaultDatabaseUrl
  }
};
