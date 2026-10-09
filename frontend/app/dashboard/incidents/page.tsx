import Link from "next/link";
import StatusBadge from "@/components/ui/StatusBadge";
import PriorityBadge from "@/components/ui/PriorityBadge";
import { serverApiFetch } from "@/lib/server-api";
import type { IncidentListResponse } from "@/types/incident";

interface IncidentsPageProps {
  searchParams: Promise<{
    page?: string;
    search?: string;
    status?: string;
    priority?: string;
  }>;
}

export default async function IncidentsPage({
  searchParams,
}: IncidentsPageProps) {
  const params = await searchParams;

  const page = Math.max(1, Number(params.page) || 1);
  const search = params.search ?? "";
  const status = params.status ?? "";
  const priority = params.priority ?? "";

  const queryParams = new URLSearchParams({
    page: String(page),
    page_size: "10",
    sort_by: "created_at",
    sort_order: "desc",
  });

  if (search) queryParams.set("search", search);
  if (status) queryParams.set("status", status);
  if (priority) queryParams.set("priority", priority);

  const incidents = await serverApiFetch<IncidentListResponse>(
    `/api/v1/incidents?${queryParams.toString()}`
  );

  function pageHref(nextPage: number) {
    const nextParams = new URLSearchParams();
    nextParams.set("page", String(nextPage));

    if (search) nextParams.set("search", search);
    if (status) nextParams.set("status", status);
    if (priority) nextParams.set("priority", priority);

    return `/dashboard/incidents?${nextParams.toString()}`;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">
          Incidents
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Track and manage scanner incidents across branches.
        </p>
      </div>

      <div className="mb-4 rounded-lg border bg-white p-4">
        <form className="flex flex-col gap-3 sm:flex-row">
          <input
            type="text"
            name="search"
            defaultValue={search}
            placeholder="Search incidents..."
            aria-label="Search incidents"
            className="min-w-0 flex-1 rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
          />

          <select
            name="status"
            defaultValue={status}
            aria-label="Filter by status"
            className="rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
          >
            <option value="">All statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>

          <select
            name="priority"
            defaultValue={priority}
            aria-label="Filter by priority"
            className="rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
          >
            <option value="">All priorities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <button
            type="submit"
            className="rounded-md border bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
          >
            Apply filters
          </button>
        </form>
      </div>

      <div className="overflow-hidden rounded-lg border bg-white">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-gray-50">
              <tr>
                <th className="px-5 py-3 font-medium text-gray-600">Incident</th>
                <th className="px-5 py-3 font-medium text-gray-600">Scanner</th>
                <th className="px-5 py-3 font-medium text-gray-600">Priority</th>
                <th className="px-5 py-3 font-medium text-gray-600">Status</th>
                <th className="px-5 py-3 font-medium text-gray-600">Created</th>
                <th className="px-5 py-3 font-medium text-gray-600">Actions</th>
              </tr>
            </thead>

            <tbody className="divide-y">
              {incidents.items.map((incident) => (
                <tr key={incident.id} className="hover:bg-gray-50">
                  <td className="max-w-sm px-5 py-4">
                    <p className="truncate font-medium text-gray-900">
                      {incident.title}
                    </p>
                    <p className="mt-1 truncate text-xs text-gray-500">
                      {incident.description}
                    </p>
                  </td>

                  <td className="px-5 py-4 text-gray-600">
                    #{incident.scanner_id}
                  </td>

                  <td className="px-5 py-4">
                    <PriorityBadge priority={incident.priority} />
                  </td>

                  <td className="px-5 py-4">
                    <StatusBadge status={incident.status} />
                  </td>

                  <td className="whitespace-nowrap px-5 py-4 text-gray-600">
                    {new Date(incident.created_at).toLocaleDateString("en-IN", {
                      day: "2-digit",
                      month: "short",
                      year: "numeric",
                      timeZone: "UTC",
                    })}
                  </td>

                  <td className="px-5 py-4">
                    <Link
                      href={`/dashboard/incidents/${incident.id}`}
                      className="font-medium text-blue-600 hover:text-blue-700"
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}

              {incidents.items.length === 0 && (
                <tr>
                  <td
                    colSpan={6}
                    className="px-5 py-10 text-center text-sm text-gray-500"
                  >
                    No incidents match your filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap items-center justify-between gap-3 text-sm">
        <p className="text-gray-500">
          Showing {incidents.items.length} of {incidents.total} incidents
        </p>

        <div className="flex items-center gap-2">
          {page > 1 && (
            <Link
              href={pageHref(page - 1)}
              className="rounded-md border px-3 py-1.5 text-gray-600 hover:bg-gray-50"
            >
              Previous
            </Link>
          )}

          <span className="px-2 text-gray-600">
            Page {incidents.page} of {incidents.total_pages}
          </span>

          {page < incidents.total_pages && (
            <Link
              href={pageHref(page + 1)}
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