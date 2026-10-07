import Link from "next/link";

export default function ScannerNotFound() {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center text-center">
      <h1 className="text-xl font-semibold text-gray-900">
        Scanner not found
      </h1>

      <p className="mt-2 max-w-md text-sm text-gray-500">
        The scanner you're looking for doesn't exist or may have
        been removed.
      </p>

      <Link
        href="/dashboard/scanners"
        className="mt-5 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
      >
        Back to Scanners
      </Link>
    </div>
  );
}