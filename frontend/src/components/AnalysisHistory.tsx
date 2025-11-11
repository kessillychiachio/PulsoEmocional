import React, { useEffect, useState } from "react";
import { listarVideosAnalisados, VideoOut, deletarAnalise } from "../services/api"; 
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { ScrollArea } from "./ui/scroll-area";
import { Clock, Youtube, Link as LinkIcon, Loader2, Trash } from "lucide-react"; 
import { Button } from "./ui/button"; 
import { toast } from "sonner";

const PAGE_SIZE = 20;

const fmtTime = (iso: string) =>
  new Date(iso).toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });

interface AnalysisHistoryProps {
  currentActiveVideoId: string | undefined;
  onDeleteSuccess: (deletedVideoId: string) => void;
}

export function AnalysisHistory({ currentActiveVideoId, onDeleteSuccess }: AnalysisHistoryProps) {
  const [items, setItems] = useState<VideoOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const carregar = async () => {
    setLoading(true);
    try {
      const data = await listarVideosAnalisados(PAGE_SIZE, 0);
      setItems(data);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (videoId: string, id: number) => {
    if (!window.confirm("Tem certeza que deseja deletar esta análise? Esta ação é irreversível.")) {
      return;
    }
    
    setDeletingId(id);
    try {
      await deletarAnalise(videoId);
      toast.success("Análise deletada com sucesso!");
      
      onDeleteSuccess(videoId);

      await carregar(); 

    } catch (e: any) {
      toast.error(e?.message || "Erro ao deletar análise");
    } finally {
      setDeletingId(null);
    }
  };

  useEffect(() => {
    carregar();
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5 text-purple-600" aria-hidden="true" />
          Vídeos analisados anteriormente
        </CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin" />
          </div>
        ) : items.length === 0 ? (
          <div className="text-center text-gray-500 py-6" role="status" aria-live="polite">
            <p>Nenhum vídeo analisado ainda</p>
            <p className="text-sm">Quando houver análises salvas, elas aparecerão aqui</p>
          </div>
        ) : (
          <ScrollArea className="h-139" role="log" aria-label="Lista de vídeos analisados">
            <div className="space-y-4">
              {items.map((it) => (
                <article 
                  key={it.id} 
                  className={`border rounded-lg p-4 space-y-3 transition-colors ${it.video_id_youtube === currentActiveVideoId ? 'border-purple-500 bg-purple-50 shadow-md' : 'hover:bg-gray-50'}`}
                  aria-current={it.video_id_youtube === currentActiveVideoId ? 'page' : 'false'}
                >
                  <header className="flex items-center justify-between">
                    <Badge variant="outline" className="text-xs bg-red-50 text-red-700 border-red-200 flex items-center gap-1">
                      <Youtube className="h-3 w-3" aria-hidden="true" />
                      YouTube
                    </Badge>
                    <time className="text-xs text-gray-500" dateTime={it.criado_em}>
                      {fmtTime(it.criado_em)}
                    </time>
                  </header>

                  <h3 className="text-sm font-semibold truncate" title={it.video_id_youtube}>
                    {it.video_id_youtube}
                  </h3>

                  <p className="text-sm text-gray-700 line-clamp-3">
                    {it.resumo ?? "Sem resumo disponível."}
                  </p>

                  <footer className="flex justify-between items-center mt-3">
                    {/* Elemento 1: Abrir Vídeo (Lado Esquerdo) */}
                    <a
                      href={`https://www.youtube.com/watch?v=${it.video_id_youtube}`}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1 text-blue-600 hover:underline text-xs"
                      aria-label="Abrir vídeo no YouTube"
                    >
                      <LinkIcon className="h-3 w-3" />
                      Abrir vídeo
                    </a>
                    
                    {/* Elemento 2: Deletar Botão (Lado Direito) */}
                    <Button
                      variant="destructive" 
                      onClick={() => handleDelete(it.video_id_youtube, it.id)}
                      disabled={deletingId === it.id}
                      className="text-xs h-6 px-2 py-1 rounded-full border border-red-200 flex items-center gap-1"
                      aria-label={`Deletar análise do vídeo ${it.video_id_youtube}`}
                    >
                      {deletingId === it.id ? (
                        <Loader2 className="h-3 w-3 animate-spin mr-1" />
                      ) : (
                        <Trash className="h-3 w-3 mr-1" aria-hidden="true" />
                      )}
                      Deletar
                    </Button>
                  </footer>
                </article>
              ))}
            </div>
          </ScrollArea>
        )}
      </CardContent>
    </Card>
  );
}