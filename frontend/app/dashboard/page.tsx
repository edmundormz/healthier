/**
 * Dashboard Page
 * 
 * Main dashboard showing overview of user's health data.
 * Displays routines, habits, and recent activity.
 */

import { requireAuth } from "@/lib/auth/utils";
import Link from "next/link";
import api from "@/lib/api/server";

// Type definitions for API responses
interface Routine {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
}

interface Habit {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
}

export default async function DashboardPage() {
  // Require authentication
  const user = await requireAuth();

  // Fetch user's routines and habits
  // Note: These will be empty arrays if the API returns 404 or if there are no items
  let routines: Routine[] = [];
  let habits: Habit[] = [];

  try {
    routines = await api.get<Routine[]>("/api/routines/");
  } catch (error) {
    // If API call fails, routines will remain empty
    console.error("Failed to fetch routines:", error);
  }

  try {
    habits = await api.get<Habit[]>("/api/habits/");
  } catch (error) {
    // If API call fails, habits will remain empty
    console.error("Failed to fetch habits:", error);
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-black dark:text-zinc-50">
          Dashboard
        </h1>
        <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
          Welcome back, {user.email}
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Routines Card */}
        <div className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-black dark:text-zinc-50">
              Routines
            </h2>
            <Link
              href="/routines"
              className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50"
            >
              View all →
            </Link>
          </div>
          <p className="mt-2 text-3xl font-bold text-black dark:text-zinc-50">
            {routines.length}
          </p>
          <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
            Active routines
          </p>
        </div>

        {/* Habits Card */}
        <div className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-black dark:text-zinc-50">
              Habits
            </h2>
            <Link
              href="/habits"
              className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50"
            >
              View all →
            </Link>
          </div>
          <p className="mt-2 text-3xl font-bold text-black dark:text-zinc-50">
            {habits.length}
          </p>
          <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
            Active habits
          </p>
        </div>
      </div>

      {/* Recent Routines */}
      {routines.length > 0 && (
        <div className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          <h2 className="text-xl font-semibold text-black dark:text-zinc-50">
            Recent Routines
          </h2>
          <ul className="mt-4 space-y-3">
            {routines.slice(0, 5).map((routine) => (
              <li
                key={routine.id}
                className="flex items-center justify-between border-b border-zinc-100 pb-3 last:border-0 dark:border-zinc-800"
              >
                <div>
                  <p className="font-medium text-black dark:text-zinc-50">
                    {routine.name}
                  </p>
                  {routine.description && (
                    <p className="text-sm text-zinc-600 dark:text-zinc-400">
                      {routine.description}
                    </p>
                  )}
                </div>
                <Link
                  href={`/routines/${routine.id}`}
                  className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50"
                >
                  View →
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Empty State */}
      {routines.length === 0 && habits.length === 0 && (
        <div className="rounded-lg border border-zinc-200 bg-white p-12 text-center dark:border-zinc-800 dark:bg-zinc-900">
          <p className="text-lg font-medium text-black dark:text-zinc-50">
            Get started with your health journey
          </p>
          <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
            Create your first routine or habit to begin tracking your progress.
          </p>
          <div className="mt-6 flex justify-center space-x-4">
            <Link
              href="/routines/new"
              className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
            >
              Create Routine
            </Link>
            <Link
              href="/habits/new"
              className="rounded-md border border-zinc-300 bg-white px-4 py-2 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
            >
              Create Habit
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
