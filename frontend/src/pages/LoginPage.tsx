import { useState, type FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/lib/use-auth";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { UserCircle2 } from "lucide-react";

const DEMO_EMAIL = "marie.dupont@demo.vitalage.health";
const DEMO_PASSWORD = "vitalage2026";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur de connexion");
    } finally {
      setIsLoading(false);
    }
  }

  function fillDemo() {
    setEmail(DEMO_EMAIL);
    setPassword(DEMO_PASSWORD);
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-6">
      <div className="w-full max-w-sm flex flex-col gap-4">
        <Card className="p-6">
          <h1 className="text-2xl font-bold font-[var(--font-heading)] text-center mb-2">
            VitalAge
          </h1>
          <p className="text-muted-foreground text-center mb-6">
            Votre compagnon de vitalite quotidien
          </p>
          {error && <ErrorBanner message={error} />}
          <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-4">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="rounded-lg border border-border bg-background px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
              aria-label="Adresse email"
            />
            <input
              type="password"
              placeholder="Mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="rounded-lg border border-border bg-background px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
              aria-label="Mot de passe"
            />
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Connexion..." : "Se connecter"}
            </Button>
          </form>
          <p className="text-sm text-muted-foreground text-center mt-4">
            Pas encore de compte ?{" "}
            <Link to="/inscription" className="text-primary hover:underline">
              S'inscrire
            </Link>
          </p>
        </Card>

        <Card className="p-4">
          <button
            type="button"
            onClick={fillDemo}
            className="w-full flex items-center gap-3 text-left group"
            aria-label="Utiliser le compte demo"
          >
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary">
              <UserCircle2 size={22} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground">
                Compte demo — Marie Dupont
              </p>
              <p className="text-xs text-muted-foreground truncate">
                {DEMO_EMAIL}
              </p>
            </div>
            <span className="text-xs text-primary font-medium opacity-0 group-hover:opacity-100 transition-opacity">
              Remplir
            </span>
          </button>
        </Card>
      </div>
    </div>
  );
}
