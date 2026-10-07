export interface Incident {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  scanner_id: number;
  created_at: string;
  resolved_at: string | null;
}

export interface IncidentListResponse {
  items: Incident[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}