import { BaseHttpClient, BaseHttpClientError } from '@/services/http';
import type { ICancelableClient } from '@/services/loading';

export class LeaderboardClientError extends Error {
  response: Response;

  constructor(response: Response) {
    super(`Leaderboard request failed: ${response.statusText} (${response.url})`);
    this.response = response;
  }
}

export class LeaderboardClient extends BaseHttpClient implements ICancelableClient {
  constructor(gatewayUrl: string, signal?: AbortSignal) {
    if (!gatewayUrl) {
        gatewayUrl = 'https://api.' + window.location.hostname + '/api';
    }

    super(gatewayUrl, signal);
  }

  async _getSimple(paramString: string) {
    const response = await fetch(this.url(paramString));

    if (!response.ok) {
        throw new BaseHttpClientError(response);
    }
  
    return response;
  }

  async getLeaderboard(params: URLSearchParams): Promise<any> {
    const response = await this._getSimple(`/leaderboard?${params.toString()}`);

    return (await response.json());
  }

  async getProfileMap(params: URLSearchParams): Promise<any> {
    const response = await this._getSimple(`/leaderboard/profile/map/?${params.toString()}`);

    return (await response.json());
  }

  async getProfileStats(params: URLSearchParams): Promise<any> {
    const response = await this._getSimple(`/leaderboard/profile/stats/?${params.toString()}`);

    return (await response.json());
  }
}