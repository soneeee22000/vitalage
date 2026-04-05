import {
  Lightbulb,
  Lock,
  TrendingUp,
  TrendingDown,
  ArrowRight,
  Moon,
  Apple,
  Footprints,
  Heart,
  Zap,
} from "lucide-react";
import { useAuth } from "@/lib/use-auth";
import { useAsyncData } from "@/lib/use-async-data";
import { api, type InsightData } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { cn } from "@/lib/utils";

const DIMENSION_ICONS: Record<string, typeof Moon> = {
  sleep: Moon,
  nutrition: Apple,
  activity: Footprints,
  mood: Heart,
  energy: Zap,
};

const DIMENSION_COLORS: Record<string, string> = {
  sleep: "text-sleep",
  nutrition: "text-nutrition",
  activity: "text-activity",
  mood: "text-mood",
  energy: "text-activity",
};

export function InsightsPage() {
  const { patientId } = useAuth();
  const safePatientId = patientId ?? "";

  const {
    data: insights,
    error,
    isLoading,
    retry,
  } = useAsyncData(
    () =>
      safePatientId
        ? api.insights.list(safePatientId)
        : Promise.reject(new Error("Patient ID manquant")),
    [safePatientId],
  );

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <LoadingSpinner message="Chargement..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="px-6 py-8">
        <ErrorBanner message={error} onRetry={retry} />
      </div>
    );
  }

  const hasInsights = insights && insights.length > 0;

  if (!hasInsights) {
    return <LockedView />;
  }

  return (
    <div className="px-6 py-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-2">
        Vos Insights
      </h1>
      <p className="text-sm text-muted-foreground mb-6">
        Correlations personnelles detectees par l'IA
      </p>

      <div className="flex flex-col gap-4">
        {insights.map((insight) => (
          <InsightCard key={insight.id} insight={insight} />
        ))}
      </div>
    </div>
  );
}

function InsightCard({ insight }: { insight: InsightData }) {
  const data = insight.correlation_data;
  const dimA = (data.dimension_a ?? "sleep") as string;
  const dimB = (data.dimension_b ?? "energy") as string;
  const direction = (data.direction ?? "positive") as string;
  const strength = (data.strength ?? "moderate") as string;

  const IconA = DIMENSION_ICONS[dimA] ?? Lightbulb;
  const IconB = DIMENSION_ICONS[dimB] ?? Lightbulb;
  const colorA = DIMENSION_COLORS[dimA] ?? "text-primary";
  const colorB = DIMENSION_COLORS[dimB] ?? "text-primary";

  return (
    <Card className="p-5">
      <div className="flex items-center gap-2 mb-3">
        <div className="flex items-center gap-1">
          <IconA size={18} className={colorA} />
          <ArrowRight size={14} className="text-muted-foreground" />
          <IconB size={18} className={colorB} />
        </div>
        <div className="ml-auto flex items-center gap-1">
          {direction === "positive" ? (
            <TrendingUp size={16} className="text-primary" />
          ) : (
            <TrendingDown size={16} className="text-destructive" />
          )}
          <span
            className={cn(
              "text-xs px-2 py-0.5 rounded-full",
              strength === "strong"
                ? "bg-primary/15 text-primary"
                : "bg-muted text-muted-foreground",
            )}
          >
            {strength === "strong"
              ? "Fort"
              : strength === "moderate"
                ? "Modere"
                : "Faible"}
          </span>
        </div>
      </div>

      <p className="text-sm leading-relaxed">{insight.insight_text}</p>

      <p className="text-xs text-muted-foreground mt-2">
        {insight.insight_type === "correlation"
          ? "Correlation detectee"
          : insight.insight_type === "trend"
            ? "Tendance observee"
            : "Recommandation"}
      </p>
    </Card>
  );
}

function LockedView() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-6 text-center">
      <div className="relative mb-6">
        <div className="w-20 h-20 rounded-full bg-mood/10 flex items-center justify-center">
          <Lightbulb size={36} className="text-mood" />
        </div>
        <div className="absolute -bottom-1 -right-1 w-8 h-8 rounded-full bg-muted flex items-center justify-center">
          <Lock size={16} className="text-muted-foreground" />
        </div>
      </div>
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-2">
        Insights en preparation
      </h1>
      <p className="text-muted-foreground max-w-xs mb-4">
        Continuez vos bilans quotidiens pour debloquer vos insights personnels.
      </p>
      <p className="text-sm text-muted-foreground max-w-xs">
        L'IA detectera des correlations entre vos habitudes et votre bien-etre
        apres 7 jours de donnees.
      </p>
    </div>
  );
}
