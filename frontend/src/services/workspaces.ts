import { BaseHttpClient, BaseHttpClientError } from "@/services/http";
import type { ICancelableClient } from '@/services/loading';
import type { OsmApiClient } from '@/services/osm';
import type { TdeiClient } from '@/services/tdei';

export class WorkspacesClientError extends Error {
  response: Response;

  constructor(response: Response) {
    super(`Workspaces request failed: ${response.statusText} (${response.url})`);
    this.response = response;
  }
}

export class WorkspacesClient extends BaseHttpClient implements ICancelableClient {
  #tdeiClient: TdeiClient;
  #osmClient: OsmApiClient;

  constructor(
    apiUrl: string,
    tdeiClient: TdeiClient,
    osmClient: OsmApiClient,
    signal?: AbortSignal
  ) {
    super(apiUrl, signal);

    this.#tdeiClient = tdeiClient;
    this.#osmClient = osmClient;
  }

  get auth() {
    return this.#tdeiClient.auth;
  }

  clone(signal?: AbortSignal) {
    return new WorkspacesClient(
      this._baseUrl,
      this.#tdeiClient,
      this.#osmClient,
      signal ?? this._abortSignal
    );
  }

  async getMyWorkspaces() {
    const response = await this._get('workspaces/mine');
    const workspaces = (await response.json()) ?? [];

    for (const workspace of workspaces) {
      workspace.createdAt = new Date(workspace.createdAt);
      workspace.tdeiMetadata = JSON.parse(workspace.tdeiMetadata || '{}');
    }

    return workspaces;
  }

  async getWorkspace(id: number) {
    try {
      const response = await this._get(`workspaces/${id}`);
      return await response.json();
    } catch (e: any) {
      return null;
    }
  }

  getWorkspaceBbox(id: number) {
    return this.#osmClient.getWorkspaceBbox(id);
  }

  #setAuthHeader() {
    if (this.#tdeiClient.auth.complete) {
      this._requestHeaders.Authorization = 'Bearer ' + this.#tdeiClient.auth.accessToken;
    }
  }

  async _send(url: string, method: string, body?: any, config?: object): Promise<Response> {
    try {
      await this.#tdeiClient.tryRefreshAuth();
      this.#setAuthHeader();

      return await super._send(url, method, body, config);
    } catch (e: any) {
      if (e instanceof BaseHttpClientError) {
        throw new WorkspacesClientError(e.response);
      }

      throw e;
    }
  }
}
