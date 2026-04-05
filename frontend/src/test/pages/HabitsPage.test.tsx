import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { HabitsPage } from "@/pages/HabitsPage";
import { AuthContext, type AuthContextValue } from "@/lib/auth-context-value";

vi.mock("@/lib/api", async () => {
  const habits = [
    {
      id: "h1",
      patient_id: "p1",
      template_id: "walk-after-lunch",
      name: "Marcher 10 min apres le dejeuner",
      dimension: "activity",
      started_at: "2026-03-25T08:00:00Z",
      is_active: true,
      current_streak: 12,
      completed_today: false,
    },
    {
      id: "h2",
      patient_id: "p1",
      template_id: "fruit-before-noon",
      name: "1 fruit avant midi",
      dimension: "nutrition",
      started_at: "2026-03-28T08:00:00Z",
      is_active: true,
      current_streak: 5,
      completed_today: true,
    },
  ];

  return {
    api: {
      habits: {
        list: vi.fn().mockResolvedValue(habits),
        complete: vi.fn().mockResolvedValue({ status: "completed" }),
        templates: vi.fn().mockResolvedValue([]),
        activate: vi.fn().mockResolvedValue({}),
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

function renderHabits() {
  return render(
    <MemoryRouter>
      <AuthContext value={mockAuth}>
        <HabitsPage />
      </AuthContext>
    </MemoryRouter>,
  );
}

describe("HabitsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows the page heading", async () => {
    renderHabits();
    expect(await screen.findByText("Mes Habitudes")).toBeInTheDocument();
  });

  it("shows active habit names", async () => {
    renderHabits();
    expect(
      await screen.findByText("Marcher 10 min apres le dejeuner"),
    ).toBeInTheDocument();
    expect(screen.getByText("1 fruit avant midi")).toBeInTheDocument();
  });

  it("shows streak for habits", async () => {
    renderHabits();
    expect(await screen.findByText(/12 jours/)).toBeInTheDocument();
    expect(screen.getByText(/5 jours/)).toBeInTheDocument();
  });

  it("shows complete button for uncompleted habit", async () => {
    renderHabits();
    const completeBtn = await screen.findByLabelText(
      "Completer Marcher 10 min apres le dejeuner",
    );
    expect(completeBtn).toBeInTheDocument();
  });

  it("shows add button when under max habits", async () => {
    renderHabits();
    expect(await screen.findByText("Ajouter une habitude")).toBeInTheDocument();
  });
});
