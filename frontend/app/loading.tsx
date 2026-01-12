/**
 * Global Loading Component
 * 
 * Shows a loading state while pages are loading.
 * This is a Next.js App Router feature.
 * 
 * See: https://nextjs.org/docs/app/api-reference/file-conventions/loading
 */

import LoadingSpinner from "@/components/common/LoadingSpinner";

export default function Loading() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black">
      <LoadingSpinner size="lg" />
    </div>
  );
}
