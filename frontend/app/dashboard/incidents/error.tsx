"use client";

import { useEffect } from "react";

export default function IncidentsError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Incidents page error:", error);
  }, [error]);

  return (
    <div className="rounded-lg border bg-white px-6 py-12 text-center">
      <h2 className="text-lg font-semibold text-gray-900">
        Unable to load incidents
      </h2>

      <p className="mt-2 text-sm text-gray-500">
        Something went wrong while loading incident data. Please try again.
      </p>

      <button
        type="button"
        onClick={reset}
        className="mt-5 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
      >
        Try again
      </button>
    </div>
  );
}