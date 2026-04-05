const BASE_URL = "/api/v1";
const AUTH_TOKEN_KEY = "vitalage-access-token";
const REFRESH_TOKEN_KEY = "vitalage-refresh-token";

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  patient_id: string;
  display_name: string;
}

export class ApiRequestError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(status: number, code: string, message: string) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
    this.code = code;
  }
}

function getToken(): string | null {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

function authHeaders(extra?: Record<string, string>): Record<string, string> {
  const headers: Record<string, string> = { ...extra };
  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

async function tryRefreshAndRetry(
  path: string,
  options: RequestInit,
): Promise<Response | null> {
  const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);
  if (!refreshToken) return null;

  try {
    const refreshResponse = await fetch(`${BASE_URL}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (!refreshResponse.ok) return null;

    const tokens = (await refreshResponse.json()) as TokenResponse;
    localStorage.setItem(AUTH_TOKEN_KEY, tokens.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);

    const retryHeaders = {
      ...(options.headers as Record<string, string>),
      Authorization: `Bearer ${tokens.access_token}`,
    };
    return await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers: retryHeaders,
    });
  } catch {
    return null;
  }
}

function clearAuthAndRedirect(): never {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem("vitalage-patient-id");
  window.location.href = "/connexion";
  throw new ApiRequestError(401, "UNAUTHORIZED", "Session expiree");
}

async function handleResponse(
  response: Response,
  path: string,
  options: RequestInit,
): Promise<Response> {
  if (response.status === 401) {
    const retried = await tryRefreshAndRetry(path, options);
    if (retried) return retried;
    clearAuthAndRedirect();
  }

  if (!response.ok) {
    let code = "UNKNOWN";
    let message = "Une erreur est survenue";
    try {
      const body = await response.json();
      code = body.code ?? body.detail ?? code;
      message = body.detail ?? body.message ?? message;
    } catch {
      message = response.statusText;
    }
    throw new ApiRequestError(response.status, code, message);
  }

  return response;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = authHeaders({ "Content-Type": "application/json" });
  const init: RequestInit = {
    ...options,
    headers: { ...headers, ...(options.headers as Record<string, string>) },
  };

  const response = await fetch(`${BASE_URL}${path}`, init);
  const validated = await handleResponse(response, path, init);
  return validated.json() as Promise<T>;
}

export interface CheckInData {
  patient_id: string;
  sleep_quality: number;
  energy_level: number;
  mood: string;
  symptoms?: string;
}

export interface CheckInResponse {
  id: string;
  patient_id: string;
  sleep_quality: number;
  energy_level: number;
  mood: string;
  symptoms: string | null;
  symptoms_structured: Record<string, unknown> | null;
  date: string;
  created_at: string;
}

export interface CheckInStatus {
  completed_today: boolean;
  streak: number;
  today_check_in: CheckInResponse | null;
}

export interface HabitResponse {
  id: string;
  patient_id: string;
  template_id: string;
  name: string;
  dimension: string;
  started_at: string;
  is_active: boolean;
  current_streak: number;
  completed_today: boolean;
}

export interface HabitTemplate {
  id: string;
  name: string;
  dimension: string;
  description: string;
}

export interface VitalityScore {
  patient_id: string;
  nutrition: number;
  sleep: number;
  activity: number;
  mood: number;
  overall: number;
  calculated_at: string;
  change_from_last_week: number | null;
}

export interface VitalityTrend {
  patient_id: string;
  period: string;
  data: Array<{
    date: string;
    overall: number;
    nutrition: number;
    sleep: number;
    activity: number;
    mood: number;
  }>;
}

export interface InsightData {
  id: string;
  insight_text: string;
  insight_type: string;
  correlation_data: Record<string, unknown>;
  generated_at: string;
}

export const api = {
  auth: {
    register(data: {
      email: string;
      password: string;
      given_name: string;
      family_name: string;
      display_name: string;
    }): Promise<TokenResponse> {
      return request("/auth/register", {
        method: "POST",
        body: JSON.stringify(data),
      });
    },

    login(email: string, password: string): Promise<TokenResponse> {
      return request("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
    },

    refresh(refreshToken: string): Promise<TokenResponse> {
      return fetch(`${BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
      }).then((r) => {
        if (!r.ok) throw new ApiRequestError(r.status, "REFRESH_FAILED", "");
        return r.json() as Promise<TokenResponse>;
      });
    },
  },

  checkIns: {
    submit(data: CheckInData): Promise<CheckInResponse> {
      return request("/check-ins", {
        method: "POST",
        body: JSON.stringify(data),
      });
    },

    history(patientId: string): Promise<CheckInResponse[]> {
      return request(`/check-ins/patients/${patientId}`);
    },

    status(patientId: string): Promise<CheckInStatus> {
      return request(`/check-ins/patients/${patientId}/status`);
    },
  },

  vitality: {
    score(patientId: string): Promise<VitalityScore> {
      return request(`/vitality/patients/${patientId}`);
    },

    trends(patientId: string, period = "7d"): Promise<VitalityTrend> {
      return request(`/vitality/patients/${patientId}/trends?period=${period}`);
    },
  },

  habits: {
    activate(data: {
      patient_id: string;
      template_id: string;
    }): Promise<HabitResponse> {
      return request("/habits/activate", {
        method: "POST",
        body: JSON.stringify(data),
      });
    },

    complete(habitId: string): Promise<{ status: string; message: string }> {
      return request(`/habits/${habitId}/complete`, { method: "POST" });
    },

    list(patientId: string): Promise<HabitResponse[]> {
      return request(`/habits/patients/${patientId}`);
    },

    templates(): Promise<HabitTemplate[]> {
      return request("/habits/templates");
    },
  },

  insights: {
    list(patientId: string): Promise<InsightData[]> {
      return request(`/insights/patients/${patientId}`);
    },
  },
};
