const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface Comentario {
  texto: string;
  polaridade: "POSITIVO" | "NEGATIVO" | "NEUTRO" | "DESCONHECIDO" | "erro";
  emocao: string;
}

export interface VideoAnalise {
  id: number;
  video_id_youtube: string;
  resumo: string | null;
  criado_em: string;
  comentarios: Comentario[];
}

export async function iniciarAnalise(videoId: string, n_comentarios = 60): Promise<VideoAnalise> {
  const resp = await fetch(`${BASE_URL}/videos/analisar?video_id=${videoId}&n_comentarios=${n_comentarios}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  if (!resp.ok) {
    const errorData = await resp.json();
    throw new Error(errorData.detail || "Erro ao iniciar a análise.");
  }
  return resp.json();
}

export async function obterAnalise(videoId: string): Promise<VideoAnalise> {
  const resp = await fetch(`${BASE_URL}/videos/${videoId}`);
  if (!resp.ok) {
    const errorData = await resp.json();
    throw new Error(errorData.detail || "Erro ao obter análise.");
  }
  return resp.json();
}

export async function deletarAnalise(videoId: string): Promise<{ message: string }> {
  const resp = await fetch(`${BASE_URL}/videos/${videoId}`, {
    method: "DELETE",
  });
  if (!resp.ok) {
    const errorData = await resp.json();
    throw new Error(errorData.detail || "Erro ao deletar análise.");
  }
  return resp.json();
}