// WiFi Session API functions

import { apiRequest } from '../api-client';
import type {
  WiFiSessionResponse,
  WiFiSessionListResponse,
  CreateWiFiSessionRequest,
  QueryParams,
} from '../../types';

/**
 * Create a new WiFi session
 * @param sessionData - WiFi session data
 * @returns Created WiFi session
 */
export async function createWiFiSession(
  sessionData?: CreateWiFiSessionRequest
): Promise<WiFiSessionResponse> {
  return apiRequest<WiFiSessionResponse>('/wifi/connect', {
    method: 'POST',
    body: JSON.stringify(sessionData || {}),
  });
}

/**
 * Get WiFi session history for the current user
 * @param params - Query parameters for filtering and pagination
 * @returns List of WiFi sessions
 */
export async function getWiFiSessions(
  params?: QueryParams
): Promise<WiFiSessionListResponse> {
  const queryString = params ? `?${new URLSearchParams(params as Record<string, string>).toString()}` : '';
  return apiRequest<WiFiSessionListResponse>(`/wifi/sessions${queryString}`, {
    method: 'GET',
  });
}

/**
 * Get active WiFi sessions for the current user
 * @returns List of active WiFi sessions (not disconnected)
 */
export async function getActiveWiFiSessions(): Promise<WiFiSessionListResponse> {
  const sessions = await getWiFiSessions();
  return {
    ...sessions,
    sessions: sessions.sessions.filter((session) => !session.disconnected_at),
  };
}
