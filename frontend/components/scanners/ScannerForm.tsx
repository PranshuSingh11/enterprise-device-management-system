"use client";

import { useRouter } from "next/navigation";

import { FormEvent, useEffect, useState } from "react";

import type { BranchListResponse } from "@/types/branch";

import type { Scanner } from "@/types/scanner";

import Link from "next/link";

interface ScannerFormProps {
  scanner?: Scanner;
}

export default function ScannerForm({scanner,}:ScannerFormProps) {
  const [name, setName] = useState(scanner?.name ?? "");
const [serialNumber, setSerialNumber] = useState(
  scanner?.serial_number ?? ""
);
const [model, setModel] = useState(scanner?.model ?? "");
const [status, setStatus] = useState(scanner?.status ?? "");
const [branchId, setBranchId] = useState(
  scanner ? String(scanner.branch_id) : ""
);

  const [branches, setBranches] = useState<BranchListResponse | null>(null);
  
  const [branchesLoading, setBranchesLoading] = useState(true);

  const [submitting, setSubmitting] = useState(false);

  const [error, setError] = useState("");

  const router = useRouter();

  useEffect(() => {
  async function loadBranches() {
    try {
      const response = await fetch("/api/branches");

      if (!response.ok) {
        throw new Error("Failed to load branches");
      }

      const data: BranchListResponse = await response.json();

      setBranches(data);
    } catch (error) {
      console.error(error);
    } finally {
      setBranchesLoading(false);
    }
  }

  loadBranches();
}, []);

async function handleSubmit(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();

  if (!name.trim()) {
  setError("Scanner name is required.");
  return;
}

if (!serialNumber.trim()) {
  setError("Serial number is required.");
  return;
}

if (!model.trim()) {
  setError("Scanner model is required.");
  return;
}

if (!status) {
  setError("Please select a scanner status.");
  return;
}

if (!branchId) {
  setError("Please select a branch.");
  return;
}

  setSubmitting(true);

  try {
    const response = await fetch(
  scanner ? `/api/scanners/${scanner.id}` : "/api/scanners",
  {
    method: scanner ? "PUT" : "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name,
      serial_number: serialNumber,
      model,
      status,
      branch_id: Number(branchId),
    }),
  }
);

    const data = await response.json();

    if (!response.ok) {
     setError(data.detail ?? "Failed to create scanner.");
      return;
    }

    console.log("Scanner created:", data);

    router.push("/dashboard/scanners");
    router.refresh();
  } catch (error) {
    console.error("Failed to create scanner:", error);
  } finally {
    setSubmitting(false);
  }
}

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label
          htmlFor="name"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Scanner Name
        </label>

        <input
          id="name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="Enter scanner name"
          className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label
          htmlFor="serialNumber"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Serial Number
        </label>

        <input
          id="serialNumber"
          value={serialNumber}
          onChange={(event) => setSerialNumber(event.target.value)}
          placeholder="Enter serial number"
          className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
        />
      </div>

      <div>
        <label
          htmlFor="model"
          className="mb-1 block text-sm font-medium text-gray-700"
        >
          Model
        </label>

        <input
          id="model"
          value={model}
          onChange={(event) => setModel(event.target.value)}
          placeholder="Enter scanner model"
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
          onChange={(event) => setStatus(event.target.value)}
          className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500"
        >
          <option value="">Select status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>

      <div>
  <label
    htmlFor="branchId"
    className="mb-1 block text-sm font-medium text-gray-700"
  >
    Branch
  </label>

  <select
    id="branchId"
    value={branchId}
    onChange={(event) => setBranchId(event.target.value)}
    disabled={branchesLoading}
    className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:border-blue-500 disabled:bg-gray-100"
  >
    <option value="">
      {branchesLoading ? "Loading branches..." : "Select branch"}
    </option>

    {branches?.items.map((branch) => (
      <option key={branch.id} value={branch.id}>
        {branch.name} — {branch.location}
      </option>
    ))}
  </select>
</div>

      <div className="flex justify-end gap-3 border-t pt-5">
        <Link
  href="/dashboard/scanners"
  className="rounded-md border px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
>
  Cancel
</Link>

        <button
  type="submit"
  disabled={submitting}
  className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
>
 {submitting
  ? scanner
    ? "Updating..."
    : "Creating..."
  : scanner
    ? "Update Scanner"
    : "Create Scanner"}
</button>
      </div>

      {error && (
  <div
    role="alert"
    className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
  >
    {error}
  </div>
)}
    </form>
  );
}