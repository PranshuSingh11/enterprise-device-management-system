"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface DeleteScannerButtonProps {
  scannerId: number;
}

export default function DeleteScannerButton({
  scannerId,
}: DeleteScannerButtonProps) {
  const router = useRouter();

  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");

 async function handleDelete() {
  const confirmed = window.confirm(
    "Are you sure you want to delete this scanner?"
  );

  if (!confirmed) {
    return;
  }

  setError("");
  setDeleting(true);

  try {
    console.log("DELETE STARTED");
    console.log("Scanner ID:", scannerId);
    console.log("URL:", `/api/scanners/${scannerId}`);

    const response = await fetch(`/api/scanners/${scannerId}`, {
      method: "DELETE",
    });

    console.log("DELETE RESPONSE:", response.status);

    if (!response.ok) {
      const data = await response.json();

      setError(
        data.detail ?? "Failed to delete scanner."
      );

      return;
    }

    router.push("/dashboard/scanners");
    router.refresh();
  } catch (error) {
    console.error("DELETE ERROR:", error);

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
        <p
          role="alert"
          className="mt-2 text-sm text-red-600"
        >
          {error}
        </p>
      )}
    </div>
  );
}