/**
 * API Client for Backend Communication
 * 
 * This client handles all communication with the FastAPI backend.
 * It automatically:
 * - Adds Supabase JWT tokens to requests
 * - Handles errors (401, 403, 500, etc.)
 * - Provides type-safe request/response handling
 * 
 * All API calls should go through this client, not directly to fetch().
 */

import { createClient } from "@/lib/supabase/client";

/**
 * Base URL for the FastAPI backend.
 * 
 * In development: http://localhost:8000
 * In production: Your Render URL (e.g., https://your-app.onrender.com)
 */
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * API Client class that handles authenticated requests to the backend.
 * 
 * Usage:
 * ```ts
 * const api = new ApiClient();
 * const routines = await api.get('/api/routines/');
 * ```
 */
export class ApiClient {
  /**
   * Gets the current Supabase session token.
   * 
   * The backend expects this token in the Authorization header:
   * Authorization: Bearer <token>
   * 
   * @returns JWT token or null if not authenticated
   */
  private async getAuthToken(): Promise<string | null> {
    const supabase = createClient();
    const {
      data: { session },
    } = await supabase.auth.getSession();

    return session?.access_token || null;
  }

  /**
   * Makes an authenticated GET request to the backend.
   * 
   * @param endpoint - API endpoint (e.g., '/api/routines/')
   * @param options - Optional fetch options
   * @returns Parsed JSON response
   * @throws Error if request fails
   */
  async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "GET",
    });
  }

  /**
   * Makes an authenticated POST request to the backend.
   * 
   * @param endpoint - API endpoint
   * @param body - Request body (will be JSON stringified)
   * @param options - Optional fetch options
   * @returns Parsed JSON response
   * @throws Error if request fails
   */
  async post<T>(
    endpoint: string,
    body?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  }

  /**
   * Makes an authenticated PUT request to the backend.
   * 
   * @param endpoint - API endpoint
   * @param body - Request body (will be JSON stringified)
   * @param options - Optional fetch options
   * @returns Parsed JSON response
   * @throws Error if request fails
   */
  async put<T>(
    endpoint: string,
    body?: unknown,
    options?: RequestInit
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  }

  /**
   * Makes an authenticated DELETE request to the backend.
   * 
   * @param endpoint - API endpoint
   * @param options - Optional fetch options
   * @returns Parsed JSON response (may be empty for 204 responses)
   * @throws Error if request fails
   */
  async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "DELETE",
    });
  }

  /**
   * Core request method that handles authentication and error handling.
   * 
   * @param endpoint - API endpoint
   * @param options - Fetch options
   * @returns Parsed JSON response
   * @throws Error with status code and message if request fails
   */
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    // Get authentication token
    const token = await this.getAuthToken();

    // Build full URL
    const url = `${API_BASE_URL}${endpoint}`;

    // Prepare headers with authentication
    const headers: HeadersInit = {
      ...options.headers,
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    // Make the request
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle errors
    if (!response.ok) {
      let errorMessage = `Request failed: ${response.status} ${response.statusText}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // If response isn't JSON, use default message
      }

      // Special handling for auth errors
      if (response.status === 401) {
        throw new Error("Unauthorized: Please log in again");
      }

      if (response.status === 403) {
        throw new Error("Forbidden: You don't have permission to access this resource");
      }

      throw new Error(errorMessage);
    }

    // Handle empty responses (e.g., 204 No Content)
    if (response.status === 204 || response.headers.get("content-length") === "0") {
      return {} as T;
    }

    // Parse and return JSON response
    return response.json();
  }
}

/**
 * Default API client instance.
 * 
 * Use this for all API calls:
 * ```ts
 * import api from '@/lib/api/client';
 * const routines = await api.get('/api/routines/');
 * ```
 */
export default new ApiClient();
