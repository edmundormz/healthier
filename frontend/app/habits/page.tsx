/**
 * Habits List Page
 * 
 * Displays all habits for the authenticated user.
 * Allows creating new habits and viewing existing ones.
 */

import { requireAuth } from "@/lib/auth/utils";
import Link from "next/link";
import api from "@/lib/api/server";

interface Habit {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export default async function HabitsPage() {
  await requireAuth();

  let habits: Habit[] = [];

  try {
    habits = await api.get<Habit[]>("/api/habits/");
  } catch (error) {
    console.error("Failed to fetch habits:", error);
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-black dark:text-zinc-50">
            Habits
          </h1>
          <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
            Track your daily habits and build consistency
          </p>
        </div>
        <Link
          href="/habits/new"
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
        >
          New Habit
        </Link>
      </div>

      {habits.length === 0 ? (
        <div className="rounded-lg border border-zinc-200 bg-white p-12 text-center dark:border-zinc-800 dark:bg-zinc-900">
          <p className="text-lg font-medium text-black dark:text-zinc-50">
            No habits yet
          </p>
          <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
            Create your first habit to start tracking.
          </p>
          <Link
            href="/habits/new"
            className="mt-6 inline-block rounded-md bg-black px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
          >
            Create Habit
          </Link>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {habits.map((habit) => (
            <Link
              key={habit.id}
              href={`/habits/${habit.id}`}
              className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md dark:border-zinc-800 dark:bg-zinc-900"
            >
              <h2 className="text-xl font-semibold text-black dark:text-zinc-50">
                {habit.name}
              </h2>
              {habit.description && (
                <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                  {habit.description}
                </p>
              )}
              <p className="mt-4 text-xs text-zinc-500 dark:text-zinc-400">
                Created {new Date(habit.created_at).toLocaleDateString()}
              </p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
