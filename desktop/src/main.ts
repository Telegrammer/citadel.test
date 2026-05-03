import { claimVirtualMachine } from "./api";
import { getStatusWebSocketUrl } from "./config";
import type { ClaimedVirtualMachine, ConnectionStatusMessage } from "./types";

let socket: WebSocket | null = null;
let claimedMachine: ClaimedVirtualMachine | null = null;
let connectSessionId = 0;

const app = document.querySelector<HTMLDivElement>("#app");

if (!app) {
  throw new Error("Root element #app not found");
}

function requireElement<T extends Element>(selector: string): T {
  const element = document.querySelector<T>(selector);
  if (!element) {
    throw new Error(`Element ${selector} not found`);
  }
  return element;
}

app.innerHTML = `
  <section>
    <header>
      <h1>Citadel</h1>
      <p>Подключение виртуальной машины по ключу активации</p>
    </header>

    <label for="activation-key">Ключ активации</label>
    <br />
    <textarea id="activation-key" rows="4" cols="64" placeholder="lookup.secret"></textarea>
    <br />
    <button id="connect-button" type="button">Подключиться</button>
    <button id="disconnect-button" type="button">Отключиться</button>

    <h2>Статус</h2>
    <p id="status">Отключено</p>

    <h2>Виртуальная машина</h2>
    <div id="vm-info" aria-live="polite"></div>

    <h2>Консоль WebSocket</h2>
    <button id="clear-log-button" type="button">Очистить консоль</button>
    <br />
    <textarea id="ws-log" readonly rows="14" cols="64" aria-label="Консоль WebSocket">Нет сообщений</textarea>
  </section>
`;

const keyInput = requireElement<HTMLTextAreaElement>("#activation-key");
const connectButton = requireElement<HTMLButtonElement>("#connect-button");
const disconnectButton = requireElement<HTMLButtonElement>("#disconnect-button");
const statusOutput = requireElement<HTMLElement>("#status");
const vmOutput = requireElement<HTMLElement>("#vm-info");
const wsLogArea = requireElement<HTMLTextAreaElement>("#ws-log");
const clearLogButton = requireElement<HTMLButtonElement>("#clear-log-button");

const WS_LOG_EMPTY = "Нет сообщений";

function setStatus(value: string): void {
  statusOutput.textContent = value;
}

function scrollWsLogToBottom(): void {
  queueMicrotask(() => {
    wsLogArea.scrollTop = wsLogArea.scrollHeight;
  });
}

function writeLog(message: string): void {
  const line = `${new Date().toLocaleTimeString()} ${message}\n`;
  if (wsLogArea.value === WS_LOG_EMPTY) {
    wsLogArea.value = line;
  } else {
    wsLogArea.value += line;
  }
  scrollWsLogToBottom();
}

function clearWsLog(): void {
  wsLogArea.value = WS_LOG_EMPTY;
}

function statusText(status: ConnectionStatusMessage["status"]): string {
  switch (status) {
    case "connected":
      return "Подключено";
    case "disconnected":
      return "Отключено";
    case "heartbeat":
      return "Ожидание";
    case "error":
      return "Ошибка";
    default:
      return "Неизвестный статус";
  }
}

function statusLogMessage(message: ConnectionStatusMessage): string {
  const base = statusText(message.status);
  if (message.host && message.port && message.protocol) {
    return `${base}: ${message.protocol}://${message.host}:${message.port}`;
  }
  if (message.detail) {
    return `${base}: ${message.detail}`;
  }
  return base;
}

function addDefinitionRow(dl: HTMLDListElement, term: string, value: string): void {
  const dt = document.createElement("dt");
  dt.textContent = term;
  const dd = document.createElement("dd");
  dd.textContent = value;
  dl.append(dt, dd);
}

function renderMachine(machine: ClaimedVirtualMachine | null): void {
  vmOutput.replaceChildren();

  if (!machine) {
    const p = document.createElement("p");
    p.textContent = "Нет данных";
    vmOutput.appendChild(p);
    return;
  }

  const dl = document.createElement("dl");
  addDefinitionRow(dl, "Хост", machine.host);
  addDefinitionRow(dl, "Порт", String(machine.port));
  addDefinitionRow(dl, "Протокол", machine.protocol);
  vmOutput.appendChild(dl);
}

function closeSocket(): void {
  if (!socket) {
    return;
  }
  const ws = socket;
  socket = null;
  const state = ws.readyState;
  if (state === WebSocket.OPEN || state === WebSocket.CONNECTING) {
    ws.close(1000);
  }
}

function connectStatusWebSocket(machine: ClaimedVirtualMachine): void {
  closeSocket();

  socket = new WebSocket(getStatusWebSocketUrl(machine.access_token));

  socket.addEventListener("open", () => {
    writeLog("[ws] соединение открыто");
  });

  socket.addEventListener("message", (event) => {
    try {
      const payload = JSON.parse(String(event.data)) as ConnectionStatusMessage;
      setStatus(statusText(payload.status));
      writeLog(`[ws] ${statusLogMessage(payload)}`);
      if (payload.status === "disconnected") {
        closeSocket();
      }
    } catch {
      writeLog(`[ws] ${String(event.data)}`);
    }
  });

  socket.addEventListener("close", (event) => {
    setStatus("Отключено");
    writeLog(`[ws] соединение закрыто code=${event.code}`);
  });

  socket.addEventListener("error", () => {
    setStatus("Ошибка");
    writeLog("[ws] ошибка соединения");
  });
}

connectButton.addEventListener("click", async () => {
  const activationKey = keyInput.value.trim();

  if (!activationKey) {
    setStatus("Введите ключ активации");
    return;
  }

  const sessionId = ++connectSessionId;
  closeSocket();

  connectButton.disabled = true;
  setStatus("Ожидание");

  try {
    claimedMachine = await claimVirtualMachine(activationKey);
    if (sessionId !== connectSessionId) {
      return;
    }
    renderMachine(claimedMachine);
    setStatus("Подключено");
    writeLog("[api] виртуальная машина получена");
    connectStatusWebSocket(claimedMachine);
  } catch (error) {
    if (sessionId !== connectSessionId) {
      return;
    }
    claimedMachine = null;
    renderMachine(null);
    setStatus("Ошибка");
    writeLog(error instanceof Error ? `[api] ${error.message}` : "[api] неизвестная ошибка");
  } finally {
    connectButton.disabled = false;
  }
});

disconnectButton.addEventListener("click", () => {
  connectSessionId += 1;
  connectButton.disabled = false;
  closeSocket();
  claimedMachine = null;
  renderMachine(null);
  setStatus("Отключено");
});

clearLogButton.addEventListener("click", () => clearWsLog());
