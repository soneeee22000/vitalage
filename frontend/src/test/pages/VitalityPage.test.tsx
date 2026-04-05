import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { VitalityPage } from "@/pages/VitalityPage";
import { AuthContext, type AuthContextValue } from "@/lib/auth-context-value";

vi.mock("@/lib/api", async () => {
  const score = {
    patient_id: "00000000-0000-0000-0000-000000000001",
    nutrition: 72,
    sleep: 85,
    activity: 60,
    mood: 78,
    overall: 74,
    calculated_at: "2026-04-05T08:00:00Z",
    change_from_last_week: 3,
  };
  const trends = {
    patient_id: "00000000-0000-0000-0000-000000000001",
    period: "7d",
    data: [
      {
        date: "2026-03-30",
        overall: 68,
        nutrition: 65,
        sleep: 80,
        activity: 55,
        mood: 72,
      },
      {
        date: "2026-04-05",
        overall: 74,
        nutrition: 72,
        sleep: 85,
        activity: 60,
        mood: 78,
      },
      {
        date: "2026-04-04",
        overall: 73,
        nutrition: 71,
        sleep: 84,
        activity: 59,
        mood: 77,
      },
    ],
  };
  return {
    api: {
      vitality: {
        score: vi.fn().mockResolvedValue(score),
        trends: vi.fn().mockResolvedValue(trends),
      },
    },
    ApiRequestError: class extends Error {
      status: number;
      code: string;
      constructor(s: number, c: string, m: string) {
        super(m);
        this.status = s;
        this.code = c;
      }
    },
  };
});

const mockAuth: AuthContextValue = {
  isAuthenticated: true,
  isLoading: false,
  patientId: "00000000-0000-0000-0000-000000000001",
  displayName: "Marie",
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
};

function renderVitality() {
  return render(
    <MemoryRouter>
      <AuthContext value={mockAuth}>
        <VitalityPage />
      </AuthContext>
    </MemoryRouter>,
  );
}

describe("VitalityPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows the page heading", async () => {
    renderVitality();
    expect(await screen.findByText("Votre Vitalite")).toBeInTheDocument();
  });

  it("shows all 4 dimension labels", async () => {
    renderVitality();
    expect(await screen.findByText("Nutrition")).toBeInTheDocument();
    expect(screen.getByText("Sommeil")).toBeInTheDocument();
    expect(screen.getByText("Activite")).toBeInTheDocument();
    expect(screen.getByText("Humeur")).toBeInTheDocument();
  });

  it("shows individual dimension scores", async () => {
    renderVitality();
    expect(await screen.findByText("72")).toBeInTheDocument();
    expect(screen.getByText("85")).toBeInTheDocument();
    expect(screen.getByText("60")).toBeInTheDocument();
    expect(screen.getByText("78")).toBeInTheDocument();
  });

  it("shows the change indicator", async () => {
    renderVitality();
    expect(
      await screen.findByText(/\+3 depuis la semaine derniere/),
    ).toBeInTheDocument();
  });

  it("shows the trend sparkline", async () => {
    renderVitality();
    const sparkline = await screen.findByLabelText(
      "Graphique de tendance de vitalite sur 7 jours",
    );
    expect(sparkline).toBeInTheDocument();
  });
});
