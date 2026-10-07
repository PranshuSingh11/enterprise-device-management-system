interface StatusBadgeProps {
  status: string;
}

const statusStyles: Record<string, string> = {
  open: "bg-red-50 text-red-700 ring-red-600/20",
  in_progress: "bg-amber-50 text-amber-700 ring-amber-600/20",
  resolved: "bg-green-50 text-green-700 ring-green-600/20",
  closed: "bg-gray-100 text-gray-600 ring-gray-500/20",
};

export default function StatusBadge({ status }: StatusBadgeProps) {
  const style =
    statusStyles[status] ?? "bg-gray-100 text-gray-600 ring-gray-500/20";

  const label = status.replace("_", " ");

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium capitalize ring-1 ring-inset ${style}`}
    >
      {label}
    </span>
  );
}