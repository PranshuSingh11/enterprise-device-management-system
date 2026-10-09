export default function PageLoading() {
  return (
    <div className="animate-pulse space-y-6">
      <div>
        <div className="h-7 w-40 rounded bg-gray-200" />
        <div className="mt-2 h-4 w-64 max-w-full rounded bg-gray-100" />
      </div>

      <div className="rounded-lg border bg-white p-4">
        <div className="h-10 w-full rounded bg-gray-100" />
      </div>

      <div className="overflow-hidden rounded-lg border bg-white p-5">
        <div className="mb-5 h-5 w-48 rounded bg-gray-200" />
        <div className="space-y-4">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="h-10 rounded bg-gray-100" />
          ))}
        </div>
      </div>
    </div>
  );
}