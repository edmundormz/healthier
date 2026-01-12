"use server";

/**
 * Server Actions for Authentication
 * 
 * These functions run on the server and can be called from Client Components.
 * They're used for logout and other auth operations that need server-side execution.
 * 
 * See: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions
 */

import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

/**
 * Sign out the current user.
 * 
 * Clears the Supabase session and redirects to the login page.
 */
export async function signOut() {
  const supabase = await createClient();
  await supabase.auth.signOut();
  redirect("/login");
}

/**
 * Get the current user session.
 * 
 * @returns User object if authenticated, null otherwise
 */
export async function getCurrentUser() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  return user;
}
