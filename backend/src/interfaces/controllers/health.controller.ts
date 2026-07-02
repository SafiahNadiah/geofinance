import type { Request, Response } from "express";

import { HealthService } from "../../application/services/health.service";

export class HealthController {
  private readonly healthService: HealthService;

  constructor(healthService: HealthService) {
    this.healthService = healthService;
  }

  public getHealth(_: Request, response: Response): void {
    const payload = this.healthService.getHealth();
    response.status(200).json(payload);
  }
}
