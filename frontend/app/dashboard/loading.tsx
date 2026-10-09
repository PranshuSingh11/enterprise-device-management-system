export default function DashboardLoading() {
  return (
    <div className="animate-pulse space-y-6">
      <div>
        <div className="h-7 w-48 rounded bg-gray-200" />
        <div className="mt-2 h-4 w-72 max-w-full rounded bg-gray-100" />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <div key={index} className="rounded-lg border bg-white p-5">
            <div className="h-4 w-28 rounded bg-gray-200" />
            <div className="mt-4 h-8 w-16 rounded bg-gray-200" />
            <div className="mt-3 h-3 w-32 rounded bg-gray-100" />
          </div>
        ))}
      </div>

      <div className="rounded-lg border bg-white p-5">
        <div className="h-5 w-40 rounded bg-gray-200" />
        <div className="mt-5 space-y-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <div key={index} className="h-12 rounded bg-gray-100" />
          ))}
        </div>
      </div>
    </div>
  );
}