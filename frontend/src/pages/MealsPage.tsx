import { useState, useCallback, useRef } from "react";
import { Camera, UtensilsCrossed, Leaf, Sparkles, Clock } from "lucide-react";
import { useAuth } from "@/lib/use-auth";
import { useAsyncData } from "@/lib/use-async-data";
import { api, type MealAnalyzeRequest, type MealResponse } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { cn, fileToBase64, formatDate } from "@/lib/utils";

const MEAL_TYPE_LABELS: Record<string, string> = {
  breakfast: "Petit-dejeuner",
  lunch: "Dejeuner",
  dinner: "Diner",
  snack: "Collation",
};

export function MealsPage() {
  const { patientId } = useAuth();
  const safePatientId = patientId ?? "";
  const [refreshKey, setRefreshKey] = useState(0);

  const {
    data: meals,
    error,
    isLoading,
    retry,
  } = useAsyncData(
    () =>
      safePatientId
        ? api.meals.history(safePatientId)
        : Promise.reject(new Error("Patient ID manquant")),
    [safePatientId, refreshKey],
  );

  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<Record<
    string,
    unknown
  > | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [selectedMealType, setSelectedMealType] = useState("lunch");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleCapture = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const handleFileSelected = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file || !safePatientId) return;

      setAnalyzing(true);
      setAnalysisError(null);
      setAnalysisResult(null);

      try {
        const base64 = await fileToBase64(file);
        const data: MealAnalyzeRequest = {
          patient_id: safePatientId,
          image_base64: base64,
          meal_type: selectedMealType,
        };
        const result = await api.meals.analyze(data);
        setAnalysisResult(result as unknown as Record<string, unknown>);
        setRefreshKey((k) => k + 1);
      } catch (err) {
        setAnalysisError(
          err instanceof Error ? err.message : "Erreur lors de l'analyse",
        );
      } finally {
        setAnalyzing(false);
        if (fileInputRef.current) fileInputRef.current.value = "";
      }
    },
    [safePatientId, selectedMealType],
  );

  return (
    <div className="px-6 py-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-6">
        Mes Repas
      </h1>

      <Card className="p-5 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Camera size={20} className="text-nutrition" />
          <span className="font-medium">Photographier un repas</span>
        </div>

        <div className="flex gap-2 mb-4">
          {Object.entries(MEAL_TYPE_LABELS).map(([value, label]) => (
            <button
              key={value}
              type="button"
              onClick={() => setSelectedMealType(value)}
              className={cn(
                "flex-1 rounded-lg py-2 text-sm font-medium transition-colors min-h-[44px]",
                selectedMealType === value
                  ? "bg-nutrition/15 text-nutrition border-2 border-nutrition"
                  : "bg-muted/50 text-muted-foreground border-2 border-transparent",
              )}
            >
              {label}
            </button>
          ))}
        </div>

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleFileSelected}
          className="hidden"
          aria-label="Prendre une photo de repas"
        />

        <Button
          onClick={handleCapture}
          disabled={analyzing}
          className="w-full min-h-[56px] text-lg"
        >
          {analyzing ? (
            <span className="flex items-center gap-2">
              <div className="w-5 h-5 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
              Analyse en cours...
            </span>
          ) : (
            <span className="flex items-center gap-2">
              <Camera size={20} />
              Prendre une photo
            </span>
          )}
        </Button>
      </Card>

      {analysisError && <ErrorBanner message={analysisError} />}

      {analysisResult && <AnalysisResultCard result={analysisResult} />}

      {isLoading && <LoadingSpinner message="Chargement de l'historique..." />}
      {error && !isLoading && <ErrorBanner message={error} onRetry={retry} />}

      {!isLoading && Array.isArray(meals) && meals.length > 0 && (
        <div className="mt-6">
          <h2 className="font-medium text-muted-foreground mb-3 flex items-center gap-2">
            <Clock size={16} />
            Historique
          </h2>
          <div className="flex flex-col gap-3">
            {meals.map((meal) => (
              <MealHistoryCard key={meal.id} meal={meal} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function AnalysisResultCard({ result }: { result: Record<string, unknown> }) {
  const analysis = (result.analysis ?? result) as Record<string, unknown>;
  const foods = (analysis.foods_identified ?? []) as string[];
  const highlights = (analysis.nutritional_highlights ?? []) as string[];
  const tip = (analysis.micro_tip ?? "") as string;
  const summary = (analysis.summary ?? "") as string;
  const score = (result.nutrition_score ??
    analysis.quality_score ??
    50) as number;

  return (
    <Card className="p-5 mb-4 border-nutrition/30">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles size={18} className="text-nutrition" />
        <span className="font-medium">Analyse nutritionnelle</span>
        <span
          className={cn(
            "ml-auto font-bold text-lg",
            score >= 70
              ? "text-nutrition"
              : score >= 50
                ? "text-activity"
                : "text-destructive",
          )}
        >
          {score}/100
        </span>
      </div>

      {summary && <p className="text-sm mb-3">{summary}</p>}

      {foods.length > 0 && (
        <div className="mb-3">
          <p className="text-xs text-muted-foreground mb-1">
            Aliments identifies
          </p>
          <div className="flex flex-wrap gap-1.5">
            {foods.map((food, i) => (
              <span key={i} className="text-xs bg-muted px-2 py-1 rounded-full">
                {food}
              </span>
            ))}
          </div>
        </div>
      )}

      {highlights.length > 0 && (
        <div className="mb-3">
          {highlights.map((h, i) => (
            <div key={i} className="flex items-start gap-2 mb-1">
              <Leaf size={14} className="text-nutrition shrink-0 mt-0.5" />
              <span className="text-sm">{h}</span>
            </div>
          ))}
        </div>
      )}

      {tip && (
        <div className="bg-nutrition/10 rounded-lg p-3 mt-2">
          <p className="text-sm text-nutrition font-medium">{tip}</p>
        </div>
      )}
    </Card>
  );
}

function MealHistoryCard({ meal }: { meal: MealResponse }) {
  const analysis = meal.analysis;
  const summary = (analysis.summary ?? "Repas") as string;
  const score = meal.nutrition_score;
  const mealType = meal.meal_type;
  const mealDate = meal.date;

  return (
    <Card className="p-3 flex items-center gap-3">
      <div
        className={cn(
          "w-10 h-10 rounded-full flex items-center justify-center shrink-0",
          score >= 70 ? "bg-nutrition/15" : "bg-muted",
        )}
      >
        <UtensilsCrossed
          size={18}
          className={score >= 70 ? "text-nutrition" : "text-muted-foreground"}
        />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium truncate">{summary}</p>
        <p className="text-xs text-muted-foreground">
          {MEAL_TYPE_LABELS[mealType] ?? mealType} — {formatDate(mealDate)}
        </p>
      </div>
      <span
        className={cn(
          "text-sm font-bold",
          score >= 70 ? "text-nutrition" : "text-muted-foreground",
        )}
      >
        {score}
      </span>
    </Card>
  );
}
