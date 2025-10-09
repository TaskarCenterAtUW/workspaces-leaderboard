import { BaseHttpClient, BaseHttpClientError } from "@/services/http";
import type { ICancelableClient } from '@/services/loading';
import type { TdeiClient } from '@/services/tdei';

export class OsmApiClientError extends Error {
  response: Response;

  constructor(response: Response) {
    super(`OSM API request failed: ${response.statusText} (${response.url})`);
    this.response = response;
  }
}

export class OsmApiClient extends BaseHttpClient implements ICancelableClient {
  #webUrl: string;
  #tdeiClient: TdeiClient;

  constructor(
    webUrl: string,
    apiUrl: string,
    tdeiClient: TdeiClient,
    signal?: AbortSignal
  ) {
    super(apiUrl, signal);

    this.#webUrl = webUrl;
    this.#tdeiClient = tdeiClient;
    this.#setAuthHeader();
    this._requestHeaders['Accept'] = 'text/plain';
    this._requestHeaders['Content-Type'] = 'text/plain';
  }

  get auth() {
    return this.#tdeiClient.auth;
  }

  clone(signal?: AbortSignal) {
    return new OsmApiClient(
      this.#webUrl,
      this._baseUrl,
      this.#tdeiClient,
      signal ?? this._abortSignal
    );
  }

  webUrl(rest: string) {
    return this.#webUrl + rest
  }

  async getWorkspaceBbox(id: number) {
    const response = await this._get(`workspaces/${id}/bbox.json`);

    if (response.status === 204) {
      return undefined
    }

    return await response.json();
  }

  async getExportBbox(id: number) {
    const bbox = await this.getWorkspaceBbox(id);

    if (bbox === undefined) {
      return undefined
    }

    // Passing the exact bounding box to the OSM map call may lose nodes on the
    // bounds. We grow the bounding box here to ensure that we export the whole
    // workspace. A bounding box of "-180,-90,180,90" covering the entire Earth
    // would be ideal, but this crashes CGImap's "map" endpoint as it allocates
    // memory for every tile in the coordinate space.
    //
    // TODO: consider implementing a dedicated endpoint for exporting the whole
    // workspace instead of reusing the existing "map" API.
    //
    const pad = 0.0000001;

    return `${bbox.min_lon},${bbox.min_lat},${bbox.max_lon + pad},${bbox.max_lat + pad}`;
  }

  async getWorkspaceData(workspaceId: number): Promise<Array> {
    const bboxParam = await this.getExportBbox(workspaceId);
    const response = await this._get(`map.json?bbox=${bboxParam}`, {
      headers: {
        ...this._requestHeaders,
        'Accept': 'application/json',
        'X-Workspace': workspaceId
      }
    });

    return (await response.json()).elements;
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

      const requestOptions = {
        credentials: 'include'
      }

      return await super._send(url, method, body, { ...requestOptions, ...config });
    } catch (e: any) {
      if (e instanceof BaseHttpClientError) {
        throw new OsmApiClientError(e.response);
      }

      throw e;
    }
  }
}
