import express from "express";

import { healthRouter } from "./interfaces/routes/health.routes";
import { env } from "./shared/config/env";

const app = express();

app.use(express.json());
app.use(healthRouter);

app.listen(env.port, () => {
  // eslint-disable-next-line no-console
  console.log(`Backend listening on port ${env.port}`);
});
