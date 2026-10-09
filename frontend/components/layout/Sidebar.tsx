"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigationItems = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Branches", href: "/dashboard/branches" },
  { label: "Scanners", href: "/dashboard/scanners" },
  { label: "Incidents", href: "/dashboard/incidents" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden min-h-screen w-64 shrink-0 flex-col border-r bg-white md:flex">
      <div className="border-b px-6 py-5">
        <div className="text-sm font-semibold text-gray-900">
          Enterprise Device
        </div>
        <div className="text-sm text-gray-500">Management</div>
      </div>

      <nav className="flex-1 px-3 py-5" aria-label="Main navigation">
        <p className="mb-2 px-3 text-xs font-medium uppercase tracking-wide text-gray-400">
          Workspace
        </p>

        <div className="space-y-1">
          {navigationItems.map((item) => {
            const isActive =
              item.href === "/dashboard"
                ? pathname === item.href
                : pathname.startsWith(item.href);

            return (
              <Link
                key={item.href}
                href={item.href}
                aria-current={isActive ? "page" : undefined}
                className={`block rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-blue-50 text-blue-700"
                    : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
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