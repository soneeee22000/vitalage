import { Link } from "react-router-dom";
import { useAuth } from "@/lib/use-auth";
import { Navigate } from "react-router-dom";
import {
  Heart,
  Moon,
  Footprints,
  Smile,
  Camera,
  TrendingUp,
  Target,
  Sparkles,
  Timer,
  ShieldCheck,
  ArrowRight,
  Leaf,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

const DIMENSIONS = [
  {
    icon: Leaf,
    label: "Nutrition",
    desc: "Photographiez vos repas, recevez une analyse nutritionnelle personnalisee",
    color: "text-nutrition bg-nutrition/10",
  },
  {
    icon: Moon,
    label: "Sommeil",
    desc: "Suivez la qualite de votre sommeil et decouvrez ce qui l'ameliore",
    color: "text-sleep bg-sleep/10",
  },
  {
    icon: Footprints,
    label: "Activite",
    desc: "Des micro-habitudes adaptees a votre rythme, pas des marathons",
    color: "text-activity bg-activity/10",
  },
  {
    icon: Smile,
    label: "Humeur",
    desc: "Comprenez les liens entre votre bien-etre et vos habitudes quotidiennes",
    color: "text-mood bg-mood/10",
  },
];

const FEATURES = [
  {
    icon: Timer,
    title: "60 secondes par jour",
    desc: "Un check-in matinal rapide qui devient un rituel agreable",
  },
  {
    icon: Camera,
    title: "Photo de repas",
    desc: "Photographiez, l'IA analyse. Pas de saisie fastidieuse de calories",
  },
  {
    icon: TrendingUp,
    title: "Score de vitalite",
    desc: "Un score composite qui evolue avec vous, pas un jugement",
  },
  {
    icon: Target,
    title: "Micro-habitudes",
    desc: "3 habitudes actives avec des streaks motivantes, style Duolingo",
  },
  {
    icon: Sparkles,
    title: "Insights IA",
    desc: "Des correlations personnelles : quand vous faites X, vous ressentez Y",
  },
  {
    icon: ShieldCheck,
    title: "Donnees FHIR",
    desc: "Vos donnees de sante au standard medical, securisees et portables",
  },
];

export function LandingPage() {
  const { isAuthenticated, isLoading } = useAuth();

  if (!isLoading && isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="min-h-screen">
      <header className="flex items-center justify-between px-6 py-4 max-w-5xl mx-auto">
        <span className="text-xl font-bold font-[var(--font-heading)] text-primary">
          VitalAge
        </span>
        <Link to="/connexion">
          <Button variant="ghost" className="text-sm">
            Se connecter
          </Button>
        </Link>
      </header>

      <section className="px-6 pt-12 pb-16 max-w-3xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-sm text-primary font-medium mb-6">
          <Heart size={14} />
          Smart Aging par Nestle Vital
        </div>
        <h1 className="text-4xl md:text-5xl font-bold font-[var(--font-heading)] leading-tight mb-4">
          Votre equation de vitalite,{" "}
          <span className="text-primary">jour apres jour</span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-xl mx-auto mb-8">
          60 secondes de check-in quotidien qui construisent une vision
          personnalisee de votre sante. Pas de regime, pas de contrainte — juste
          des micro-habitudes durables.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link to="/inscription">
            <Button className="gap-2 px-8">
              Commencer gratuitement
              <ArrowRight size={16} />
            </Button>
          </Link>
          <Link to="/connexion">
            <Button variant="secondary" className="px-8">
              Compte demo disponible
            </Button>
          </Link>
        </div>
      </section>

      <section className="px-6 py-12 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold font-[var(--font-heading)] text-center mb-2">
          4 dimensions de votre vitalite
        </h2>
        <p className="text-muted-foreground text-center mb-8">
          Un score composite construit sur ce qui compte vraiment
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {DIMENSIONS.map((d) => (
            <Card key={d.label} className="p-5 flex items-start gap-4">
              <div
                className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-xl ${d.color}`}
              >
                <d.icon size={22} />
              </div>
              <div>
                <h3 className="font-semibold mb-1">{d.label}</h3>
                <p className="text-sm text-muted-foreground">{d.desc}</p>
              </div>
            </Card>
          ))}
        </div>
      </section>

      <section className="px-6 py-12 bg-muted/50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-2xl font-bold font-[var(--font-heading)] text-center mb-2">
            Comment ca marche
          </h2>
          <p className="text-muted-foreground text-center mb-8">
            Simple, rapide, et concu pour durer
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {FEATURES.map((f) => (
              <Card key={f.title} className="p-5">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary mb-3">
                  <f.icon size={20} />
                </div>
                <h3 className="font-semibold mb-1">{f.title}</h3>
                <p className="text-sm text-muted-foreground">{f.desc}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <section className="px-6 py-12 max-w-3xl mx-auto">
        <Card className="p-8 text-center bg-primary/5 border-primary/20">
          <h2 className="text-2xl font-bold font-[var(--font-heading)] mb-2">
            Le parcours de Marie
          </h2>
          <p className="text-muted-foreground mb-6">
            En 30 jours, Marie a vu son score de vitalite passer de{" "}
            <span className="font-semibold text-activity">52</span> a{" "}
            <span className="font-semibold text-primary">76</span> — grace a 3
            micro-habitudes simples et 60 secondes par jour.
          </p>
          <div className="flex justify-center gap-8 mb-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-primary">76</p>
              <p className="text-xs text-muted-foreground">Score actuel</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-activity">12j</p>
              <p className="text-xs text-muted-foreground">Streak record</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-sleep">15</p>
              <p className="text-xs text-muted-foreground">Repas analyses</p>
            </div>
          </div>
          <Link to="/connexion">
            <Button className="gap-2">
              Explorer le profil demo
              <ArrowRight size={16} />
            </Button>
          </Link>
        </Card>
      </section>

      <section className="px-6 py-16 text-center max-w-3xl mx-auto">
        <h2 className="text-2xl font-bold font-[var(--font-heading)] mb-3">
          Pret a decouvrir votre vitalite ?
        </h2>
        <p className="text-muted-foreground mb-6">
          Rejoignez VitalAge et commencez votre parcours de sante preventive
          aujourd'hui.
        </p>
        <Link to="/inscription">
          <Button className="gap-2 px-8">
            Commencer maintenant
            <ArrowRight size={16} />
          </Button>
        </Link>
      </section>

      <footer className="border-t border-border px-6 py-6">
        <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <span className="font-[var(--font-heading)] font-semibold text-foreground">
            VitalAge
          </span>
          <span>
            Un produit{" "}
            <span className="font-medium text-foreground">Ekkhara</span> — AI
            Venture Studio
          </span>
          <span>VivaTech 2026 — Nestle Vital Challenge</span>
        </div>
      </footer>
    </div>
  );
}
