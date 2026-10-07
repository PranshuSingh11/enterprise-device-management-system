import { serverApiFetch } from "@/lib/server-api";
import StatCard from "@/components/ui/StatCard";
import type { DashboardSummary } from "@/types/dashboard";
import type { IncidentListResponse } from "@/types/incident";
import StatusBadge from "@/components/ui/StatusBadge";
import PriorityBadge from "@/components/ui/PriorityBadge";

export default async function DashboardPage() {
  const summary = await serverApiFetch<DashboardSummary>(
    "/dashboard/summary"
  );

  const incidents = await serverApiFetch<IncidentListResponse>(
  "/api/v1/incidents?page=1&page_size=5&sort_by=created_at&sort_order=desc"
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

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="Total Scanners"
          value={summary.total_scanners}
          description="Registered devices"
        />

        <StatCard
          label="Active Scanners"
          value={summary.active_scanners}
          description="Currently active"
        />

        <StatCard
          label="Open Incidents"
          value={summary.open_incidents}
          description="Require attention"
        />

        <StatCard
          label="Critical Incidents"
          value={summary.critical_incidents}
          description="High priority"
        />

        
      </div>
      

        <div className="mt-8 rounded-lg border bg-white">
  <div className="flex items-center justify-between border-b px-5 py-4">
    <div>
      <h2 className="text-base font-semibold text-gray-900">
        Recent Incidents
      </h2>

      <p className="mt-1 text-sm text-gray-500">
        Latest incidents reported across the environment.
      </p>
    </div>

    <a
      href="/dashboard/incidents"
      className="text-sm font-medium text-blue-600 hover:text-blue-700"
    >
      View all
    </a>
  </div>

  <div className="divide-y">
    {incidents.items.map((incident) => (
      <div
        key={incident.id}
        className="flex items-center justify-between px-5 py-4"
      >
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-gray-900">
            {incident.title}
          </p>

          <p className="mt-1 text-xs text-gray-500">
            Scanner #{incident.scanner_id}
          </p>
        </div>

        <div className="ml-4 flex shrink-0 items-center gap-3">
          <PriorityBadge priority={incident.priority} />

          <StatusBadge status={incident.status} />
        </div>
      </div>
    ))}

    {incidents.items.length === 0 && (
      <div className="px-5 py-8 text-center text-sm text-gray-500">
        No recent incidents.
      </div>
    )}
  </div>
</div>
    </div>
  );
}