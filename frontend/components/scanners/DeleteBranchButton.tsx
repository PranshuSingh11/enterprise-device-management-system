"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface DeleteBranchButtonProps {
  branchId: number;
}

export default function DeleteBranchButton({
  branchId,
}: DeleteBranchButtonProps) {
  const router = useRouter();

  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");

  async function handleDelete() {
    const confirmed = window.confirm(
      "Are you sure you want to delete this branch?"
    );

    if (!confirmed) return;

    setError("");
    setDeleting(true);

    try {
      const response = await fetch(`/api/branches/${branchId}`, {
        method: "DELETE",
      });

     if (!response.ok) {
  let message = "Failed to delete branch.";

  try {
    const data = await response.json();
    message = data.detail ?? message;
  } catch {
    // Response was not JSON.
  }

  setError(message);
  return;
}

      router.push("/dashboard/branches");
      router.refresh();
    } catch (error) {
      console.error("Failed to delete branch:", error);

      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong. Please try again."
      );
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div>
      <button
        type="button"
        onClick={handleDelete}
        disabled={deleting}
        className="rounded-md border border-red-200 px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {deleting ? "Deleting..." : "Delete"}
      </button>

      {error && (
        <p role="alert" className="mt-2 text-sm text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}