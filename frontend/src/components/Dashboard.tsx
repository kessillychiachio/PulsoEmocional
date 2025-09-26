import React, { useState } from "react";
import { iniciarAnalise, deletarAnalise, VideoAnalise, Comentario } from "../services/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Smile, Frown, Meh, BarChart3, Youtube, Link as LinkIcon, RefreshCw, FileText, ThumbsUp, ThumbsDown, Clock } from "lucide-react";
import { SentimentChart } from "./SentimentChart";
import { AnalysisHistory } from "./AnalysisHistory";
import { toast } from "sonner";

const extractVideoId = (urlOrId: string): string | null => {
  const s = urlOrId.trim();
  if (/^[a-zA-Z0-9_-]{11}$/.test(s)) return s;
  const m = s.match(/[?&]v=([a-zA-Z0-9_-]{11})/) || s.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/);
  return m ? m[1] : null;
};

export function Dashboard() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analise, setAnalise] = useState<VideoAnalise | null>(null);

  const connectYouTube = async () => {
    const vid = extractVideoId(youtubeUrl);
    if (!vid) {
      toast.error("Informe uma URL válida do YouTube ou um videoId de 11 caracteres");
      return;
    }
    setIsAnalyzing(true);
    try {
      const novaAnalise: VideoAnalise = await iniciarAnalise(vid, 60);
      setAnalise(novaAnalise);
      toast.success("Análise concluída com sucesso!");
    } catch (e: any) {
      toast.error(e?.message || "Erro ao processar vídeo");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const deleteAnalysis = async () => {
    if (!analise) {
      toast.error("Nenhuma análise para deletar.");
      return;
    }
    setIsAnalyzing(true);
    try {
      await deletarAnalise(analise.video_id_youtube);
      setAnalise(null);
      setYoutubeUrl("");
      toast.success("Análise deletada com sucesso!");
    } catch (e: any) {
      toast.error(e?.message || "Erro ao deletar análise");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case "POSITIVO":
        return <Smile className="h-5 w-5 text-green-500" aria-label="Sentimento positivo" />;
      case "NEGATIVO":
        return <Frown className="h-5 w-5 text-red-500" aria-label="Sentimento negativo" />;
      default:
        return <Meh className="h-5 w-5 text-yellow-500" aria-label="Sentimento neutro" />;
    }
  };

  const stats = analise ? {
    totalAnalyses: analise.comentarios.length,
    positiveCount: analise.comentarios.filter(c => c.polaridade === "POSITIVO").length,
    negativeCount: analise.comentarios.filter(c => c.polaridade === "NEGATIVO").length,
    neutralCount: analise.comentarios.filter(c => c.polaridade === "NEUTRO" || c.polaridade === "DESCONHECIDO").length,
  } : {
    totalAnalyses: 0,
    positiveCount: 0,
    negativeCount: 0,
    neutralCount: 0,
  };

  const generateSummaryText = () => {
    if (!analise || !analise.resumo) return "Nenhum resumo gerado pela IA.";
    return analise.resumo;
  };

  return (
    <div className="min-h-screen p-6" role="main">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Análise de Sentimentos - YouTube</h1>
          <p className="text-gray-600">Monitore sentimentos em comentários do YouTube em tempo real</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de comentários</CardTitle>
              <BarChart3 className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold" aria-label={`${stats.totalAnalyses} análises totais`}>{stats.totalAnalyses}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Positivos</CardTitle>
              <ThumbsUp className="h-4 w-4 text-green-500" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600" aria-label={`${stats.positiveCount} comentários positivos`}>{stats.positiveCount}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Negativos</CardTitle>
              <ThumbsDown className="h-4 w-4 text-red-500" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600" aria-label={`${stats.negativeCount} comentários negativos`}>{stats.negativeCount}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Neutros</CardTitle>
              <Meh className="h-4 w-4 text-gray-500" aria-hidden="true" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-600" aria-label={`${stats.neutralCount} comentários neutros`}>{stats.neutralCount}</div>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="sentiment" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3" role="tablist">
            <TabsTrigger value="sentiment" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" aria-hidden="true" />
              Análise
            </TabsTrigger>
            <TabsTrigger value="summary" className="flex items-center gap-2">
              <FileText className="h-4 w-4" aria-hidden="true" />
              Resumo
            </TabsTrigger>
            <TabsTrigger value="history" className="flex items-center gap-2">
              <Clock className="h-4 w-4" aria-hidden="true" />
              Histórico de vídeos
            </TabsTrigger>
          </TabsList>

          <TabsContent value="sentiment" className="space-y-6" role="tabpanel">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Youtube className="h-5 w-5 text-red-600" aria-hidden="true" />
                      Conectar ao YouTube
                    </CardTitle>
                    <CardDescription>Cole a URL do vídeo do YouTube para começar a análise</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="youtube-url">URL do YouTube</Label>
                      <div className="flex gap-2">
                        <Input
                          id="youtube-url"
                          placeholder="https://www.youtube.com/watch?v=..."
                          value={youtubeUrl}
                          onChange={(e) => setYoutubeUrl(e.target.value)}
                          className="flex-1"
                          aria-describedby="youtube-url-help"
                          disabled={isAnalyzing}
                        />
                        <Button
                          onClick={connectYouTube}
                          disabled={isAnalyzing || !youtubeUrl.trim()}
                          className="bg-red-600 hover:bg-red-700 focus:ring-2 focus:ring-red-500"
                          aria-label="Conectar ao vídeo do YouTube"
                        >
                          {isAnalyzing ? <RefreshCw className="h-4 w-4 animate-spin" aria-hidden="true" /> : <LinkIcon className="h-4 w-4" aria-hidden="true" />}
                        </Button>
                      </div>
                      {analise && (
                        <div className="flex justify-end mt-2">
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={deleteAnalysis}
                            disabled={isAnalyzing}
                            aria-label="Deletar análise atual"
                          >
                            Deletar Análise
                          </Button>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <div className="space-y-6">
                <SentimentChart comments={analise ? analise.comentarios : []} />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="summary" className="space-y-6" role="tabpanel">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-blue-600" aria-hidden="true" />
                  Resumo dos Comentários
                </CardTitle>
                <CardDescription>Análise consolidada de todos os comentários processados</CardDescription>
              </CardHeader>
              <CardContent>
                {!analise ? (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Nenhum comentário analisado ainda</p>
                    <p className="text-sm text-gray-400 mt-2">Comece analisando alguns comentários para ver o resumo aqui</p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="prose max-w-none">
                      <p className="whitespace-pre-wrap text-gray-700">{generateSummaryText()}</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 pt-6 border-t">
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600 mb-1">{stats.positiveCount}</div>
                        <div className="text-sm text-green-700">Comentários Positivos</div>
                        <div className="text-xs text-green-600 mt-1">{((stats.positiveCount / stats.totalAnalyses) * 100).toFixed(1)}% do total</div>
                      </div>
                      <div className="text-center p-4 bg-red-50 rounded-lg">
                        <div className="text-2xl font-bold text-red-600 mb-1">{stats.negativeCount}</div>
                        <div className="text-sm text-red-700">Comentários Negativos</div>
                        <div className="text-xs text-red-600 mt-1">{((stats.negativeCount / stats.totalAnalyses) * 100).toFixed(1)}% do total</div>
                      </div>
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-gray-600 mb-1">{stats.neutralCount}</div>
                        <div className="text-sm text-gray-700">Comentários Neutros</div>
                        <div className="text-xs text-gray-600 mt-1">{((stats.neutralCount / stats.totalAnalyses) * 100).toFixed(1)}% do total</div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="history" className="space-y-6" role="tabpanel">
            <AnalysisHistory />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
