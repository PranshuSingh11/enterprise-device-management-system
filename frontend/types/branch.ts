export interface Branch {
  id: number;
  name: string;
  location: string;
  status: string;
}

export interface BranchListResponse {
  items: Branch[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}