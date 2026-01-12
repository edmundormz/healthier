/**
 * Habit Detail Page
 * 
 * Displays details for a specific habit.
 * Shows habit information and allows editing/deleting.
 */

import { requireAuth } from "@/lib/auth/utils";
import { notFound } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api/server";
import dynamic from "next/dynamic";

// Dynamically import client component to avoid SSR issues
const DeleteHabitButton = dynamic(
  () => import("@/components/habits/DeleteHabitButton"),
  { ssr: false }
);

interface Habit {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export default async function HabitDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  await requireAuth();
  const { id } = await params;

  let habit: Habit | null = null;

  try {
    habit = await api.get<Habit>(`/api/habits/${id}`);
  } catch (error) {
    // If habit not found, show 404
    notFound();
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Link
            href="/habits"
            className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50"
          >
            ← Back to Habits
          </Link>
          <h1 className="mt-2 text-3xl font-bold text-black dark:text-zinc-50">
            {habit.name}
          </h1>
        </div>
        <div className="flex space-x-2">
          <Link
            href={`/habits/${id}/edit`}
            className="rounded-md border border-zinc-300 bg-white px-4 py-2 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
          >
            Edit
          </Link>
          <DeleteHabitButton habitId={id} habitName={habit.name} />
        </div>
      </div>

      <div className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        {habit.description && (
          <div className="mb-4">
            <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
              Description
            </h2>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              {habit.description}
            </p>
          </div>
        )}

        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
              Created
            </h2>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              {new Date(habit.created_at).toLocaleString()}
            </p>
          </div>
          <div>
            <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
              Last Updated
            </h2>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              {new Date(habit.updated_at).toLocaleString()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
