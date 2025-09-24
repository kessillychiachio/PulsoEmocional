import React, { useState } from "react";
import { analisarManual, processarYoutube, YoutubeResp } from "../services/api";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "./ui/tabs";
import {
  Alert,
  AlertDescription,
  AlertTitle,
} from "./ui/alert";
import {
  Brain,
  Send,
  Smile,
  Frown,
  Meh,
  Clock,
  BarChart3,
  Youtube,
  Link,
  RefreshCw,
  Shield,
  FileText,
  ThumbsUp,
  ThumbsDown,
} from "lucide-react";
import { SentimentChart } from "./SentimentChart";
import { AnalysisHistory } from "./AnalysisHistory";
import { toast } from "sonner";

interface SentimentResult {
  id: string;
  text: string;
  sentiment: "positive" | "negative" | "neutral";
  confidence: number;
  emotions: {
    joy: number;
    sadness: number;
    anger: number;
    fear: number;
    surprise: number;
  };
  timestamp: Date;
  source: "manual" | "youtube";
  author?: string;
}

const mapPolaridade = (p: string): "positive" | "negative" | "neutral" => {
  const v = (p || "").toUpperCase().trim();
  if (v === "POSITIVO") return "positive";
  if (v === "NEGATIVO") return "negative";
  return "neutral";
};

const extractVideoId = (urlOrId: string): string | null => {
  const s = urlOrId.trim();
  if (/^[a-zA-Z0-9_-]{11}$/.test(s)) return s;
  const m = s.match(/[?&]v=([a-zA-Z0-9_-]{11})/) || s.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/);
  return m ? m[1] : null;
};

export function Dashboard() {
  const [text, setText] = useState("");
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<SentimentResult[]>([]);
  const [currentResult, setCurrentResult] = useState<SentimentResult | null>(null);

  const analyzeText = async (inputText?: string) => {
    const textToAnalyze = (inputText ?? text).trim();
    if (!textToAnalyze) {
      toast.error("Por favor, insira um texto para análise");
      return;
    }
    setIsAnalyzing(true);
    try {
      const r = await analisarManual({ texto: textToAnalyze });
      const result: SentimentResult = {
        id: r.id?.toString() || Date.now().toString(),
        text: r.texto || textToAnalyze,
        sentiment: mapPolaridade(r.polaridade),
        confidence: typeof r.confianca === "number" ? r.confianca : 0.9,
        emotions: { joy: 0, sadness: 0, anger: 0, fear: 0, surprise: 0 },
        timestamp: r.criado_em ? new Date(r.criado_em) : new Date(),
        source: "manual",
      };
      setResults(prev => [result, ...prev]);
      setCurrentResult(result);
      setText("");
      toast.success("Análise concluída!");
    } catch (e: any) {
      toast.error(e?.message || "Erro ao analisar texto");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const connectYouTube = async () => {
    const vid = extractVideoId(youtubeUrl);
    if (!vid) {
      toast.error("Informe uma URL válida do YouTube ou um videoId de 11 caracteres");
      return;
    }
    setIsAnalyzing(true);
    try {
      const data: YoutubeResp = await processarYoutube(vid, 60);
      const classificados = (data.classificados || []).map((c, idx) => {
        return {
          id: `${Date.now()}-${idx}`,
          text: c.Texto,
          sentiment: mapPolaridade(c.Polaridade),
          confidence: 0.9,
          emotions: { joy: 0, sadness: 0, anger: 0, fear: 0, surprise: 0 },
          timestamp: new Date(),
          source: "youtube" as const,
        } as SentimentResult;
      });
      setResults(prev => [...classificados, ...prev]);
      if (classificados[0]) setCurrentResult(classificados[0]);
      toast.success("Comentários coletados e classificados!");
    } catch (e: any) {
      toast.error(e?.message || "Erro ao processar vídeo");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return <Smile className="h-5 w-5 text-green-500" aria-label="Sentimento positivo" />;
      case "negative":
        return <Frown className="h-5 w-5 text-red-500" aria-label="Sentimento negativo" />;
      default:
        return <Meh className="h-5 w-5 text-yellow-500" aria-label="Sentimento neutro" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "bg-green-100 text-green-800 border-green-200";
      case "negative":
        return "bg-red-100 text-red-800 border-red-200";
      default:
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
    }
  };

  const getSentimentLabel = (sentiment: string) => {
    switch (sentiment) {
      case "positive":
        return "Positivo";
      case "negative":
        return "Negativo";
      default:
        return "Neutro";
    }
  };

  const stats = {
    totalAnalyses: results.length,
    positiveCount: results.filter(r => r.sentiment === "positive").length,
    negativeCount: results.filter(r => r.sentiment === "negative").length,
    neutralCount: results.filter(r => r.sentiment === "neutral").length,
    avgConfidence: results.length > 0 ? results.reduce((acc, r) => acc + r.confidence, 0) / results.length : 0,
    youtubeComments: results.filter(r => r.source === "youtube").length,
  };

  const generateSummary = () => {
    if (results.length === 0) return "Nenhum comentário analisado ainda.";
    const totalComments = results.length;
    const positivePercentage = ((stats.positiveCount / totalComments) * 100).toFixed(1);
    const negativePercentage = ((stats.negativeCount / totalComments) * 100).toFixed(1);
    const neutralPercentage = ((stats.neutralCount / totalComments) * 100).toFixed(1);
    let mainSentiment = "neutro";
    if (stats.positiveCount > stats.negativeCount && stats.positiveCount > stats.neutralCount) mainSentiment = "positivo";
    else if (stats.negativeCount > stats.positiveCount && stats.negativeCount > stats.neutralCount) mainSentiment = "negativo";
    let summary = `**Resumo Geral dos Comentários**\n\n`;
    summary += `Foram analisados ${totalComments} comentários ao total. `;
    summary += `O sentimento geral é **${mainSentiment}**, com ${positivePercentage}% positivos, ${negativePercentage}% negativos e ${neutralPercentage}% neutros.\n\n`;
    if (stats.positiveCount > 0) {
      summary += `**Aspectos Positivos:**\n`;
      summary += `• Os usuários demonstram satisfação com o conteúdo\n`;
      summary += `• Há engajamento positivo da audiência\n`;
      summary += `• Palavras-chave positivas frequentes: "amo", "ótimo", "parabéns", "incrível"\n\n`;
    }
    if (stats.negativeCount > 0) {
      summary += `**Pontos de Atenção:**\n`;
      summary += `• Alguns usuários expressaram insatisfação\n`;
      summary += `• Há comentários que podem precisar de moderação\n`;
      summary += `• Considere revisar aspectos que geram feedback negativo\n\n`;
    }
    summary += `**Recomendações:**\n`;
    if (stats.positiveCount > stats.negativeCount) {
      summary += `• Continue com a estratégia atual, pois está gerando boa recepção\n`;
      summary += `• Aproveite o engajamento positivo para criar mais conteúdo similar\n`;
    } else if (stats.negativeCount > stats.positiveCount) {
      summary += `• Analise os comentários negativos para identificar melhorias\n`;
      summary += `• Considere ajustar a abordagem do conteúdo\n`;
    }
    summary += `• Monitore continuamente o sentimento da audiência para otimizar a estratégia`;
    return summary;
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
              Análise de Sentimento
            </TabsTrigger>
            <TabsTrigger value="moderation" className="flex items-center gap-2">
              <Shield className="h-4 w-4" aria-hidden="true" />
              Moderação Inteligente
            </TabsTrigger>
            <TabsTrigger value="summary" className="flex items-center gap-2">
              <FileText className="h-4 w-4" aria-hidden="true" />
              Resumo
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
                        />
                        <Button
                          onClick={connectYouTube}
                          disabled={isAnalyzing}
                          className="bg-red-600 hover:bg-red-700 focus:ring-2 focus:ring-red-500"
                          aria-label="Conectar ao vídeo do YouTube"
                        >
                          {isAnalyzing ? <RefreshCw className="h-4 w-4 animate-spin" aria-hidden="true" /> : <Link className="h-4 w-4" aria-hidden="true" />}
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Brain className="h-5 w-5 text-purple-600" aria-hidden="true" />
                      Análise Manual de Texto
                    </CardTitle>
                    <CardDescription>Digite ou cole qualquer texto para análise de sentimentos</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="manual-text">Texto para análise</Label>
                      <Textarea
                        id="manual-text"
                        placeholder="Digite seu texto aqui... (ex: 'Eu amo este produto, é simplesmente fantástico!')"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        className="min-h-32"
                        aria-describedby="text-count"
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <span id="text-count" className="text-sm text-gray-500" aria-live="polite">
                        {text.length} caracteres
                      </span>
                      <Button
                        onClick={() => analyzeText(text)}
                        disabled={isAnalyzing || !text.trim()}
                        className="bg-purple-600 hover:bg-purple-700 focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                        aria-label="Analisar sentimento do texto digitado"
                      >
                        {isAnalyzing ? (
                          <>
                            <Clock className="h-4 w-4 mr-2 animate-spin" aria-hidden="true" />
                            Analisando...
                          </>
                        ) : (
                          <>
                            <Send className="h-4 w-4 mr-2" aria-hidden="true" />
                            Analisar Sentimento
                          </>
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>

                {currentResult && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        {getSentimentIcon(currentResult.sentiment)}
                        Último Resultado
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <p className="text-sm text-gray-600">
                            {currentResult.source === "youtube" ? "Comentário do YouTube:" : "Texto analisado:"}
                          </p>
                        </div>
                        <p className="text-gray-900">"{currentResult.text}"</p>
                      </div>

                      <div className="flex items-center gap-4">
                        <Badge className={getSentimentColor(currentResult.sentiment)}>
                          {getSentimentLabel(currentResult.sentiment)}
                        </Badge>
                        <div className="flex items-center gap-2">
                          <span className="text-sm text-gray-600">Confiança:</span>
                          <Progress value={currentResult.confidence * 100} className="w-24" aria-label={`Confiança de ${(currentResult.confidence * 100).toFixed(1)}%`} />
                          <span className="text-sm font-medium">{(currentResult.confidence * 100).toFixed(1)}%</span>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <h4 className="font-medium text-gray-900">Detalhamento das Emoções:</h4>
                        <div className="grid grid-cols-2 gap-3">
                          <div className="flex items-center justify-between p-2 bg-yellow-50 rounded" role="group" aria-label="Nível de alegria">
                            <span className="text-sm">😊 Alegria</span>
                            <span className="text-sm font-medium" aria-label={`${currentResult.emotions.joy.toFixed(1)} por cento`}>{currentResult.emotions.joy.toFixed(1)}%</span>
                          </div>
                          <div className="flex items-center justify-between p-2 bg-blue-50 rounded" role="group" aria-label="Nível de tristeza">
                            <span className="text-sm">😢 Tristeza</span>
                            <span className="text-sm font-medium" aria-label={`${currentResult.emotions.sadness.toFixed(1)} por cento`}>{currentResult.emotions.sadness.toFixed(1)}%</span>
                          </div>
                          <div className="flex items-center justify-between p-2 bg-red-50 rounded" role="group" aria-label="Nível de raiva">
                            <span className="text-sm">😠 Raiva</span>
                            <span className="text-sm font-medium" aria-label={`${currentResult.emotions.anger.toFixed(1)} por cento`}>{currentResult.emotions.anger.toFixed(1)}%</span>
                          </div>
                          <div className="flex items-center justify-between p-2 bg-purple-50 rounded" role="group" aria-label="Nível de medo">
                            <span className="text-sm">😨 Medo</span>
                            <span className="text-sm font-medium" aria-label={`${currentResult.emotions.fear.toFixed(1)} por cento`}>{currentResult.emotions.fear.toFixed(1)}%</span>
                          </div>
                          <div className="flex items-center justify-between p-2 bg-green-50 rounded" role="group" aria-label="Nível de surpresa">
                            <span className="text-sm">😲 Surpresa</span>
                            <span className="text-sm font-medium" aria-label={`${currentResult.emotions.surprise.toFixed(1)} por cento`}>{currentResult.emotions.surprise.toFixed(1)}%</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>

              <div className="space-y-6">
                <SentimentChart results={results} />
                <AnalysisHistory />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="moderation" className="space-y-6" role="tabpanel">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-red-600" aria-hidden="true" />
                  Moderação Inteligente
                </CardTitle>
                <CardDescription>Comentários classificados como negativos que podem precisar de atenção</CardDescription>
              </CardHeader>
              <CardContent>
                {results.filter((r) => r.sentiment === "negative").length === 0 ? (
                  <div className="text-center py-8">
                    <Shield className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Nenhum comentário negativo encontrado</p>
                    <p className="text-sm text-gray-400 mt-2">Quando houver comentários negativos, eles aparecerão aqui para moderação</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <p className="text-sm text-gray-600">
                        {results.filter((r) => r.sentiment === "negative").length} comentários negativos encontrados
                      </p>
                      <Badge variant="outline" className="bg-red-50 text-red-700 border-red-200">Requer Atenção</Badge>
                    </div>
                    {results
                      .filter((r) => r.sentiment === "negative")
                      .map((result) => (
                        <Card key={result.id} className="border-red-200 bg-red-50">
                          <CardContent className="pt-4">
                            <div className="flex items-start justify-between mb-2">
                              <div className="flex items-center gap-2">
                                <Frown className="h-4 w-4 text-red-500" aria-hidden="true" />
                                <span className="text-sm font-medium text-red-700">Comentário Negativo</span>
                              </div>
                              <span className="text-xs text-gray-500">{result.timestamp.toLocaleString()}</span>
                            </div>
                            <p className="text-gray-900 mb-3">"{result.text}"</p>
                            <div className="flex items-center gap-4">
                              <div className="flex items-center gap-2">
                                <span className="text-sm text-gray-600">Confiança:</span>
                                <Progress value={result.confidence * 100} className="w-20" aria-label={`Confiança de ${(result.confidence * 100).toFixed(1)}%`} />
                                <span className="text-sm font-medium">{(result.confidence * 100).toFixed(1)}%</span>
                              </div>
                              <div className="flex gap-2 ml-auto">
                                <Button size="sm" variant="outline" className="text-xs">Aprovar</Button>
                                <Button size="sm" variant="outline" className="text-xs text-red-600 border-red-200 hover:bg-red-50">Remover</Button>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                  </div>
                )}
              </CardContent>
            </Card>
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
                {results.length === 0 ? (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Nenhum comentário analisado ainda</p>
                    <p className="text-sm text-gray-400 mt-2">Comece analisando alguns comentários para ver o resumo aqui</p>
                  </div>
                ) : (
                  <div className="space-y-6">
                    <div className="prose max-w-none">
                      <div className="whitespace-pre-wrap text-gray-700">{generateSummary()}</div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 pt-6 border-t">
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600 mb-1">{stats.positiveCount}</div>
                        <div className="text-sm text-green-700">Comentários Positivos</div>
                        <div className="text-xs text-green-600 mt-1">{((stats.positiveCount / results.length) * 100).toFixed(1)}% do total</div>
                      </div>
                      <div className="text-center p-4 bg-red-50 rounded-lg">
                        <div className="text-2xl font-bold text-red-600 mb-1">{stats.negativeCount}</div>
                        <div className="text-sm text-red-700">Comentários Negativos</div>
                        <div className="text-xs text-red-600 mt-1">{((stats.negativeCount / results.length) * 100).toFixed(1)}% do total</div>
                      </div>
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-gray-600 mb-1">{stats.neutralCount}</div>
                        <div className="text-sm text-gray-700">Comentários Neutros</div>
                        <div className="text-xs text-gray-600 mt-1">{((stats.neutralCount / results.length) * 100).toFixed(1)}% do total</div>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}