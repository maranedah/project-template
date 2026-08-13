// Template: page chrome only — no data fetching, no business logic.

import type { ReactNode } from "react";

export function MainLayout({ children }: { children: ReactNode }) {
  return (
    <div className="layout">
      <header>
        <h1>PROJECT_NAME</h1>
      </header>
      <main>{children}</main>
    </div>
  );
}
