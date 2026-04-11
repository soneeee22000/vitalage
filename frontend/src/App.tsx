import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/lib/auth-context";
import { ErrorBoundary } from "@/components/error/ErrorBoundary";
import { AppShell } from "@/components/layout/AppShell";
import { LandingPage } from "@/pages/LandingPage";
import { LoginPage } from "@/pages/LoginPage";
import { RegisterPage } from "@/pages/RegisterPage";
import { CheckInPage } from "@/pages/CheckInPage";
import { VitalityPage } from "@/pages/VitalityPage";
import { HabitsPage } from "@/pages/HabitsPage";
import { MealsPage } from "@/pages/MealsPage";
import { InsightsPage } from "@/pages/InsightsPage";

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route path="/bienvenue" element={<LandingPage />} />
            <Route path="/connexion" element={<LoginPage />} />
            <Route path="/inscription" element={<RegisterPage />} />
            <Route element={<AppShell />}>
              <Route index element={<CheckInPage />} />
              <Route path="repas" element={<MealsPage />} />
              <Route path="vitalite" element={<VitalityPage />} />
              <Route path="habitudes" element={<HabitsPage />} />
              <Route path="insights" element={<InsightsPage />} />
            </Route>
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
}
