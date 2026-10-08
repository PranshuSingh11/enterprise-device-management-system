import { notFound } from "next/navigation";
import BranchForm from "@/components/branches/BranchForm";
import { serverApiFetch } from "@/lib/server-api";
import type { Branch } from "@/types/branch";
import Link from "next/link";

interface BranchEditPageProps {
  params: Promise<{ id: string }>;
}

export default async function BranchEditPage({
  params,
}: BranchEditPageProps) {
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
          href={`/dashboard/branches/${id}`}
          className="text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          ← Back to Branch
        </Link>

        <h1 className="mt-3 text-2xl font-semibold text-gray-900">
          Edit Branch
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Update branch information and configuration.
        </p>
      </div>

      <div className="max-w-2xl rounded-lg border bg-white p-6">
        <BranchForm branch={branch} />
      </div>
    </div>
  );
}