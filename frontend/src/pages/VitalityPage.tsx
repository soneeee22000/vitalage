import {
  Apple,
  Moon,
  Footprints,
  Heart,
  TrendingUp,
  TrendingDown,
  Minus,
} from "lucide-react";
import { useAuth } from "@/lib/use-auth";
import { useAsyncData } from "@/lib/use-async-data";
import { api, type VitalityScore, type VitalityTrend } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { cn } from "@/lib/utils";

const DIMENSIONS = [
  {
    key: "nutrition" as const,
    label: "Nutrition",
    color: "bg-nutrition",
    textColor: "text-nutrition",
    icon: Apple,
  },
  {
    key: "sleep" as const,
    label: "Sommeil",
    color: "bg-sleep",
    textColor: "text-sleep",
    icon: Moon,
  },
  {
    key: "activity" as const,
    label: "Activite",
    color: "bg-activity",
    textColor: "text-activity",
    icon: Footprints,
  },
  {
    key: "mood" as const,
    label: "Humeur",
    color: "bg-mood",
    textColor: "text-mood",
    icon: Heart,
  },
] as const;

function getScoreColor(score: number): string {
  if (score >= 75) return "text-primary";
  if (score >= 50) return "text-activity";
  return "text-destructive";
}

export function VitalityPage() {
  const { patientId } = useAuth();
  const safePatientId = patientId ?? "";

  const {
    data: score,
    error: scoreError,
    isLoading: scoreLoading,
    retry: retryScore,
  } = useAsyncData(
    () =>
      safePatientId
        ? api.vitality.score(safePatientId)
        : Promise.reject(new Error("Patient ID manquant")),
    [safePatientId],
  );

  const { data: trends, isLoading: trendsLoading } = useAsyncData(
    () =>
      safePatientId
        ? api.vitality.trends(safePatientId, "7d")
        : Promise.reject(new Error("Patient ID manquant")),
    [safePatientId],
  );

  if (scoreLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <LoadingSpinner message="Chargement du score..." />
      </div>
    );
  }

  if (scoreError) {
    const isNoScore = scoreError.includes("Pas encore");
    if (isNoScore) {
      return <NoScoreView />;
    }
    return (
      <div className="px-6 py-8">
        <ErrorBanner message={scoreError} onRetry={retryScore} />
      </div>
    );
  }

  if (!score) return null;

  return (
    <div className="px-6 py-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-6">
        Votre Vitalite
      </h1>

      <ScoreCircle score={score} />

      <div className="flex flex-col gap-3 mt-6">
        {DIMENSIONS.map(({ key, label, color, textColor, icon: Icon }) => (
          <DimensionBar
            key={key}
            label={label}
            value={score[key]}
            color={color}
            textColor={textColor}
            icon={<Icon size={18} />}
          />
        ))}
      </div>

      {!trendsLoading && trends && trends.data.length >= 3 && (
        <TrendSparkline data={trends} />
      )}
    </div>
  );
}

function ScoreCircle({ score }: { score: VitalityScore }) {
  const circumference = 2 * Math.PI * 54;
  const dashOffset = circumference - (score.overall / 100) * circumference;
  const change = score.change_from_last_week;

  return (
    <Card className="p-6 flex flex-col items-center">
      <div className="relative w-36 h-36">
        <svg viewBox="0 0 120 120" className="w-full h-full -rotate-90">
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="var(--color-muted)"
            strokeWidth="8"
          />
          <circle
            cx="60"
            cy="60"
            r="54"
            fill="none"
            stroke="var(--color-primary)"
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={dashOffset}
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className={cn("text-4xl font-bold", getScoreColor(score.overall))}
          >
            {score.overall}
          </span>
          <span className="text-xs text-muted-foreground">/100</span>
        </div>
      </div>

      {change !== null && change !== undefined && (
        <div
          className={cn(
            "flex items-center gap-1 mt-3 text-sm font-medium",
            change > 0
              ? "text-primary"
              : change < 0
                ? "text-destructive"
                : "text-muted-foreground",
          )}
        >
          {change > 0 ? (
            <TrendingUp size={16} />
          ) : change < 0 ? (
            <TrendingDown size={16} />
          ) : (
            <Minus size={16} />
          )}
          <span>
            {change > 0 ? "+" : ""}
            {change} depuis la semaine derniere
          </span>
        </div>
      )}
    </Card>
  );
}

function DimensionBar({
  label,
  value,
  color,
  textColor,
  icon,
}: {
  label: string;
  value: number;
  color: string;
  textColor: string;
  icon: React.ReactNode;
}) {
  return (
    <Card className="p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className={textColor}>{icon}</span>
          <span className="font-medium text-sm">{label}</span>
        </div>
        <span className={cn("font-bold", textColor)}>{value}</span>
      </div>
      <div className="h-2.5 rounded-full bg-muted overflow-hidden">
        <div
          className={cn(
            "h-full rounded-full transition-all duration-700 ease-out",
            color,
          )}
          style={{ width: `${value}%` }}
        />
      </div>
    </Card>
  );
}

function TrendSparkline({ data }: { data: VitalityTrend }) {
  const points = data.data;
  if (points.length < 2) return null;

  const maxScore = Math.max(...points.map((p) => p.overall));
  const minScore = Math.min(...points.map((p) => p.overall));
  const range = Math.max(maxScore - minScore, 10);

  const width = 280;
  const height = 60;
  const padding = 4;

  const pathPoints = points.map((p, i) => {
    const x = padding + (i / (points.length - 1)) * (width - padding * 2);
    const y =
      height -
      padding -
      ((p.overall - minScore) / range) * (height - padding * 2);
    return `${x},${y}`;
  });

  return (
    <Card className="p-4 mt-4">
      <div className="flex items-center justify-between mb-3">
        <span className="font-medium text-sm">Tendance 7 jours</span>
        <span className="text-xs text-muted-foreground">
          {points[0].date} — {points[points.length - 1].date}
        </span>
      </div>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        className="w-full"
        aria-label="Graphique de tendance de vitalite sur 7 jours"
      >
        <polyline
          points={pathPoints.join(" ")}
          fill="none"
          stroke="var(--color-primary)"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {points.map((p, i) => {
          const x = padding + (i / (points.length - 1)) * (width - padding * 2);
          const y =
            height -
            padding -
            ((p.overall - minScore) / range) * (height - padding * 2);
          return (
            <circle key={i} cx={x} cy={y} r="3" fill="var(--color-primary)" />
          );
        })}
      </svg>
      <div className="flex justify-between mt-1">
        <span className="text-xs text-muted-foreground">{minScore}</span>
        <span className="text-xs text-muted-foreground">{maxScore}</span>
      </div>
    </Card>
  );
}

function NoScoreView() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-6 text-center">
      <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mb-6">
        <Heart size={36} className="text-muted-foreground" />
      </div>
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-2">
        Score en preparation
      </h1>
      <p className="text-muted-foreground max-w-xs">
        Completez votre premier bilan du matin pour generer votre score de
        vitalite. Il s'ameliorera au fil des jours.
      </p>
    </div>
  );
}
