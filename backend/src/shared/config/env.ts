type AppConfig = {
  port: number;
  nodeEnv: string;
  databaseUrl: string;
  jwtSecret: string;
};

const parsePort = (value: string | undefined): number => {
  const parsed = Number.parseInt(value ?? "3001", 10);

  if (Number.isNaN(parsed) || parsed <= 0) {
    throw new Error("Invalid PORT environment variable.");
  }

  return parsed;
};

export const env: AppConfig = {
  port: parsePort(process.env.PORT),
  nodeEnv: process.env.NODE_ENV ?? "development",
  databaseUrl: process.env.DATABASE_URL ?? "",
  jwtSecret: process.env.JWT_SECRET ?? ""
};
