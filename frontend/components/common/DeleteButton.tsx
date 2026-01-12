"use client";

/**
 * Delete Button Component
 * 
 * A button that shows a confirmation dialog before deleting.
 * Used for deleting routines, habits, etc.
 */

import { useState } from "react";
import { useRouter } from "next/navigation";

interface DeleteButtonProps {
  itemName: string;
  itemType: string;
  onDelete: () => Promise<void>;
  redirectTo?: string;
}

export default function DeleteButton({
  itemName,
  itemType,
  onDelete,
  redirectTo,
}: DeleteButtonProps) {
  const router = useRouter();
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async () => {
    setError(null);
    setLoading(true);

    try {
      await onDelete();
      if (redirectTo) {
        router.push(redirectTo);
        router.refresh();
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to delete. Please try again."
      );
      setShowConfirm(false);
    } finally {
      setLoading(false);
    }
  };

  if (showConfirm) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20">
        <p className="text-sm font-medium text-red-800 dark:text-red-200">
          Are you sure you want to delete "{itemName}"?
        </p>
        <p className="mt-1 text-xs text-red-600 dark:text-red-300">
          This action cannot be undone.
        </p>
        {error && (
          <p className="mt-2 text-xs text-red-600 dark:text-red-300">{error}</p>
        )}
        <div className="mt-4 flex space-x-2">
          <button
            onClick={handleDelete}
            disabled={loading}
            className="rounded-md bg-red-600 px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Deleting..." : "Yes, Delete"}
          </button>
          <button
            onClick={() => {
              setShowConfirm(false);
              setError(null);
            }}
            disabled={loading}
            className="rounded-md border border-red-300 bg-white px-3 py-1.5 text-xs font-medium text-red-700 transition-colors hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-red-700 dark:bg-zinc-800 dark:text-red-200 dark:hover:bg-zinc-700"
          >
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <button
      onClick={() => setShowConfirm(true)}
      className="rounded-md border border-red-300 bg-white px-4 py-2 text-sm font-medium text-red-700 transition-colors hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:border-red-700 dark:bg-zinc-800 dark:text-red-200 dark:hover:bg-zinc-700"
    >
      Delete {itemType}
    </button>
  );
}
