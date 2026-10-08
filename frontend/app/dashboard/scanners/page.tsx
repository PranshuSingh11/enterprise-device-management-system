import Link from "next/link";

import { serverApiFetch } from "@/lib/server-api";
import type { ScannerListResponse } from "@/types/scanner";
import ScannerStatusBadge from "@/components/ui/ScannerStatusBadge";

interface ScannersPageProps {
  searchParams: Promise<{
    page?: string;
    search?: string;
    status?: string;
  }>;
}

export default async function ScannersPage({
  searchParams,
}: ScannersPageProps) {
  const params = await searchParams;

  const page = Number(params.page) || 1;
  const search = params.search ?? "";
  const status = params.status ?? "";

  const queryParams = new URLSearchParams({
    page: String(page),
    page_size: "10",
  });

  if (search) {
    queryParams.set("search", search);
  }

  if (status) {
    queryParams.set("status", status);
  }

  const scanners = await serverApiFetch<ScannerListResponse>(
    `/api/v1/scanners?${queryParams.toString()}`
  );

  return (
    <div>
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            Scanners
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Manage and monitor registered scanners.
          </p>
        </div>

        <Link
          href="/dashboard/scanners/new"
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Add Scanner
        </Link>
      </div>

      <div className="mb-4 rounded-lg border bg-white p-4">
        <form className="flex flex-col gap-3 sm:flex-row">
          <input
            type="text"
            name="search"
            defaultValue={search}
            placeholder="Search scanners..."
            className="flex-1 rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
          />

          <select
            name="status"
            defaultValue={status}
            className="rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
          >
            <option value="">All statuses</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>

          <button
            type="submit"
            className="rounded-md border bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
          >
            Search
          </button>
        </form>
      </div>

      <div className="overflow-hidden rounded-lg border bg-white">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-gray-50">
              <tr>
                <th className="px-5 py-3 font-medium text-gray-600">
                  Name
                </th>

                <th className="px-5 py-3 font-medium text-gray-600">
                  Serial Number
                </th>

                <th className="px-5 py-3 font-medium text-gray-600">
                  Model
                </th>

                <th className="px-5 py-3 font-medium text-gray-600">
                  Status
                </th>

                <th className="px-5 py-3 font-medium text-gray-600">
                  Branch
                </th>
                 <th className="px-5 py-3 text-right font-medium text-gray-600">
  Actions
</th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {scanners.items.map((scanner) => (
                
               
                <tr
                  key={scanner.id}
                  className="hover:bg-gray-50"
                >
                  
                  <td className="px-5 py-4">
  <Link
    href={`/dashboard/scanners/${scanner.id}`}
    className="font-medium text-gray-900 hover:text-blue-600"
  >
    {scanner.name}
  </Link>
</td>

                  <td className="px-5 py-4 text-gray-600">
                    {scanner.serial_number}
                  </td>

                  <td className="px-5 py-4 text-gray-600">
                    {scanner.model}
                  </td>

                 <td className="px-5 py-4">
  <ScannerStatusBadge status={scanner.status} />
</td>

                  <td className="px-5 py-4 text-gray-600">
                    #{scanner.branch_id}
                  </td>
                  <td className="px-5 py-4 text-right">
  <Link
    href={`/dashboard/scanners/${scanner.id}`}
    className="text-sm font-medium text-blue-600 hover:text-blue-700"
  >
    View
  </Link>&nbsp;&nbsp;

    <Link
    href={`/dashboard/scanners/${scanner.id}/edit`}
    className="text-sm font-medium text-gray-600 hover:text-gray-900"
  >
    Edit
  </Link>
</td>
                </tr>
              ))}

              {scanners.items.length === 0 && (
                <tr>
                  <td
                    colSpan={5}
                    className="px-5 py-10 text-center text-sm text-gray-500"
                  >
                    No scanners found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between text-sm">
        <p className="text-gray-500">
          Showing {scanners.items.length} of {scanners.total} scanners
        </p>

        <div className="flex items-center gap-2">
          {page > 1 && (
            <Link
              href={`/dashboard/scanners?page=${page - 1}&search=${encodeURIComponent(search)}&status=${encodeURIComponent(status)}`}
              className="rounded-md border px-3 py-1.5 text-gray-600 hover:bg-gray-50"
            >
              Previous
            </Link>
          )}

          <span className="px-2 text-gray-600">
            Page {scanners.page} of {scanners.total_pages}
          </span>

          {page < scanners.total_pages && (
            <Link
              href={`/dashboard/scanners?page=${page + 1}&search=${encodeURIComponent(search)}&status=${encodeURIComponent(status)}`}
              className="rounded-md border px-3 py-1.5 text-gray-600 hover:bg-gray-50"
            >
              Next
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}