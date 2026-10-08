"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

interface BranchFormProps {
  branch?: {
    id: number;
    name: string;
    location: string;
    status: string;
  };
}

export default function BranchForm({
  branch,
}: BranchFormProps) {
  const [name, setName] = useState(branch?.name ?? "");
  const [location, setLocation] = useState(
    branch?.location ?? ""
  );
  const [status, setStatus] = useState(
    branch?.status ?? ""
  );

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const router = useRouter();

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");

    if (!name.trim()) {
      setError("Branch name is required.");
      return;
    }

    if (!location.trim()) {
      setError("Branch location is required.");
      return;
    }

    if (!status) {
      setError("Please select a branch status.");
      return;
    }

    setSubmitting(true);

    try {
      const response = await fetch(
        branch
          ? `/api/branches/${branch.id}`
          : "/api/branches",
        {
          method: branch ? "PUT" : "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name,
            location,
            status,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(
          data.detail ?? "Failed to save branch."
        );
        return;
      }

      router.push("/dashboard/branches");
      router.refresh();
    } catch (error) {
      console.error("Failed to save branch:", error);
      setError(
        "Something went wrong. Please try again."
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-5"
    >
      {error && (
        <div
          role="alert"
          className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
        >
          {error}
        </div>
      )}

      <div>
        <label
          htmlFor="name"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Branch Name
        </label>

        <input
          id="name"
          value={name}
          onChange={(event) =>
            setName(event.target.value)
          }
          placeholder="Enter branch name"
          className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label
          htmlFor="location"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Location
        </label>

        <input
          id="location"
          value={location}
          onChange={(event) =>
            setLocation(event.target.value)
          }
          placeholder="Enter branch location"
          className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label
          htmlFor="status"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Status
        </label>

        <select
          id="status"
          value={status}
          onChange={(event) =>
            setStatus(event.target.value)
          }
          className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
        >
          <option value="">
            Select status
          </option>

          <option value="active">
            Active
          </option>

          <option value="inactive">
            Inactive
          </option>
        </select>
      </div>

      <div className="flex justify-end gap-3 border-t pt-5">
        <a
          href="/dashboard/branches"
          className="rounded-md border px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Cancel
        </a>

        <button
          type="submit"
          disabled={submitting}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {submitting
            ? branch
              ? "Updating..."
              : "Creating..."
            : branch
              ? "Update Branch"
              : "Create Branch"}
        </button>
      </div>
    </form>
  );
}