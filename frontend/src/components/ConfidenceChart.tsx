import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { formatDiseaseName, getConfidenceColor, Prediction } from '../api/api';

interface ConfidenceChartProps {
  predictions: Prediction[];
}

const ConfidenceChart: React.FC<ConfidenceChartProps> = ({ predictions }) => {
  const data = predictions.map((p) => ({
    name: formatDiseaseName(p.disease).split(' - ')[1] || formatDiseaseName(p.disease),
    fullName: formatDiseaseName(p.disease),
    confidence: Math.round(p.confidence * 100),
    fill: getConfidenceColor(p.confidence),
  }));

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
          <XAxis
            type="number"
            domain={[0, 100]}
            tickFormatter={(value) => `${value}%`}
            className="text-xs"
            tick={{ fill: 'currentColor' }}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={120}
            tick={{ fill: 'currentColor', fontSize: 11 }}
            className="text-xs"
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload;
                return (
                  <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
                    <p className="font-medium text-gray-900 dark:text-white text-sm">
                      {item.fullName}
                    </p>
                    <p className="text-primary-600 dark:text-primary-400 font-bold">
                      {item.confidence}%
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="confidence" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.fill} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ConfidenceChart;