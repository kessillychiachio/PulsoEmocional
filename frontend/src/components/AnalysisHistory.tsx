import React, { useEffect, useMemo, useState } from "react";
import { listarVideosAnalisados, VideoAnaliseResumo } from "../services/api";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { ScrollArea } from "./ui/scroll-area";
import { Button } from "./ui/button";
import { Clock, Youtube, Link as LinkIcon, Loader2 } from "lucide-react";

const PAGE_SIZE = 20;

const fmtTime = (iso: string) =>
  new Date(iso).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

const thumbUrl = (id: string) => `https://img.youtube.com/vi/${id}/hqdefault.jpg`;

const polClass: Record<string, string> = {
  POSITIVO: "bg-green-100 text-green-800 border-green-200",
  NEGATIVO: "bg-red-100 text-red-800 border-red-200",
  NEUTRO: "bg-yellow-100 text-yellow-800 border-yellow-200",
  DESCONHECIDO: "bg-gray-100 text-gray-800 border-gray-200",
};

export function AnalysisHistory() {
  const [items, setItems] = useState<VideoAnaliseResumo[]>([]);
  const [loading, setLoading] = useState(true);
  const [moreLoading, setMoreLoading] = useState(false);
  const [offset, setOffset] = useState(0);

  const hasMore = useMemo(() => items.length >= offset + PAGE_SIZE, [items.length, offset]);

  const carregar = async () => {
    setLoading(true);
    try {
      const data = await listarVideosAnalisados(PAGE_SIZE, 0);
      setItems(data);
      setOffset(0);
    } finally {
      setLoading(false);
    }
  };

  const carregarMais = async () => {
    if (moreLoading) return;
    setMoreLoading(true);
    try {
      const nextOffset = offset + PAGE_SIZE;
      const data = await listarVideosAnalisados(PAGE_SIZE, nextOffset);
      setItems((prev) => [...prev, ...data]);
      setOffset(nextOffset);
    } finally {
      setMoreLoading(false);
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
          Vídeos Analisados
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
          <>
            <ScrollArea className="h-96" role="log" aria-label="Lista de vídeos analisados">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {items.map((it, idx) => (
                  <article
                    key={`${it.video_id_youtube}-${idx}`}
                    className="border rounded-lg overflow-hidden"
                  >
                    <div className="flex">
                      <img
                        src={thumbUrl(it.video_id_youtube)}
                        alt={`Thumbnail do vídeo ${it.video_id_youtube}`}
                        className="w-40 h-28 object-cover"
                        loading="lazy"
                      />
                      <div className="flex-1 p-4 space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <Badge
                              variant="outline"
                              className="text-xs bg-red-50 text-red-700 border-red-200"
                            >
                              <Youtube className="h-3 w-3 mr-1" aria-hidden="true" />
                              YouTube
                            </Badge>
                            {it.polaridade_geral ? (
                              <Badge className={polClass[it.polaridade_geral] || polClass.DESCONHECIDO}>
                                {it.polaridade_geral}
                              </Badge>
                            ) : null}
                          </div>
                          <time className="text-xs text-gray-500" dateTime={it.criado_em}>
                            {fmtTime(it.criado_em)}
                          </time>
                        </div>

                        <h3
                          className="text-sm font-semibold truncate"
                          title={it.video_id_youtube}
                        >
                          {it.video_id_youtube}
                        </h3>

                        <p className="text-sm text-gray-700 line-clamp-3">
                          {it.resumo || "Sem resumo disponível."}
                        </p>

                        <div className="flex items-center justify-between text-xs text-gray-500">
                          {typeof it.total_comentarios === "number" ? (
                            <span>{it.total_comentarios} comentários</span>
                          ) : (
                            <span />
                          )}
                          <a
                            href={`https://www.youtube.com/watch?v=${it.video_id_youtube}`}
                            target="_blank"
                            rel="noreferrer"
                            className="inline-flex items-center gap-1 text-blue-600 hover:underline"
                            aria-label="Abrir vídeo no YouTube"
                          >
                            <LinkIcon className="h-3 w-3" />
                            Abrir vídeo
                          </a>
                        </div>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </ScrollArea>

            <div className="flex justify-center mt-4">
              <Button
                variant="outline"
                onClick={carregarMais}
                disabled={moreLoading || !hasMore}
              >
                {moreLoading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                {hasMore ? "Carregar mais" : "Fim da lista"}
              </Button>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
