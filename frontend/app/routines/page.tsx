/**
 * Routines List Page
 * 
 * Displays all routines for the authenticated user.
 * Allows creating new routines and viewing existing ones.
 */

import { requireAuth } from "@/lib/auth/utils";
import Link from "next/link";
import api from "@/lib/api/server";

interface Routine {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export default async function RoutinesPage() {
  await requireAuth();

  let routines: Routine[] = [];

  try {
    routines = await api.get<Routine[]>("/api/routines/");
  } catch (error) {
    console.error("Failed to fetch routines:", error);
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-black dark:text-zinc-50">
            Routines
          </h1>
          <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
            Manage your daily routines and track your progress
          </p>
        </div>
        <Link
          href="/routines/new"
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
        >
          New Routine
        </Link>
      </div>

      {routines.length === 0 ? (
        <div className="rounded-lg border border-zinc-200 bg-white p-12 text-center dark:border-zinc-800 dark:bg-zinc-900">
          <p className="text-lg font-medium text-black dark:text-zinc-50">
            No routines yet
          </p>
          <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
            Create your first routine to get started.
          </p>
          <Link
            href="/routines/new"
            className="mt-6 inline-block rounded-md bg-black px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
          >
            Create Routine
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {routines.map((routine) => (
            <Link
              key={routine.id}
              href={`/routines/${routine.id}`}
              className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md dark:border-zinc-800 dark:bg-zinc-900"
            >
              <h2 className="text-xl font-semibold text-black dark:text-zinc-50">
                {routine.name}
              </h2>
              {routine.description && (
                <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                  {routine.description}
                </p>
              )}
              <p className="mt-4 text-xs text-zinc-500 dark:text-zinc-400">
                Created {new Date(routine.created_at).toLocaleDateString()}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
