import Link from "next/link";
import { notFound } from "next/navigation";

import BranchStatusBadge from "@/components/ui/BranchStatusBadge";
import { serverApiFetch } from "@/lib/server-api";
import type { Branch } from "@/types/branch";
import DeleteBranchButton from "@/components/scanners/DeleteBranchButton";

interface BranchDetailPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function BranchDetailPage({
  params,
}: BranchDetailPageProps) {
  const { id } = await params;

  let branch: Branch;

  try {
    branch = await serverApiFetch<Branch>(
      `/api/v1/branches/${id}`
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
          href="/dashboard/branches"
          className="text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          ← Back to Branches
        </Link>
      </div>

      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            {branch.name}
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Branch details and operational information.
          </p>
        </div>
<div className="flex items-center gap-3">
    <Link
      href={`/dashboard/branches/${branch.id}/edit`}
      className="rounded-md border px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
    >
      Edit
    </Link>

    <DeleteBranchButton branchId={branch.id} />
</div>
  </div>

      <div className="max-w-2xl rounded-lg border bg-white">
        <div className="border-b px-5 py-4">
          <h2 className="text-base font-semibold text-gray-900">
            Branch Information
          </h2>
        </div>

        <div className="divide-y">
          <div className="flex justify-between px-5 py-4">
            <span className="text-sm text-gray-500">
              Branch ID
            </span>

            <span className="text-sm font-medium text-gray-900">
              #{branch.id}
            </span>
          </div>

          <div className="flex justify-between px-5 py-4">
            <span className="text-sm text-gray-500">
              Name
            </span>

            <span className="text-sm font-medium text-gray-900">
              {branch.name}
            </span>
          </div>

          <div className="flex justify-between px-5 py-4">
            <span className="text-sm text-gray-500">
              Location
            </span>

            <span className="text-sm font-medium text-gray-900">
              {branch.location}
            </span>
          </div>

          <div className="flex justify-between px-5 py-4">
            <span className="text-sm text-gray-500">
              Status
            </span>

            <BranchStatusBadge status={branch.status} />
          </div>
        </div>
      </div>
    </div>
  );
}