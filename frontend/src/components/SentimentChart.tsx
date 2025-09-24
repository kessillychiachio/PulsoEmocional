import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LineChart, Line } from 'recharts';
import { TrendingUp, Youtube, MessageSquare } from 'lucide-react';

interface SentimentResult {
  id: string;
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  confidence: number;
  emotions: {
    joy: number;
    sadness: number;
    anger: number;
    fear: number;
    surprise: number;
  };
  timestamp: Date;
  source: 'manual' | 'youtube';
  author?: string;
}

interface SentimentChartProps {
  results: SentimentResult[];
}

export function SentimentChart({ results }: SentimentChartProps) {
  if (results.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-purple-600" aria-hidden="true" />
            Distribuição de Sentimentos
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-gray-500 py-8" role="status" aria-live="polite">
            <p>Nenhuma análise realizada ainda</p>
            <p className="text-sm">Faça sua primeira análise para ver os gráficos</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  const sentimentData = [
    {
      name: 'Positivo',
      value: results.filter(r => r.sentiment === 'positive').length,
      color: '#10B981',
      percentage: ((results.filter(r => r.sentiment === 'positive').length / results.length) * 100).toFixed(1)
    },
    {
      name: 'Negativo',
      value: results.filter(r => r.sentiment === 'negative').length,
      color: '#EF4444',
      percentage: ((results.filter(r => r.sentiment === 'negative').length / results.length) * 100).toFixed(1)
    },
    {
      name: 'Neutro',
      value: results.filter(r => r.sentiment === 'neutral').length,
      color: '#F59E0B',
      percentage: ((results.filter(r => r.sentiment === 'neutral').length / results.length) * 100).toFixed(1)
    }
  ];

  const emotionData = results.length > 0 ? [
    {
      name: 'Alegria',
      value: results.reduce((acc, r) => acc + r.emotions.joy, 0) / results.length,
      color: '#FBBF24'
    },
    {
      name: 'Tristeza',
      value: results.reduce((acc, r) => acc + r.emotions.sadness, 0) / results.length,
      color: '#3B82F6'
    },
    {
      name: 'Raiva',
      value: results.reduce((acc, r) => acc + r.emotions.anger, 0) / results.length,
      color: '#EF4444'
    },
    {
      name: 'Medo',
      value: results.reduce((acc, r) => acc + r.emotions.fear, 0) / results.length,
      color: '#8B5CF6'
    },
    {
      name: 'Surpresa',
      value: results.reduce((acc, r) => acc + r.emotions.surprise, 0) / results.length,
      color: '#10B981'
    }
  ] : [];

  // Time series data for trend analysis
  const timeSeriesData = results
    .sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime())
    .map((result, index) => ({
      index: index + 1,
      sentiment: result.sentiment === 'positive' ? 1 : result.sentiment === 'negative' ? -1 : 0,
      confidence: result.confidence * 100
    }));

  const sourceData = [
    {
      name: 'YouTube',
      value: results.filter(r => r.source === 'youtube').length,
      color: '#FF0000'
    },
    {
      name: 'Manual',
      value: results.filter(r => r.source === 'manual').length,
      color: '#8B5CF6'
    }
  ];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border rounded-lg shadow-lg" role="tooltip">
          <p className="font-medium">{`${payload[0].name}: ${payload[0].value}`}</p>
          {payload[0].payload.percentage && (
            <p className="text-sm text-gray-600">{`${payload[0].payload.percentage}% do total`}</p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-purple-600" aria-hidden="true" />
          Análise de Sentimentos
        </CardTitle>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-xs">
            <MessageSquare className="h-3 w-3 mr-1" aria-hidden="true" />
            {results.length} análises
          </Badge>
          {results.some(r => r.source === 'youtube') && (
            <Badge variant="outline" className="text-xs bg-red-50 text-red-700 border-red-200">
              <Youtube className="h-3 w-3 mr-1" aria-hidden="true" />
              YouTube
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Sentiment Distribution */}
          <div>
            <h4 className="font-medium mb-3">Distribuição de Sentimentos</h4>
            <div className="grid grid-cols-3 gap-2 mb-4 text-sm">
              {sentimentData.map((item, index) => (
                <div key={index} className="text-center p-2 rounded" style={{ backgroundColor: item.color + '20' }} role="group" aria-label={`${item.name}: ${item.value} comentários, ${item.percentage}%`}>
                  <div className="font-medium" style={{ color: item.color }}>
                    {item.value}
                  </div>
                  <div className="text-xs text-gray-600">{item.name}</div>
                  <div className="text-xs font-medium">{item.percentage}%</div>
                </div>
              ))}
            </div>
            <div role="img" aria-label="Gráfico de pizza mostrando distribuição de sentimentos">
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={sentimentData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {sentimentData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip content={<CustomTooltip />} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Emotion Distribution */}
          <div>
            <h4 className="font-medium mb-3">Emoções Médias</h4>
            <div role="img" aria-label="Gráfico de emoções médias detectadas">
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={emotionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" fontSize={12} />
                  <YAxis fontSize={12} />
                  <Tooltip formatter={(value) => [`${Number(value).toFixed(1)}%`, 'Intensidade']} />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Sentiment Trend */}
          {timeSeriesData.length > 5 && (
            <div>
              <h4 className="font-medium mb-3">Tendência de Sentimentos</h4>
              <div role="img" aria-label="Gráfico de linha mostrando tendência de sentimentos ao longo do tempo">
                <ResponsiveContainer width="100%" height={150}>
                  <LineChart data={timeSeriesData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="index" fontSize={12} />
                    <YAxis domain={[-1, 1]} fontSize={12} />
                    <Tooltip 
                      formatter={(value: number) => [
                        value === 1 ? 'Positivo' : value === -1 ? 'Negativo' : 'Neutro', 
                        'Sentimento'
                      ]} 
                    />
                    <Line 
                      type="monotone" 
                      dataKey="sentiment" 
                      stroke="#8884d8" 
                      strokeWidth={2}
                      dot={{ r: 3 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}