import type { HealthResponseDto } from "../dtos/health.dto";

export class HealthService {
  public getHealth(): HealthResponseDto {
    return { status: "ok" };
  }
}
