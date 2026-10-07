interface PriorityBadgeProps {
  priority: string;
}

const priorityStyles: Record<string, string> = {
  critical: "bg-red-50 text-red-700 ring-red-600/20",
  high: "bg-orange-50 text-orange-700 ring-orange-600/20",
  medium: "bg-blue-50 text-blue-700 ring-blue-600/20",
  low: "bg-gray-100 text-gray-600 ring-gray-500/20",
};

export default function PriorityBadge({
  priority,
}: PriorityBadgeProps) {
  const style =
    priorityStyles[priority] ??
    "bg-gray-100 text-gray-600 ring-gray-500/20";

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium capitalize ring-1 ring-inset ${style}`}
    >
      {priority}
    </span>
  );
}