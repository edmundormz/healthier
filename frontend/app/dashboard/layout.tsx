/**
 * Dashboard Layout
 * 
 * Wraps all dashboard pages with the navigation bar.
 * Requires authentication - redirects to login if not authenticated.
 */

import { requireAuth } from "@/lib/auth/utils";
import Navbar from "@/components/layout/Navbar";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Require authentication - redirects to /login if not authenticated
  await requireAuth();

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black">
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}
