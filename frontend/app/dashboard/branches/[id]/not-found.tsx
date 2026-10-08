import Link from "next/link";

export default function BranchNotFound() {
  return (
    <div className="flex min-h-100 flex-col items-center justify-center text-center">
      <h1 className="text-xl font-semibold text-gray-900">
        Branch not found
      </h1>

      <p className="mt-2 max-w-md text-sm text-gray-500">
        The branch you're looking for doesn't exist or may have
        been closed.
      </p>

      <Link
        href="/dashboard/branches"
        className="mt-5 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
      >
        Back to Branches
      </Link>
    </div>
  );
}