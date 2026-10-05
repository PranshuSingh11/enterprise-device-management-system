import { apiFetch } from "@/lib/api";
import { serverApiFetch } from "@/lib/server-api";
import type { ScannerListResponse } from "@/types/scanner";

export default async function DashboardPage() {
  const scanners = await serverApiFetch<ScannerListResponse>(
    "/api/v1/scanners?page=1&page_size=1"
  );

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">
          Dashboard
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Overview of your device management environment.
        </p>
      </div>

      <div className="rounded-lg border bg-white p-5">
        <p className="text-sm text-gray-500">
          Total Scanners
        </p>

        <p className="mt-2 text-3xl font-semibold text-gray-900">
          {scanners.total}
        </p>
      </div>
    </div>
  );
}