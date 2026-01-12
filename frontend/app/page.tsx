import { getOptionalUser } from "@/lib/auth/utils";
import Link from "next/link";

/**
 * Home Page
 * 
 * Landing page that redirects authenticated users to dashboard,
 * or shows login/signup options for unauthenticated users.
 */
export default async function Home() {
  const user = await getOptionalUser();

  // If user is authenticated, redirect to dashboard
  if (user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-4 dark:bg-black">
        <div className="w-full max-w-md space-y-6 text-center">
          <h1 className="text-4xl font-bold text-black dark:text-zinc-50">
            CH Health OS
          </h1>
          <p className="text-lg text-zinc-600 dark:text-zinc-400">
            Welcome back! Redirecting to your dashboard...
          </p>
          <Link
            href="/dashboard"
            className="inline-block rounded-md bg-black px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
          >
            Go to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  // Show landing page for unauthenticated users
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 px-4 dark:bg-black">
      <div className="w-full max-w-md space-y-8 text-center">
        <div>
          <h1 className="text-4xl font-bold text-black dark:text-zinc-50">
            CH Health OS
          </h1>
          <p className="mt-4 text-lg text-zinc-600 dark:text-zinc-400">
            Family-centered health operating system with rules-first AI assistance
          </p>
        </div>

        <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
          <Link
            href="/signup"
            className="rounded-md bg-black px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-zinc-800 dark:bg-zinc-50 dark:text-black dark:hover:bg-zinc-200"
          >
            Get Started
          </Link>
          <Link
            href="/login"
            className="rounded-md border border-zinc-300 bg-white px-6 py-3 text-sm font-medium text-zinc-700 transition-colors hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
