/**
 * Routines Layout
 * 
 * Wraps all routine pages with the navigation bar.
 * Requires authentication.
 */

import { requireAuth } from "@/lib/auth/utils";
import Navbar from "@/components/layout/Navbar";

export default async function RoutinesLayout({
  children,
}: {
  children: React.ReactNode;
}) {
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
