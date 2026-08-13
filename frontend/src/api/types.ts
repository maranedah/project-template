// Mirrors the backend HTTP contract 1:1 (backend/app/infrastructure/api/routes.py).
// Rule: this file changes ONLY when the backend contract changes, in the same task.

export interface Item {
  id: number;
  name: string;
  source: string;
  created_at: string;
}
