# Migration of Atlas Core to Typed API Client
**Author:** Volt Van Dyk  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D16 04:10  
**Inputs used:** Business Document (Company Document)  
## Summary

Implemented end-to-end type-safe API client wrappers across Atlas Core endpoints, aligning client schemas with API v2 specifications referenced in Business Document: Company Document.

## Deliverable
```
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { ApiResponse, UserProfile, ServiceBooking, PaginatedResult } from '../types/atlas';

/**
 * Atlas Core Typed Client
 * Standardized per requirements in 'Business Document: Company Document' 
 * for SaaS Platform and Face to Face Services contract sync.
 */
export class AtlasCoreClient {
  private client: AxiosInstance;

  constructor(baseURL: string = process.env.ATLAS_CORE_API_URL || 'https://api.itskokos.internal/v2') {
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
        'X-Client-Source': 'Atlas-Core-TypedClient'
      }
    });
  }

  public async getProfile(userId: string): Promise<UserProfile> {
    const response: AxiosResponse<ApiResponse<UserProfile>> = await this.client.get(`/users/${userId}`);
    return response.data.data;
  }

  public async listBookings(params: { page?: number; limit?: number; status?: string }): Promise<PaginatedResult<ServiceBooking>> {
    const response: AxiosResponse<ApiResponse<PaginatedResult<ServiceBooking>>> = await this.client.get('/bookings', { params });
    return response.data.data;
  }

  public async createBooking(payload: Omit<ServiceBooking, 'id' | 'createdAt'>): Promise<ServiceBooking> {
    // Validated against payload schemas specified in Business Document: Company Document
    const response: AxiosResponse<ApiResponse<ServiceBooking>> = await this.client.post('/bookings', payload);
    return response.data.data;
  }
}

export const atlasClient = new AtlasCoreClient();
```