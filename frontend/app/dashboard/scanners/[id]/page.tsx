import Link from "next/link";
import { notFound } from "next/navigation";
import { serverApiFetch } from "@/lib/server-api";
import ScannerStatusBadge from "@/components/ui/ScannerStatusBadge";
import type { Scanner } from "@/types/scanner";

interface ScannerDetailPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function ScannerDetailPage({
  params,
}: ScannerDetailPageProps) {
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
          href="/dashboard/scanners"
          className="text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          ← Back to Scanners
        </Link>
      </div>

      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            {scanner.name}
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Scanner details and device information.
          </p>
        </div>

        <ScannerStatusBadge status={scanner.status} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-lg border bg-white">
          <div className="border-b px-5 py-4">
            <h2 className="text-base font-semibold text-gray-900">
              Device Information
            </h2>
          </div>

          <div className="divide-y">
            <div className="flex justify-between px-5 py-4">
              <span className="text-sm text-gray-500">
                Scanner ID
              </span>

              <span className="text-sm font-medium text-gray-900">
                #{scanner.id}
              </span>
            </div>

            <div className="flex justify-between px-5 py-4">
              <span className="text-sm text-gray-500">
                Serial Number
              </span>

              <span className="text-sm font-medium text-gray-900">
                {scanner.serial_number}
              </span>
            </div>

            <div className="flex justify-between px-5 py-4">
              <span className="text-sm text-gray-500">
                Model
              </span>

              <span className="text-sm font-medium text-gray-900">
                {scanner.model}
              </span>
            </div>

            <div className="flex justify-between px-5 py-4">
              <span className="text-sm text-gray-500">
                Branch
              </span>

              <span className="text-sm font-medium text-gray-900">
                #{scanner.branch_id}
              </span>
            </div>
          </div>
        </div>

        <div className="rounded-lg border bg-white">
          <div className="border-b px-5 py-4">
            <h2 className="text-base font-semibold text-gray-900">
              Current Status
            </h2>
          </div>

          <div className="p-5">
            <ScannerStatusBadge status={scanner.status} />

            <p className="mt-3 text-sm text-gray-500">
              Current operational status of this scanner.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}