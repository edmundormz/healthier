/**
 * Supabase Client for Middleware
 * 
 * This client is used in Next.js middleware to:
 * - Refresh user sessions
 * - Protect routes
 * - Redirect unauthenticated users
 * 
 * Middleware runs on the edge, so we use a special client that works
 * with the request/response objects.
 * 
 * See: https://supabase.com/docs/guides/auth/server-side/nextjs
 */

import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

/**
 * Creates a Supabase client for use in Next.js middleware.
 * 
 * Middleware runs on the edge (before the request reaches your app),
 * so we need to handle cookies differently using request/response objects.
 * 
 * @param request - Next.js request object
 * @returns Object with Supabase client and response object
 */
export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({
            request,
          });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh session if expired - required for Server Components
  // https://supabase.com/docs/guides/auth/server-side/nextjs
  await supabase.auth.getUser();

  return supabaseResponse;
}
