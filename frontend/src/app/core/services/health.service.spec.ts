import { HttpErrorResponse, provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { HealthService } from './health.service';

describe('HealthService', () => {
  let service: HealthService;
  let httpController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });

    service = TestBed.inject(HealthService);
    httpController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpController.verify();
  });

  it('returns the backend liveness status', () => {
    service.getLiveness().subscribe((response) => {
      expect(response).toEqual({ status: 'ok' });
    });

    const request = httpController.expectOne('/health/live');

    expect(request.request.method).toBe('GET');

    request.flush({ status: 'ok' });
  });

  it('propagates a network error', () => {
    let status: number | undefined;

    service.getLiveness().subscribe({
      error: (error: HttpErrorResponse) => {
        status = error.status;
      },
    });

    const request = httpController.expectOne('/health/live');

    request.error(new ProgressEvent('network error'));

    expect(status).toBe(0);
  });
});
