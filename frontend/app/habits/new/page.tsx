"use client";

/**
 * New Habit Page
 * 
 * Form to create a new habit.
 * Supports both boolean (yes/no) and numeric (with target value) habits.
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api/client";

export default function NewHabitPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [type, setType] = useState<"boolean" | "numeric">("boolean");
  const [targetValue, setTargetValue] = useState("");
  const [unit, setUnit] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const habit = await api.post("/api/habits/", {
        name: name.trim(),
        type,
        target_value: type === "numeric" && targetValue ? parseFloat(targetValue) : null,
        unit: type === "numeric" && unit ? unit.trim() : null,
        active: true,
      });

      // Redirect to the new habit's detail page
      router.push(`/habits/${habit.id}`);
      router.refresh();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create habit. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <Link
          href="/habits"
          className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50"
        >
          ← Back to Habits
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-black dark:text-zinc-50">
          New Habit
        </h1>
        <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
          Create a new habit to track your daily progress
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
          {error && (
            <div className="mb-6 rounded-md bg-red-50 p-3 text-sm text-red-800 dark:bg-red-900/20 dark:text-red-200">
              {error}
            </div>
          )}

          <div className="space-y-6">
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-zinc-700 dark:text-zinc-300"
              >
                Name <span className="text-red-500">*</span>
              </label>
              <input
                id="name"
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="mt-1 block w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm placeholder-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50"
                placeholder="e.g., Drink Water, Exercise"
              />
            </div>

            <div>
              <label
                htmlFor="type"
                className="block text-sm font-medium text-zinc-700 dark:text-zinc-300"
              >
                Type <span className="text-red-500">*</span>
              </label>
              <select
                id="type"
                value={type}
                onChange={(e) => setType(e.target.value as "boolean" | "numeric")}
                className="mt-1 block w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50"
              >
                <option value="boolean">Yes/No (Did you do it?)</option>
                <option value="numeric">Numeric (Track a number)</option>
              </select>
              <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
                {type === "boolean"
                  ? "Track whether you completed the habit (yes/no)"
                  : "Track a numeric value (e.g., steps, minutes, cups of water)"}
              </p>
            </div>

            {type === "numeric" && (
              <>
                <div>
                  <label
                    htmlFor="targetValue"
                    className="block text-sm font-medium text-zinc-700 dark:text-zinc-300"
                  >
                    Target Value
                  </label>
                  <input
                    id="targetValue"
                    type="number"
                    step="0.1"
                    value={targetValue}
                    onChange={(e) => setTargetValue(e.target.value)}
                    className="mt-1 block w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm placeholder-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50"
                    placeholder="e.g., 10000"
                  />
                  <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
                    Optional: Set a daily target value
                  </p>
                </div>

                <div>
                  <label
                    htmlFor="unit"
                    className="block text-sm font-medium text-zinc-700 dark:text-zinc-300"
                  >
                    Unit
                  </label>
                  <input
                    id="unit"
                    type="text"
                    value={unit}
                    onChange={(e) => setUnit(e.target.value)}
                    className="mt-1 block w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm placeholder-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-50"
                    placeholder="e.g., steps, minutes, cups"
                  />
                  <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
                    Optional: Unit of measurement
                  </p>
                </div>
              </>
            )}
          </div>
        </div>

        <div className="flex items-center justify-end space-x-4">
          <Link
            href="/habits"
            className="rounded-md border border-zinc-300 bg-white px-4 py-2 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
          >
            Cancel
          </Link>
          <button
            type="submit"
            disabled={loading || !name.trim()}
            className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
          >
            {loading ? "Creating..." : "Create Habit"}
          </button>
        </div>
      </form>
    </div>
  );
}
