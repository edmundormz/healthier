/**
 * Server-Side API Client
 * 
 * This client is used in Server Components and Server Actions.
 * It uses the server-side Supabase client to get the user's session.
 * 
 * Use this instead of the regular API client when making requests from Server Components.
 */

import { createClient } from "@/lib/supabase/server";

/**
 * Base URL for the FastAPI backend.
 */
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Server-side API Client class.
 * 
 * Usage in Server Components:
 * ```ts
 * import api from '@/lib/api/server';
 * const routines = await api.get('/api/routines/');
 * ```
 */
export class ServerApiClient {
  /**
   * Gets the current Supabase session token from the server.
   */
  private async getAuthToken(): Promise<string | null> {
    const supabase = await createClient();
    const {
      data: { session },
    } = await supabase.auth.getSession();

    return session?.access_token || null;
  }

  /**
   * Makes an authenticated GET request to the backend.
   */
  async get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "GET",
    });
  }

  /**
   * Makes an authenticated POST request to the backend.
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
   */
  async delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: "DELETE",
    });
  }

  /**
   * Core request method that handles authentication and error handling.
   */
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = await this.getAuthToken();

    const url = `${API_BASE_URL}${endpoint}`;

    const headers: HeadersInit = {
      ...options.headers,
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorMessage = `Request failed: ${response.status} ${response.statusText}`;

      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
        // If response isn't JSON, use default message
      }

      if (response.status === 401) {
        throw new Error("Unauthorized: Please log in again");
      }

      if (response.status === 403) {
        throw new Error("Forbidden: You don't have permission to access this resource");
      }

      throw new Error(errorMessage);
    }

    if (response.status === 204 || response.headers.get("content-length") === "0") {
      return {} as T;
    }

    return response.json();
  }
}

/**
 * Default server-side API client instance.
 */
export default new ServerApiClient();
