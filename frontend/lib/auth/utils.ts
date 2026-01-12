/**
 * Authentication Utilities
 * 
 * Helper functions for checking authentication status and protecting routes.
 */

import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

/**
 * Requires authentication for a route.
 * 
 * If the user is not authenticated, redirects to the login page.
 * Use this in Server Components or Server Actions.
 * 
 * @returns User object if authenticated
 * @throws Redirects to /login if not authenticated
 */
export async function requireAuth() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  return user;
}

/**
 * Gets the current user if authenticated, or null if not.
 * 
 * Does not redirect - use this when you want to handle unauthenticated
 * users gracefully (e.g., show different content).
 * 
 * @returns User object or null
 */
export async function getOptionalUser() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return user;
}
