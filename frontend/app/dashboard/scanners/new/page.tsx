import Link from "next/link";
import ScannerForm from "@/components/scanners/ScannerForm";

export default function NewScannerPage() {
  return (
    <div>
      <div className="mb-6">
        <Link
          href="/dashboard/scanners"
          className="text-sm font-medium text-blue-600 hover:text-blue-700"
        >
          ← Back to Scanners
        </Link>

        <h1 className="mt-3 text-2xl font-semibold text-gray-900">
          Add Scanner
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Register a new scanner in the device management system.
        </p>
      </div>

      <div className="max-w-2xl rounded-lg border bg-white p-6">
        <ScannerForm />
      </div>
    </div>
  );
}