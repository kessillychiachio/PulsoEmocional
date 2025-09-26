import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { TrendingUp, Youtube, MessageSquare } from 'lucide-react';

interface Comentario {
  texto: string;
  polaridade: 'POSITIVO' | 'NEGATIVO' | 'NEUTRO' | 'DESCONHECIDO' | 'erro';
  emocao: string;
}

interface SentimentChartProps {
  comments: Comentario[];
}

export function SentimentChart({ comments }: SentimentChartProps) {
  if (!comments || comments.length === 0) {
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
      value: comments.filter(c => c.polaridade === 'POSITIVO').length,
      color: '#10B981',
    },
    {
      name: 'Negativo',
      value: comments.filter(c => c.polaridade === 'NEGATIVO').length,
      color: '#EF4444',
    },
    {
      name: 'Neutro',
      value: comments.filter(c => c.polaridade === 'NEUTRO' || c.polaridade === 'DESCONHECIDO').length,
      color: '#F59E0B',
    }
  ];

  const validEmotions = comments.filter(c => c.emocao && c.emocao !== 'indefinida');
  const emotionCounts: { [key: string]: number } = validEmotions.reduce((acc, c) => {
    acc[c.emocao] = (acc[c.emocao] || 0) + 1;
    return acc;
  }, {} as { [key: string]: number });
  
  const emotionData = Object.keys(emotionCounts).map(emocao => ({
    name: emocao.charAt(0).toUpperCase() + emocao.slice(1),
    value: emotionCounts[emocao],
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const total = payload.reduce((sum: number, entry: any) => sum + entry.value, 0);
      const percentage = total > 0 ? ((payload[0].value / total) * 100).toFixed(1) : 0;

      return (
        <div className="bg-white p-3 border rounded-lg shadow-lg" role="tooltip">
          <p className="font-medium" style={{ color: payload[0].color }}>{`${payload[0].name}: ${payload[0].value}`}</p>
          <p className="text-sm text-gray-600">{`${percentage}% do total`}</p>
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
            {comments.length} comentários
          </Badge>
          {comments.length > 0 && (
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
                <div 
                  key={index} 
                  className="text-center p-2 rounded" 
                  style={{ backgroundColor: item.color + '20' }} 
                  role="group" 
                  aria-label={`${item.name}: ${item.value} comentários`}
                >
                  <div className="font-medium" style={{ color: item.color }}>
                    {item.value}
                  </div>
                  <div className="text-xs text-gray-600">{item.name}</div>
                  <div className="text-xs font-medium">{((item.value / comments.length) * 100).toFixed(1)}%</div>
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
          {emotionData.length > 0 && (
            <div>
              <h4 className="font-medium mb-3">Contagem de Emoções</h4>
              <div role="img" aria-label="Gráfico de barras mostrando a contagem de emoções detectadas">
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={emotionData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" fontSize={12} />
                    <YAxis fontSize={12} />
                    <Tooltip />
                    <Bar dataKey="value" fill="#8B5CF6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}