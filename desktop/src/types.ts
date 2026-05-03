export type ConnectionProtocol = "http" | "https" | "socks5";

export type ConnectionStatus =
  | "connected"
  | "disconnected"
  | "heartbeat"
  | "error";

export interface ClaimedVirtualMachine {
  user_id: string;
  host: string;
  port: number;
  protocol: ConnectionProtocol;
  access_token: string;
  token_type: "Bearer";
}

export interface ConnectionStatusMessage {
  status: ConnectionStatus;
  user_id?: string;
  host?: string;
  port?: number;
  protocol?: ConnectionProtocol;
  code?: string;
  detail?: string;
}
