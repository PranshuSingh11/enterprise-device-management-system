import Link from "next/link";

const navigationItems = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Branches", href: "/dashboard/branches" },
  { label: "Scanners", href: "/dashboard/scanners" },
  { label: "Incidents", href: "/dashboard/incidents" },
];

export default function Sidebar() {
  return (
    <aside className="flex min-h-screen w-64 flex-col border-r bg-white">
      <div className="border-b px-6 py-5">
        <div className="text-sm font-semibold text-gray-900">
          Enterprise Device
        </div>
        <div className="text-sm text-gray-500">
          Management
        </div>
      </div>

      <nav className="flex-1 px-3 py-5">
        <p className="mb-2 px-3 text-xs font-medium uppercase tracking-wide text-gray-400">
          Workspace
        </p>

        <div className="space-y-1">
          {navigationItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="block rounded-md px-3 py-2 text-sm font-medium text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-900"
            >
              {item.label}
            </Link>
          ))}
        </div>
      </nav>

      <div className="border-t px-6 py-4">
        <p className="text-xs text-gray-400">
          Enterprise Device Management
        </p>
      </div>
    </aside>
  );
}