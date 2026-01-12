/**
 * Next.js Middleware
 * 
 * This middleware runs on every request and:
 * 1. Refreshes Supabase user sessions
 * 2. Protects routes that require authentication
 * 3. Redirects unauthenticated users to login
 * 
 * See: https://nextjs.org/docs/app/building-your-application/routing/middleware
 */

import { updateSession } from "@/lib/supabase/middleware";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  // Update Supabase session (refreshes token if needed)
  return await updateSession(request);
}

/**
 * Configure which routes the middleware runs on.
 * 
 * Matcher patterns:
 * - `(auth)` - Routes in the (auth) group
 * - `dashboard` - Dashboard routes
 * - Excludes static files and API routes
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
