/**
 * Supabase Client for Client Components
 * 
 * This client is used in React Client Components (components that run in the browser).
 * It's safe to use in components marked with 'use client'.
 * 
 * See: https://supabase.com/docs/guides/auth/server-side/creating-a-client
 */

import { createBrowserClient } from "@supabase/ssr";

/**
 * Creates a Supabase client for use in Client Components.
 * 
 * This client automatically handles:
 * - Reading/writing cookies for session management
 * - Token refresh
 * - Browser-specific optimizations
 * 
 * @returns Supabase client instance
 */
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
