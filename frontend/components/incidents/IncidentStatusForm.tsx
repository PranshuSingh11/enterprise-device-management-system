"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface IncidentStatusFormProps {
  incidentId: number;
  currentStatus: string;
}

const statusOptions = [
  { value: "open", label: "Open" },
  { value: "in_progress", label: "In progress" },
  { value: "resolved", label: "Resolved" },
  { value: "closed", label: "Closed" },
];

export default function IncidentStatusForm({
  incidentId,
  currentStatus,
}: IncidentStatusFormProps) {
  const router = useRouter();

  const [status, setStatus] = useState(currentStatus);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    console.log("Incident status form submitted", { incidentId, status });
    event.preventDefault();
    
    setError("");
    setSuccess("");

    if (status === currentStatus) {
      setError("Choose a different status before saving.");
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch(`/api/incidents/${incidentId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });

      if (!response.ok) {
        let message = "Failed to update incident status.";

        try {
          const data = await response.json();
          message = data.detail ?? message;
        } catch {
          // Keep the fallback message if the response isn't JSON.
        }

        setError(message);
        return;
      }

      setSuccess("Incident status updated.");
      router.refresh();
    } catch (error) {
      console.error("Failed to update incident status:", error);
      setError("Unable to reach the server. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label
          htmlFor="incident-status"
          className="mb-2 block text-sm font-medium text-gray-700"
        >
          Status
        </label>

        <select
          id="incident-status"
          value={status}
          onChange={(event) => {
            setStatus(event.target.value);
            setError("");
            setSuccess("");
          }}
          disabled={submitting || currentStatus === "closed"}
          className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500 disabled:bg-gray-100"
        >
          {statusOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      {currentStatus === "closed" && (
        <p className="text-xs text-gray-500">
          Closed incidents cannot be reopened.
        </p>
      )}

      {error && (
        <p role="alert" className="text-sm text-red-600">
          {error}
        </p>
      )}

      {success && (
        <p role="status" className="text-sm text-green-700">
          {success}
        </p>
      )}

      <button
        type="submit"
        disabled={submitting || currentStatus === "closed"}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {submitting ? "Saving..." : "Save Status"}
      </button>
    </form>
  );
}