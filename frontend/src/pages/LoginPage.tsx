import { useState, type FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/lib/use-auth";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ErrorBanner } from "@/components/ui/ErrorBanner";

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

  return (
    <div className="flex min-h-screen items-center justify-center px-6">
      <Card className="w-full max-w-sm p-6">
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
    </div>
  );
}
