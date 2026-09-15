export type ResourceCategory =
  | 'parking'
  | 'ev_charging'
  | 'pharmacy'
  | 'shop';

export type AvailabilityStatus =
  | 'available'
  | 'unavailable'
  | 'unknown';

export type FreshnessState =
  | 'fresh'
  | 'acceptable'
  | 'stale'
  | 'expired';

export interface LocationDto {
  latitude: number;
  longitude: number;
  accuracyMeters?: number;
}

export interface AvailabilityDto {
  status: AvailabilityStatus;
  available?: number;
  capacity?: number;
  observedAt?: string;
}

export interface FreshnessDto {
  state: FreshnessState;
  ageSeconds: number;
  score?: number;
}

export interface ResourceDto {
  id: string;
  category: ResourceCategory;
  name: string;
  location: LocationDto;
  address?: string;
  providerId: string;
  active: boolean;
  availability?: AvailabilityDto;
  freshness: FreshnessDto;
}
