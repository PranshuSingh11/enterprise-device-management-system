import Link from "next/link";
import { notFound } from "next/navigation";

import ScannerForm from "@/components/scanners/ScannerForm";
import { serverApiFetch } from "@/lib/server-api";
import type { Scanner } from "@/types/scanner";


interface EditScannerPageProps {
  params: Promise<{
    id: string;
  }>;
}



export default async function EditScannerPage({
  params,
}: EditScannerPageProps) {
  const { id } = await params;

  let scanner: Scanner;

  try {
    scanner = await serverApiFetch<Scanner>(
      `/api/v1/scanners/${id}`
    );
  } catch (error) {
    if (
      error instanceof Error &&
      "status" in error &&
      error.status === 404
    ) {
      notFound();
    }

    throw error;
  }

  return (
    <div>
      <div className="mb-6">
        <Link
          href={`/dashboard/scanners/${id}`}
          className="text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          ← Back to Scanner
        </Link>

        <h1 className="mt-3 text-2xl font-semibold text-gray-900">
          Edit Scanner
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Update scanner information and configuration.
        </p>
      </div>

      <div className="max-w-2xl rounded-lg border bg-white p-6">
        <ScannerForm scanner={scanner} />
      </div>
    </div>
  );
}