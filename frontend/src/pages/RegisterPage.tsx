import { useState, type FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@/lib/use-auth";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ErrorBanner } from "@/components/ui/ErrorBanner";

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    given_name: "",
    family_name: "",
    display_name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  function updateField(field: string, value: string) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await register(form);
      navigate("/");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Erreur lors de l'inscription",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-6">
      <Card className="w-full max-w-sm p-6">
        <h1 className="text-2xl font-bold font-[var(--font-heading)] text-center mb-2">
          Bienvenue sur VitalAge
        </h1>
        <p className="text-muted-foreground text-center mb-6">
          60 secondes par jour pour comprendre votre vitalite
        </p>
        {error && <ErrorBanner message={error} />}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 mt-4">
          <input
            type="text"
            placeholder="Prenom"
            value={form.given_name}
            onChange={(e) => updateField("given_name", e.target.value)}
            required
            className="rounded-lg border border-border bg-background px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
            aria-label="Prenom"
          />
          <input
            type="text"
            placeholder="Nom"
            value={form.family_name}
            onChange={(e) => updateField("family_name", e.target.value)}
            required
            className="rounded-lg border border-border bg-background px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
            aria-label="Nom de famille"
          />
          <input
            type="text"
            placeholder="Comment vous appeler ?"
            value={form.display_name}
            onChange={(e) => updateField("display_name", e.target.value)}
            required
            className="rounded-lg border border-border bg-background px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
            aria-label="Nom d'affichage"
          />
          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(e) => updateField("email", e.target.value)}
            required
            className="rounded-lg border border-border bg-background px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
            aria-label="Adresse email"
          />
          <input
            type="password"
            placeholder="Mot de passe (8 caracteres min.)"
            value={form.password}
            onChange={(e) => updateField("password", e.target.value)}
            required
            minLength={8}
            className="rounded-lg border border-border bg-background px-4 py-3 text-lg focus:outline-none focus:ring-2 focus:ring-primary"
            aria-label="Mot de passe"
          />
          <Button type="submit" disabled={isLoading}>
            {isLoading ? "Inscription..." : "Commencer"}
          </Button>
        </form>
        <p className="text-sm text-muted-foreground text-center mt-4">
          Deja un compte ?{" "}
          <Link to="/connexion" className="text-primary hover:underline">
            Se connecter
          </Link>
        </p>
      </Card>
    </div>
  );
}
