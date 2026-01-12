"use client";

/**
 * Edit Habit Page
 * 
 * Form to edit an existing habit.
 * Pre-fills the form with current habit data.
 */

import { useState, useEffect } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api/client";

interface Habit {
  id: string;
  name: string;
  type: "boolean" | "numeric";
  target_value: number | null;
  unit: string | null;
  active: boolean;
}

export default function EditHabitPage() {
  const router = useRouter();
  const params = useParams();
  const habitId = params.id as string;

  const [name, setName] = useState("");
  const [type, setType] = useState<"boolean" | "numeric">("boolean");
  const [targetValue, setTargetValue] = useState("");
  const [unit, setUnit] = useState("");
  const [active, setActive] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);

  // Fetch habit data on mount
  useEffect(() => {
    const fetchHabit = async () => {
      try {
        const habit = await api.get<Habit>(`/api/habits/${habitId}`);
        setName(habit.name);
        setType(habit.type);
        setTargetValue(habit.target_value?.toString() || "");
        setUnit(habit.unit || "");
        setActive(habit.active);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load habit. Please try again."
        );
      } finally {
        setFetching(false);
      }
    };

    fetchHabit();
  }, [habitId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await api.put(`/api/habits/${habitId}`, {
        name: name.trim(),
        target_value: type === "numeric" && targetValue ? parseFloat(targetValue) : null,
        unit: type === "numeric" && unit ? unit.trim() : null,
        active,
      });

      // Redirect to habit detail page
      router.push(`/habits/${habitId}`);
      router.refresh();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to update habit. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  if (fetching) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-black dark:text-zinc-50">
            Edit Habit
          </h1>
        </div>
        <div className="rounded-lg border border-zinc-200 bg-white p-12 text-center dark:border-zinc-800 dark:bg-zinc-900">
          <p className="text-zinc-600 dark:text-zinc-400">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <Link
          href={`/habits/${habitId}`}
          className="text-sm font-medium text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50"
        >
          ← Back to Habit
        </Link>
        <h1 className="mt-2 text-3xl font-bold text-black dark:text-zinc-50">
          Edit Habit
        </h1>
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
                </div>
              </>
            )}

            <div>
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={active}
                  onChange={(e) => setActive(e.target.checked)}
                  className="h-4 w-4 rounded border-zinc-300 text-black focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-800"
                />
                <span className="ml-2 text-sm text-zinc-700 dark:text-zinc-300">
                  Active (habit is currently being tracked)
                </span>
              </label>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-end space-x-4">
          <Link
            href={`/habits/${habitId}`}
            className="rounded-md border border-zinc-300 bg-white px-4 py-2 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
          >
            Cancel
          </Link>
          <button
            type="submit"
            disabled={loading || !name.trim()}
            className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
          >
            {loading ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </form>
    </div>
  );
}
