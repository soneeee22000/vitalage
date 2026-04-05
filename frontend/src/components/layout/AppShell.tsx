import { Outlet, Navigate } from "react-router-dom";
import { useAuth } from "@/lib/use-auth";
import { BottomNav } from "@/components/ui/BottomNav";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorBoundary } from "@/components/error/ErrorBoundary";

export function AppShell() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <LoadingSpinner message="Chargement..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/connexion" replace />;
  }

  return (
    <div className="flex min-h-screen flex-col pb-16">
      <main className="flex-1">
        <ErrorBoundary>
          <Outlet />
        </ErrorBoundary>
      </main>
      <BottomNav />
    </div>
  );
}
