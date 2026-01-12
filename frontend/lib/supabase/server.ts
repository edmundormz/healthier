/**
 * Supabase Client for Server Components and Server Actions
 * 
 * This client is used in:
 * - Server Components (default in App Router)
 * - Server Actions
 * - Route Handlers (API routes)
 * 
 * It reads cookies from the request to maintain user sessions.
 * 
 * See: https://supabase.com/docs/guides/auth/server-side/creating-a-client
 */

import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

/**
 * Creates a Supabase client for use in Server Components and Server Actions.
 * 
 * This client:
 * - Reads cookies from the Next.js request
 * - Maintains user session across server-side requests
 * - Automatically refreshes tokens when needed
 * 
 * @returns Supabase client instance
 */
export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // The `setAll` method was called from a Server Component.
            // This can be ignored if you have middleware refreshing
            // user sessions.
          }
        },
      },
    }
  );
}
