import React from 'react';
import { 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  Leaf, 
  Shield, 
  Stethoscope,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { Prediction, TreatmentInfo, formatDiseaseName, getConfidenceColor, getConfidenceTextColor } from '../api/api';
import ConfidenceChart from './ConfidenceChart';

interface PredictionResultsProps {
  primaryPrediction: Prediction;
  allPredictions: Prediction[];
  treatment: TreatmentInfo;
}

const PredictionResults: React.FC<PredictionResultsProps> = ({
  primaryPrediction,
  allPredictions,
  treatment,
}) => {
  const [showAllPredictions, setShowAllPredictions] = React.useState(false);
  const [expandedSections, setExpandedSections] = React.useState({
    description: true,
    treatment: true,
    prevention: true,
    predictions: false,
  });

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  const isHealthy = primaryPrediction.disease.toLowerCase().includes('healthy');
  const confidencePercent = Math.round(primaryPrediction.confidence * 100);

  return (
    <div className="space-y-6 fade-in">
      {/* Primary Result */}
      <div className="card p-6 card-hover">
        <div className="flex items-start gap-4">
          <div className={`
            p-3 rounded-full
            ${isHealthy ? 'bg-green-100 dark:bg-green-900/30' : 'bg-orange-100 dark:bg-orange-900/30'}
          `}>
            {isHealthy ? (
              <CheckCircle size={28} className="text-green-600 dark:text-green-400" />
            ) : (
              <AlertTriangle size={28} className="text-orange-600 dark:text-orange-400" />
            )}
          </div>
          
          <div className="flex-1">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              {formatDiseaseName(primaryPrediction.disease)}
            </h2>
            
            <div className="mt-2 flex items-center gap-3">
              <div className="flex-1">
                <div className="confidence-bar">
                  <div
                    className={`confidence-fill ${getConfidenceColor(primaryPrediction.confidence)}`}
                    style={{ width: `${confidencePercent}%` }}
                  />
                </div>
              </div>
              <span className={`font-bold text-lg ${getConfidenceTextColor(primaryPrediction.confidence)}`}>
                {confidencePercent}%
              </span>
            </div>
            
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Confidence in prediction
            </p>
          </div>
        </div>
      </div>

      {/* Description */}
      <div className="card overflow-hidden">
        <button
          onClick={() => toggleSection('description')}
          className="w-full px-6 py-4 flex items-center justify-between bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <div className="flex items-center gap-3">
            <Info size={20} className="text-primary-500" />
            <span className="font-semibold text-gray-900 dark:text-white">About This Condition</span>
          </div>
          {expandedSections.description ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        {expandedSections.description && (
          <div className="px-6 py-4">
            <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
              {treatment.description}
            </p>
          </div>
        )}
      </div>

      {/* Treatment */}
      {!isHealthy && (
        <div className="card overflow-hidden">
          <button
            onClick={() => toggleSection('treatment')}
            className="w-full px-6 py-4 flex items-center justify-between bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <div className="flex items-center gap-3">
              <Stethoscope size={20} className="text-red-500" />
              <span className="font-semibold text-gray-900 dark:text-white">Treatment Recommendations</span>
            </div>
            {expandedSections.treatment ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
          </button>
          {expandedSections.treatment && (
            <div className="px-6 py-4">
              <ul className="space-y-3">
                {treatment.treatment.map((item, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 flex items-center justify-center text-sm font-medium">
                      {index + 1}
                    </span>
                    <span className="text-gray-600 dark:text-gray-300">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Prevention */}
      <div className="card overflow-hidden">
        <button
          onClick={() => toggleSection('prevention')}
          className="w-full px-6 py-4 flex items-center justify-between bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <div className="flex items-center gap-3">
            <Shield size={20} className="text-blue-500" />
            <span className="font-semibold text-gray-900 dark:text-white">Prevention Tips</span>
          </div>
          {expandedSections.prevention ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        {expandedSections.prevention && (
          <div className="px-6 py-4">
            <ul className="space-y-3">
              {treatment.prevention.map((item, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-sm font-medium">
                    {index + 1}
                  </span>
                  <span className="text-gray-600 dark:text-gray-300">{item}</span>
                  </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* All Predictions Chart */}
      <div className="card overflow-hidden">
        <button
          onClick={() => toggleSection('predictions')}
          className="w-full px-6 py-4 flex items-center justify-between bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <div className="flex items-center gap-3">
            <Leaf size={20} className="text-primary-500" />
            <span className="font-semibold text-gray-900 dark:text-white">Top 5 Predictions</span>
          </div>
          {expandedSections.predictions ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        {expandedSections.predictions && (
          <div className="px-6 py-4">
            <ConfidenceChart predictions={allPredictions} />
          </div>
        )}
      </div>

      {/* Alternative Predictions List */}
      <div className="card p-6">
        <h3 className="font-semibold text-gray-900 dark:text-white mb-4">All Predictions</h3>
        <div className="space-y-3">
          {allPredictions.map((prediction, index) => (
            <div
              key={index}
              className={`
                flex items-center justify-between p-3 rounded-lg
                ${index === 0 
                  ? 'bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800' 
                  : 'bg-gray-50 dark:bg-gray-800/50'
                }
              `}
            >
              <div className="flex items-center gap-3">
                <span className={`
                  w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold
                  ${index === 0 
                    ? 'bg-primary-500 text-white' 
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                  }
                `}>
                  {index + 1}
                </span>
                <span className={`text-sm ${index === 0 ? 'font-medium text-gray-900 dark:text-white' : 'text-gray-600 dark:text-gray-300'}`}>
                  {formatDiseaseName(prediction.disease)}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${getConfidenceColor(prediction.confidence)}`}
                    style={{ width: `${Math.round(prediction.confidence * 100)}%` }}
                  />
                </div>
                <span className="text-sm font-medium text-gray-600 dark:text-gray-300 w-12 text-right">
                  {Math.round(prediction.confidence * 100)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PredictionResults;