import React, { useEffect, useState } from "react";
import { listarAnalises, AnaliseItem } from "../services/api";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { ScrollArea } from "./ui/scroll-area";
import { Button } from "./ui/button";
import { Clock, Youtube, MessageSquare, Loader2 } from "lucide-react";

const polClass: Record<string, string> = {
  POSITIVO: "bg-green-100 text-green-800 border-green-200",
  NEGATIVO: "bg-red-100 text-red-800 border-red-200",
  NEUTRO: "bg-yellow-100 text-yellow-800 border-yellow-200",
  OUTRO: "bg-gray-100 text-gray-800 border-gray-200",
  DESCONHECIDO: "bg-gray-100 text-gray-800 border-gray-200",
  erro: "bg-gray-100 text-gray-800 border-gray-200"
};

export function AnalysisHistory() {
  const [items, setItems] = useState<AnaliseItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [moreLoading, setMoreLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const limit = 20;
  const hasMore = items.length >= offset + limit;

  const formatTime = (iso: string) => {
    return new Date(iso).toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit"
    });
  };

  const carregar = async () => {
    setLoading(true);
    try {
      const data = await listarAnalises(limit, 0);
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
      const nextOffset = offset + limit;
      const data = await listarAnalises(limit, nextOffset);
      setItems(prev => [...prev, ...data]);
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
          Histórico de Análises
        </CardTitle>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-6 w-6 animate-spin" />
          </div>
        ) : items.length === 0 ? (
          <div className="text-center text-gray-500 py-6" role="status" aria-live="polite">
            <p>Nenhuma análise salva ainda</p>
            <p className="text-sm">As análises aparecerão aqui quando forem feitas</p>
          </div>
        ) : (
          <>
            <ScrollArea className="h-96" role="log" aria-label="Lista de análises salvas">
              <div className="space-y-4">
                {items.map((it, idx) => (
                  <article
                    key={it.id}
                    className="border rounded-lg p-4 space-y-3 hover:bg-gray-50 transition-colors"
                    aria-labelledby={`item-${it.id}-title`}
                  >
                    <header className="flex items-start justify-between">
                      <div className="flex items-center gap-2">
                        <Badge className={polClass[it.Polaridade] || polClass.OUTRO}>
                          {it.Polaridade}
                        </Badge>
                        {it.Origem === "youtube" ? (
                          <Badge variant="outline" className="text-xs bg-red-50 text-red-700 border-red-200">
                            <Youtube className="h-3 w-3 mr-1" aria-hidden="true" />
                            YouTube
                          </Badge>
                        ) : (
                          <Badge variant="outline" className="text-xs">
                            <MessageSquare className="h-3 w-3 mr-1" aria-hidden="true" />
                            Manual
                          </Badge>
                        )}
                      </div>
                      <time className="text-xs text-gray-500" dateTime={it.CriadoEm}>
                        {formatTime(it.CriadoEm)}
                      </time>
                    </header>

                    <blockquote className="text-sm text-gray-800" id={`item-${it.id}-title`}>
                      <p>"{it.Texto}"</p>
                    </blockquote>

                    <footer className="flex items-center justify-between text-xs text-gray-500">
                      <span>Origem: {it.Origem}</span>
                      {typeof it.Confianca === "number" && (
                        <span>Confiança: {(it.Confianca * 100).toFixed(1)}%</span>
                      )}
                      {idx === 0 && (
                        <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">
                          Mais recente
                        </Badge>
                      )}
                    </footer>
                  </article>
                ))}
              </div>
            </ScrollArea>

            <div className="flex justify-center mt-4">
              <Button variant="outline" onClick={carregarMais} disabled={moreLoading || !hasMore}>
                {moreLoading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                {hasMore ? "Carregar mais" : "Fim do histórico"}
              </Button>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}