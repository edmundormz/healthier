"use client";

/**
 * Logout Button Component
 * 
 * A simple button that signs out the user when clicked.
 * Uses the signOut server action.
 */

import { signOut } from "@/lib/auth/actions";
import { useState } from "react";

export default function LogoutButton() {
  const [loading, setLoading] = useState(false);

  const handleLogout = async () => {
    setLoading(true);
    await signOut();
  };

  return (
    <button
      onClick={handleLogout}
      disabled={loading}
      className="rounded-md bg-zinc-200 px-4 py-2 text-sm font-medium text-zinc-900 transition-colors hover:bg-zinc-300 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-zinc-800 dark:text-zinc-50 dark:hover:bg-zinc-700"
    >
      {loading ? "Signing out..." : "Sign Out"}
    </button>
  );
}
