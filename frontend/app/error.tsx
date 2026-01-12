"use client";

/**
 * Error Boundary Component
 * 
 * Catches errors in the app and displays a user-friendly error message.
 * This is a Next.js App Router feature.
 * 
 * See: https://nextjs.org/docs/app/api-reference/file-conventions/error
 */

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-4 dark:bg-black">
      <div className="w-full max-w-md space-y-6 text-center">
        <h1 className="text-4xl font-bold text-black dark:text-zinc-50">
          Something went wrong!
        </h1>
        <p className="text-lg text-zinc-600 dark:text-zinc-400">
          {error.message || "An unexpected error occurred"}
        </p>
        <div className="flex justify-center space-x-4">
          <button
            onClick={reset}
            className="rounded-md bg-black px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
          >
            Try again
          </button>
          <a
            href="/"
            className="rounded-md border border-zinc-300 bg-white px-6 py-3 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
          >
            Go home
          </a>
        </div>
      </div>
    </div>
  );
}
