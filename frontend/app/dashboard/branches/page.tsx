import Link from "next/link";

import BranchStatusBadge from "@/components/ui/BranchStatusBadge"
import { serverApiFetch } from "@/lib/server-api";
import type { BranchListResponse } from "@/types/branch";

interface BranchesPageProps {
  searchParams: Promise<{
    page?: string;
    search?: string;
    status?: string;
  }>;
}

export default async function BranchesPage({
  searchParams,
}: BranchesPageProps) {
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

  const branches = await serverApiFetch<BranchListResponse>(
    `/api/v1/branches?${queryParams.toString()}`
  );

  return (
    <div>
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            Branches
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Manage business branches and their operational status.
          </p>
        </div>

        <Link
          href="/dashboard/branches/new"
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Add Branch
        </Link>
      </div>

      <div className="mb-4 rounded-lg border bg-white p-4">
        <form className="flex flex-col gap-3 sm:flex-row">
          <input
            type="text"
            name="search"
            defaultValue={search}
            placeholder="Search branches..."
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
                  Location
                </th>

                <th className="px-5 py-3 font-medium text-gray-600">
                  Status
                </th>

                <th className="px-5 py-3 font-medium text-gray-600">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {branches.items.map((branch) => (
                <tr
                  key={branch.id}
                  className="hover:bg-gray-50"
                >
                  <td className="px-5 py-4 font-medium text-gray-900">
                    {branch.name}
                  </td>

                  <td className="px-5 py-4 text-gray-600">
                    {branch.location}
                  </td>

                  <td className="px-5 py-4">
                    <BranchStatusBadge
                      status={branch.status}
                    />
                  </td>

                  <td className="px-5 py-4">
                    <Link
                      href={`/dashboard/branches/${branch.id}`}
                      className="text-sm font-medium text-blue-600 hover:text-blue-700"
                    >
                      View
                    </Link>&nbsp;&nbsp;

    <Link
    href={`/dashboard/branches/${branch.id}/edit`}
    className="text-sm font-medium text-gray-600 hover:text-gray-900"
  >
    Edit
  </Link>
                  </td>
                </tr>
              ))}

              {branches.items.length === 0 && (
                <tr>
                  <td
                    colSpan={4}
                    className="px-5 py-10 text-center text-sm text-gray-500"
                  >
                    No branches found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between text-sm">
        <p className="text-gray-500">
          Showing {branches.items.length} of {branches.total} branches
        </p>

        <div className="flex items-center gap-2">
          {page > 1 && (
            <Link
              href={`/dashboard/branches?page=${page - 1}&search=${encodeURIComponent(search)}&status=${encodeURIComponent(status)}`}
              className="rounded-md border px-3 py-1.5 text-gray-600 hover:bg-gray-50"
            >
              Previous
            </Link>
          )}

          <span className="px-2 text-gray-600">
            Page {branches.page} of {branches.total_pages}
          </span>

          {page < branches.total_pages && (
            <Link
              href={`/dashboard/branches?page=${page + 1}&search=${encodeURIComponent(search)}&status=${encodeURIComponent(status)}`}
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