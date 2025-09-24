export type Comentario = { Texto: string };
export type Classificado = { Texto: string; Polaridade: "POSITIVO" | "NEGATIVO" | "NEUTRO" | "OUTRO" | "DESCONHECIDO" | "erro" };
export type YoutubeResp = { comentarios: Comentario[]; classificados: Classificado[] };

export type AnaliseItem = {
  id: number;
  Texto: string;
  Polaridade: "POSITIVO" | "NEGATIVO" | "NEUTRO" | "OUTRO" | "DESCONHECIDO" | "erro";
  Origem: "manual" | "youtube";
  Confianca: number | null;
  CriadoEm: string;
};

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function processarYoutube(videoId: string, n = 60): Promise<YoutubeResp> {
  const resp = await fetch(`${BASE_URL}/api/youtube/processar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ video_id: videoId, n })
  });
  if (!resp.ok) throw new Error(await resp.text());
  return resp.json();
}

export async function classificarTexto(texto: string): Promise<Classificado> {
  const resp = await fetch(`${BASE_URL}/api/classificar/texto`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ texto })
  });
  if (!resp.ok) throw new Error(await resp.text());
  return resp.json();
}

export async function listarAnalises(limit = 20, offset = 0): Promise<AnaliseItem[]> {
  const resp = await fetch(`${BASE_URL}/api/analises?limit=${limit}&offset=${offset}`);
  if (!resp.ok) throw new Error(await resp.text());
  return resp.json();
}