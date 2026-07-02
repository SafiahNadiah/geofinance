import { Router } from "express";

import { HealthService } from "../../application/services/health.service";
import { HealthController } from "../controllers/health.controller";

const healthRouter = Router();
const healthService = new HealthService();
const healthController = new HealthController(healthService);

healthRouter.get("/health", (request, response) => {
  healthController.getHealth(request, response);
});

export { healthRouter };
