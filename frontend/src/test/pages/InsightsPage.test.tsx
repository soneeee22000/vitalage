import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { InsightsPage } from "@/pages/InsightsPage";
import { AuthContext, type AuthContextValue } from "@/lib/auth-context-value";

vi.mock("@/lib/api", async () => {
  const insights = [
    {
      id: "i1",
      insight_text:
        "Quand vous dormez plus de 4/5, votre energie le lendemain est 40% plus elevee",
      insight_type: "correlation",
      correlation_data: {
        dimension_a: "sleep",
        dimension_b: "energy",
        direction: "positive",
        strength: "strong",
      },
      generated_at: "2026-04-05T08:00:00Z",
    },
    {
      id: "i2",
      insight_text: "Les jours ou vous marchez, votre humeur est meilleure",
      insight_type: "correlation",
      correlation_data: {
        dimension_a: "activity",
        dimension_b: "mood",
        direction: "positive",
        strength: "moderate",
      },
      generated_at: "2026-04-05T08:00:00Z",
    },
  ];

  return {
    api: {
      insights: {
        list: vi.fn().mockResolvedValue(insights),
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
  patientId: "p1",
  displayName: "Marie",
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
};

function renderInsights() {
  return render(
    <MemoryRouter>
      <AuthContext value={mockAuth}>
        <InsightsPage />
      </AuthContext>
    </MemoryRouter>,
  );
}

describe("InsightsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows the page heading", async () => {
    renderInsights();
    expect(await screen.findByText("Vos Insights")).toBeInTheDocument();
  });

  it("shows insight text", async () => {
    renderInsights();
    expect(
      await screen.findByText(/votre energie le lendemain/),
    ).toBeInTheDocument();
  });

  it("shows correlation strength label", async () => {
    renderInsights();
    expect(await screen.findByText("Fort")).toBeInTheDocument();
    expect(screen.getByText("Modere")).toBeInTheDocument();
  });

  it("shows insight type label", async () => {
    renderInsights();
    const correlations = await screen.findAllByText("Correlation detectee");
    expect(correlations.length).toBe(2);
  });
});
