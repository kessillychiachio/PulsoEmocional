import React from "react";
import { Button } from "./ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Badge } from "./ui/badge";
import {
  Brain,
  Zap,
  Shield,
  TrendingUp,
  MessageCircle,
  BarChart3,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  Youtube,
  Radio,
  Users,
  Clock,
  Eye,
  Heart,
  FileText,
} from "lucide-react";

interface LandingPageProps {
  setCurrentPage: (page: "dashboard") => void;
}

export function LandingPage({
  setCurrentPage,
}: LandingPageProps) {
  const features = [
    {
      icon: Youtube,
      title: "Integração YouTube",
      description:
        "Adicione diretamente vídeos do YouTube para análise automática",
    },
    {
      icon: Users,
      title: "Engajamento da Audiência",
      description:
        "Entenda como sua audiência está reagindo em tempo real",
    },
    {
      icon: TrendingUp,
      title: "Insights Acionáveis",
      description:
        "Relatórios detalhados para melhorar o conteúdo e engajamento",
    },
  ];

  const useCases = [
    {
      icon: Eye,
      title: "Análise de sentimento em Vídeos",
      description:
        "Analise comentários de vídeos publicados para entender a recepção do público como positiva, negativa ou neutra",
    },
    {
      icon: Heart,
      title: "Moderação Inteligente",
      description:
        "Identifique comentários negativos automaticamente para moderação proativa",
    },
    {
      icon: FileText,
      title: "Resumo",
      description:
        "Gere resumos concisos de opiniões ou pontos de vista compartilhados nos comentários",
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="pt-20 pb-32 px-4" role="banner">
        <div className="max-w-7xl mx-auto text-center">
          <Badge
            className="mb-8 bg-red-100 text-red-800 border-red-200"
            aria-label="Produto focado em YouTube"
          >
            <Youtube
              className="h-4 w-4 mr-2"
              aria-hidden="true"
            />
            Especializado em YouTube
          </Badge>

          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Analise{" "}
            <span className="text-red-600">Comentários</span> do
            YouTube com{" "}
            <span className="text-purple-600">IA</span>
          </h1>

          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
            O Pulso Emocional monitora sentimentos em
            comentários do YouTube, oferecendo insights valiosos
            sobre a reação da sua audiência.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              size="lg"
              className="bg-red-600 hover:bg-red-700 text-white px-8 py-6 text-lg focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
              onClick={() => setCurrentPage("dashboard")}
              aria-label="Começar análise gratuita de comentários do YouTube"
            >
              Começar Análise Gratuita
              <ArrowRight
                className="ml-2 h-5 w-5"
                aria-hidden="true"
              />
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section
        className="py-20 px-4 bg-white"
        role="region"
        aria-labelledby="features-heading"
      >
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2
              id="features-heading"
              className="text-3xl font-bold text-gray-900 mb-4"
            >
              Feito Especialmente para Criadores do YouTube
            </h2>
            <p className="text-xl text-gray-600">
              Recursos desenvolvidos para entender sua audiência
              em tempo real
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card
                key={index}
                className="border-red-100 hover:shadow-lg transition-shadow focus-within:ring-2 focus-within:ring-red-500 focus-within:ring-offset-2"
              >
                <CardHeader className="text-center">
                  <feature.icon
                    className="h-12 w-12 text-red-600 mx-auto mb-4"
                    aria-hidden="true"
                  />
                  <CardTitle className="text-lg">
                    {feature.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-center">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section
        className="py-20 px-4"
        role="region"
        aria-labelledby="usecases-heading"
      >
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2
              id="usecases-heading"
              className="text-3xl font-bold text-gray-900 mb-4"
            >
              Casos de Uso no YouTube
            </h2>
            <p className="text-xl text-gray-600">
              Como o Pulso Emocional pode transformar sua
              estratégia de conteúdo
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 px-[99px] mx-[6px] my-[0px] py-[0px]">
            {useCases.map((useCase, index) => (
              <Card
                key={index}
                className={`${useCase.highlight ? "border-red-200 bg-red-50" : "border-gray-200"} hover:shadow-lg transition-shadow focus-within:ring-2 focus-within:ring-red-500 focus-within:ring-offset-2`}
              >
                <CardHeader>
                  <useCase.icon
                    className={`h-8 w-8 ${useCase.highlight ? "text-red-600" : "text-gray-600"} mb-2`}
                    aria-hidden="true"
                  />
                  <CardTitle className="flex items-center gap-2">
                    {useCase.title}
                    {useCase.highlight && (
                      <Badge
                        variant="secondary"
                        className="bg-red-100 text-red-800"
                      >
                        Popular
                      </Badge>
                    )}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600">
                    {useCase.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Live Demo Section */}
      <section
        className="py-20 px-4 bg-gradient-to-r from-red-600 to-purple-600 text-white"
        role="region"
        aria-labelledby="demo-heading"
      >
        <div className="max-w-4xl mx-auto text-center">
          <Radio
            className="h-16 w-16 mx-auto mb-6 text-red-200"
            aria-hidden="true"
          />
          <h2
            id="demo-heading"
            className="text-3xl font-bold mb-4"
          >
            Experimente com Comentários Reais do YouTube
          </h2>
          <p className="text-xl mb-8 text-red-100">
            Cole o link do vídeo do YouTube para ver a análise
            em ação
          </p>
          <Button
            size="lg"
            className="bg-white text-red-600 hover:bg-gray-100 px-8 py-6 text-lg focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-red-600"
            onClick={() => setCurrentPage("dashboard")}
            aria-label="Experimentar análise de comentários do YouTube"
          >
            Experimentar Agora - É Grátis
            <Youtube
              className="ml-2 h-5 w-5"
              aria-hidden="true"
            />
          </Button>
        </div>
      </section>
    </div>
  );
}