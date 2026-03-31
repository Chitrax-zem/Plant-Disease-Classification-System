import React from 'react';
import { Clock, Leaf, Trash2 } from 'lucide-react';
import { formatDiseaseName, Prediction } from '../api/api';

interface HistoryItem {
  id: string;
  timestamp: Date;
  imageName: string;
  prediction: Prediction;
  imageData: string;
}

interface PredictionHistoryProps {
  history: HistoryItem[];
  onClear: () => void;
  onSelect: (item: HistoryItem) => void;
}

const PredictionHistory: React.FC<PredictionHistoryProps> = ({
  history,
  onClear,
  onSelect,
}) => {
  if (history.length === 0) {
    return null;
  }

  return (
    <div className="card p-6 fade-in">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Clock size={20} className="text-primary-500" />
          <h3 className="font-semibold text-gray-900 dark:text-white">Recent Predictions</h3>
        </div>
        <button
          onClick={onClear}
          className="flex items-center gap-1 text-sm text-red-500 hover:text-red-600 transition-colors"
        >
          <Trash2 size={16} />
          <span>Clear</span>
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {history.slice(0, 8).map((item) => (
          <button
            key={item.id}
            onClick={() => onSelect(item)}
            className="group relative rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-800 aspect-square hover:ring-2 hover:ring-primary-500 transition-all"
          >
            <img
              src={item.imageData}
              alt={item.imageName}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="absolute bottom-0 left-0 right-0 p-2 text-left">
                <p className="text-white text-xs font-medium truncate">
                  {formatDiseaseName(item.prediction.disease)}
                </p>
                <p className="text-white/70 text-xs">
                  {Math.round(item.prediction.confidence * 100)}% confidence
                </p>
              </div>
            </div>
            <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <div className="p-1.5 bg-white/90 dark:bg-gray-800/90 rounded-full">
                <Leaf size={14} className="text-primary-500" />
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default PredictionHistory;