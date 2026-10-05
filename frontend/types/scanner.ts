export interface Scanner {
  id: number;
  name: string;
  serial_number: string;
  model: string;
  status: string;
  branch_id: number;
}

export interface ScannerListResponse {
  items: Scanner[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}