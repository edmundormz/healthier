/**
 * Navigation Bar Component
 * 
 * Displays the main navigation for authenticated users.
 * Shows user email and logout button.
 */

import { createClient } from "@/lib/supabase/server";
import LogoutButton from "@/components/auth/LogoutButton";
import Link from "next/link";

export default async function Navbar() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return null;
  }

  return (
    <nav className="border-b border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center space-x-8">
            <Link
              href="/dashboard"
              className="text-xl font-bold text-black dark:text-zinc-50"
            >
              CH Health OS
            </Link>
            <div className="hidden space-x-4 sm:flex">
              <Link
                href="/dashboard"
                className="rounded-md px-3 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800"
              >
                Dashboard
              </Link>
              <Link
                href="/routines"
                className="rounded-md px-3 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800"
              >
                Routines
              </Link>
              <Link
                href="/habits"
                className="rounded-md px-3 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800"
              >
                Habits
              </Link>
              <Link
                href="/profile"
                className="rounded-md px-3 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:bg-zinc-800"
              >
                Profile
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-zinc-600 dark:text-zinc-400">
              {user.email}
            </span>
            <LogoutButton />
          </div>
        </div>
      </div>
    </nav>
  );
}
