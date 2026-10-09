import Link from "next/link";
import { notFound } from "next/navigation";
import StatusBadge from "@/components/ui/StatusBadge";
import PriorityBadge from "@/components/ui/PriorityBadge";
import { serverApiFetch } from "@/lib/server-api";
import type { Incident } from "@/types/incident";
import IncidentStatusForm from "@/components/incidents/IncidentStatusForm";

interface IncidentDetailPageProps {
  params: Promise<{ id: string }>;
}

export default async function IncidentDetailPage({
  params,
}: IncidentDetailPageProps) {
  const { id } = await params;

  let incident: Incident;

  try {
    incident = await serverApiFetch<Incident>(
      `/api/v1/incidents/${id}`
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

  const createdAt = new Date(incident.created_at).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "UTC",
  });

  const resolvedAt = incident.resolved_at
    ? new Date(incident.resolved_at).toLocaleString("en-IN", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "UTC",
      })
    : null;

  return (
    <div>
      <div className="mb-6">
        <Link
          href="/dashboard/incidents"
          className="text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          ← Back to Incidents
        </Link>
      </div>

      <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm text-gray-500">
            Incident #{incident.id}
          </p>
          <h1 className="mt-1 text-2xl font-semibold text-gray-900">
            {incident.title}
          </h1>
          <p className="mt-2 text-sm text-gray-500">
            Reported on {createdAt}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <PriorityBadge priority={incident.priority} />
          <StatusBadge status={incident.status} />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <section className="rounded-lg border bg-white lg:col-span-2">
          <div className="border-b px-5 py-4">
            <h2 className="text-base font-semibold text-gray-900">
              Incident Information
            </h2>
          </div>

          <div className="space-y-5 p-5">
            <div>
              <h3 className="text-sm font-medium text-gray-700">
                Description
              </h3>
              <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-gray-600">
                {incident.description}
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <p className="text-sm text-gray-500">Scanner ID</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  #{incident.scanner_id}
                </p>
              </div>

              <div>
                <p className="text-sm text-gray-500">Resolved at</p>
                <p className="mt-1 text-sm font-medium text-gray-900">
                  {resolvedAt ?? "Not resolved"}
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-lg border bg-white">
          <div className="border-b px-5 py-4">
            <h2 className="text-base font-semibold text-gray-900">
              Update Status
            </h2>
          </div>

          <div className="p-5">
            <IncidentStatusForm
              incidentId={incident.id}
              currentStatus={incident.status}
            />
          </div>
        </section>
      </div>
    </div>
  );
}