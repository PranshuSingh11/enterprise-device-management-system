interface BranchStatusBadgeProps {
  status: string;
}

const statusStyles: Record<string, string> = {
  Active: "bg-green-50 text-green-700 ring-green-600/20",
  inactive: "bg-gray-100 text-gray-600 ring-gray-500/20",
};

export default function BranchStatusBadge({
  status,
}: BranchStatusBadgeProps) {
  const style =
    statusStyles[status] ??
    "bg-gray-100 text-gray-600 ring-gray-500/20";

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium capitalize ring-1 ring-inset ${style}`}
    >
      {status}
    </span>
  );
}