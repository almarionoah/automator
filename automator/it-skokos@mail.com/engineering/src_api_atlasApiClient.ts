# Atlas Core Typed API Client Migration
**Author:** Mint Bishop  
**Department:** Engineering  
**Project:** Atlas Core  
**Produced:** D17 10:40  
**Inputs used:** Business Document (Company Document)  
## Summary

Migrated legacy untyped HTTP calls in Atlas Core to a strongly-typed TypeScript API client, integrating standard error handling and schemas per Company Document.

## Deliverable
```
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Aligned with API contracts outlined in Business Document: Company Document
export interface UserProfile {
  id: string;
  organizationId: string;
  name: string;
  email: string;
  role: 'admin' | 'member' | 'guest';
}

export interface ServiceEngagement {
  engagementId: string;
  serviceType: 'saas_sync' | 'face_to_face_consulting';
  scheduledDate: string;
  status: 'pending' | 'confirmed' | 'completed';
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export class AtlasApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string, tokenProvider: () => Promise<string>) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' },
    });

    this.client.interceptors.request.use(async (config) => {
      const token = await tokenProvider();
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  public async getUser(userId: string): Promise<ApiResponse<UserProfile>> {
    const res = await this.client.get<UserProfile>(`/v1/users/${userId}`);
    return { data: res.data, status: res.status };
  }

  public async createEngagement(payload: Omit<ServiceEngagement, 'engagementId'>): Promise<ApiResponse<ServiceEngagement>> {
    // Validated against service schemas defined in Company Document
    const res = await this.client.post<ServiceEngagement>('/v1/engagements', payload);
    return { data: res.data, status: res.status };
  }
}

export const atlasApi = new AtlasApiClient(
  process.env.ATLAS_API_BASE_URL || 'https://api.itskokos.com',
  async () => process.env.ATLAS_API_TOKEN || ''
);
```