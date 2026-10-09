import { NextResponse } from "next/server";
import { serverApiFetch } from "@/lib/server-api";

interface IncidentRouteProps {
  params: Promise<{ id: string }>;
}

export async function PUT(
  request: Request,
  { params }: IncidentRouteProps
) {
  const { id } = await params;

  try {
    const body = await request.json();

    const incident = await serverApiFetch(
      `/api/v1/incidents/${id}`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }
    );

    return NextResponse.json(incident);
  } catch (error) {
    console.error("Failed to update incident:", error);

    if (
      error instanceof Error &&
      "status" in error &&
      typeof error.status === "number"
    ) {
      return NextResponse.json(
        { detail: error.message },
        { status: error.status }
      );
    }

    return NextResponse.json(
      { detail: "Failed to update incident" },
      { status: 500 }
    );
  }
}