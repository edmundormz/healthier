/**
 * Profile Page
 * 
 * Displays the current user's profile information.
 * Shows user details and account settings.
 */

import { requireAuth, getOptionalUser } from "@/lib/auth/utils";
import api from "@/lib/api/server";

interface User {
  id: string;
  email: string;
  full_name: string | null;
  created_at: string;
  updated_at: string;
}

export default async function ProfilePage() {
  const authUser = await requireAuth();

  // Fetch user details from backend
  let user: User | null = null;

  try {
    // The backend API expects user_id, but we can get it from the auth user
    // Note: The backend should have an endpoint like GET /api/users/me
    // For now, we'll try to get the user by their auth ID
    user = await api.get<User>(`/api/users/${authUser.id}`);
  } catch (error) {
    console.error("Failed to fetch user profile:", error);
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-black dark:text-zinc-50">
          Profile
        </h1>
        <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
          Manage your account settings and preferences
        </p>
      </div>

      <div className="rounded-lg border border-zinc-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <div className="space-y-4">
          <div>
            <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
              Email
            </h2>
            <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
              {authUser.email}
            </p>
          </div>

          {user?.full_name && (
            <div>
              <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                Full Name
              </h2>
              <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
                {user.full_name}
              </p>
            </div>
          )}

          <div>
            <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
              User ID
            </h2>
            <p className="mt-1 font-mono text-xs text-zinc-600 dark:text-zinc-400">
              {authUser.id}
            </p>
          </div>

          {user && (
            <div className="grid gap-4 sm:grid-cols-2">
              <div>
                <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                  Account Created
                </h2>
                <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
                  {new Date(user.created_at).toLocaleString()}
                </p>
              </div>
              <div>
                <h2 className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
                  Last Updated
                </h2>
                <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
                  {new Date(user.updated_at).toLocaleString()}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
