import { useState, useEffect, useCallback } from 'react';
import { Leaf, AlertCircle, RefreshCw, Info } from 'lucide-react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ImageUpload from './components/ImageUpload';
import PredictionResults from './components/PredictionResults';
import PredictionHistory from './components/PredictionHistory';
import {
  predictFromImage,
  fileToBase64,
  PredictionResponse,
  checkHealth,
  Prediction,
} from './api/api';

// Types
interface HistoryItem {
  id: string;
  timestamp: Date;
  imageName: string;
  prediction: Prediction;
  imageData: string;
}

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('darkMode');
      if (saved !== null) {
        return JSON.parse(saved);
      }
      return window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });

  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [predictionResult, setPredictionResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [history, setHistory] = useState<HistoryItem[]>(() => {
    const saved = localStorage.getItem('predictionHistory');
    if (saved) {
      try {
        return JSON.parse(saved).map((item: HistoryItem) => ({
          ...item,
          timestamp: new Date(item.timestamp),
        }));
      } catch {
        return [];
      }
    }
    return [];
  });

  // Apply dark mode
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  // Save history to localStorage
  useEffect(() => {
    localStorage.setItem('predictionHistory', JSON.stringify(history.slice(0, 20)));
  }, [history]);

  // Check API health on mount
  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        await checkHealth();
        setApiStatus('online');
      } catch {
        setApiStatus('offline');
      }
    };
    checkApiHealth();
  }, []);

  const toggleDarkMode = () => setDarkMode(!darkMode);

  const handleImageSelect = useCallback(async (file: File) => {
    setError(null);
    setPredictionResult(null);
    setSelectedFile(file);

    try {
      const base64 = await fileToBase64(file);
      setSelectedImage(base64);
    } catch {
      setError('Failed to read image file');
    }
  }, []);

  const handleClear = useCallback(() => {
    setSelectedImage(null);
    setSelectedFile(null);
    setPredictionResult(null);
    setError(null);
  }, []);

  const handlePredict = useCallback(async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setError(null);

    try {
      const result = await predictFromImage(selectedFile);
      setPredictionResult(result);

      // Add to history
      if (selectedImage) {
        const historyItem: HistoryItem = {
          id: Date.now().toString(),
          timestamp: new Date(),
          imageName: selectedFile.name,
          prediction: result.primary_prediction,
          imageData: selectedImage,
        };
        setHistory((prev) => [historyItem, ...prev.slice(0, 19)]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Prediction failed');
    } finally {
      setIsProcessing(false);
    }
  }, [selectedFile, selectedImage]);

  const handleHistorySelect = useCallback((item: HistoryItem) => {
    setSelectedImage(item.imageData);
    setPredictionResult({
      success: true,
      primary_prediction: item.prediction,
      all_predictions: [item.prediction],
      treatment: {
        description: 'View full details by analyzing the image again.',
        treatment: [],
        prevention: [],
      },
    });
    setSelectedFile(null);
  }, []);

  const handleHistoryClear = useCallback(() => {
    setHistory([]);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      <Navbar darkMode={darkMode} toggleDarkMode={toggleDarkMode} />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {/* API Status Banner */}
        {apiStatus === 'offline' && (
          <div className="mb-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg flex items-center gap-3">
            <AlertCircle size={20} className="text-yellow-600 dark:text-yellow-400" />
            <div>
              <p className="font-medium text-yellow-800 dark:text-yellow-200">
                API Server Offline
              </p>
              <p className="text-sm text-yellow-600 dark:text-yellow-400">
                The backend server is not running. Start it with <code className="px-1 py-0.5 bg-yellow-100 dark:bg-yellow-800 rounded">python backend/app.py</code>
              </p>
            </div>
          </div>
        )}

        {/* Header Section */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 dark:bg-primary-900/30 rounded-full text-primary-700 dark:text-primary-300 text-sm font-medium mb-4">
            <Leaf size={16} />
            <span>AI-Powered Disease Detection</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-3">
            Plant Disease Classification
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Upload a leaf image to identify plant diseases and get treatment recommendations.
            Our AI model can classify 38 different plant disease categories.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="card p-4 text-center">
            <p className="text-2xl font-bold text-primary-500">38</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Disease Classes</p>
          </div>
          <div className="card p-4 text-center">
            <p className="text-2xl font-bold text-primary-500">95%+</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Accuracy</p>
          </div>
          <div className="card p-4 text-center">
            <p className="text-2xl font-bold text-primary-500">&lt;2s</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Prediction Time</p>
          </div>
          <div className="card p-4 text-center">
            <p className="text-2xl font-bold text-primary-500">14</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Plant Types</p>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div>
            <div className="card p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                <Info size={20} className="text-primary-500" />
                Upload Leaf Image
              </h2>
              
              <ImageUpload
                onImageSelect={handleImageSelect}
                onClear={handleClear}
                selectedImage={selectedImage}
                isProcessing={isProcessing}
              />

              {/* Predict Button */}
              {selectedImage && !predictionResult && (
                <button
                  onClick={handlePredict}
                  disabled={isProcessing || apiStatus === 'offline'}
                  className={`
                    w-full mt-6 py-4 rounded-lg font-semibold text-white
                    flex items-center justify-center gap-2
                    transition-all duration-300
                    ${isProcessing || apiStatus === 'offline'
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-primary-500 hover:bg-primary-600 active:scale-[0.98]'
                    }
                  `}
                >
                  {isProcessing ? (
                    <>
                      <RefreshCw size={20} className="animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Leaf size={20} />
                      Analyze Plant
                    </>
                  )}
                </button>
              )}

              {/* New Prediction Button */}
              {predictionResult && (
                <button
                  onClick={handleClear}
                  className="w-full mt-6 py-4 rounded-lg font-semibold bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 flex items-center justify-center gap-2 transition-all"
                >
                  <RefreshCw size={20} />
                  New Prediction
                </button>
              )}
            </div>

            {/* Prediction History */}
            {history.length > 0 && !predictionResult && (
              <div className="mt-6">
                <PredictionHistory
                  history={history}
                  onClear={handleHistoryClear}
                  onSelect={handleHistorySelect}
                />
              </div>
            )}
          </div>

          {/* Results Section */}
          <div>
            {predictionResult ? (
              <PredictionResults
                primaryPrediction={predictionResult.primary_prediction}
                allPredictions={predictionResult.all_predictions}
                treatment={predictionResult.treatment}
              />
            ) : (
              <div className="card p-8 text-center">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
                  <Leaf size={32} className="text-gray-400 dark:text-gray-500" />
                </div>
                <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">
                  No Results Yet
                </h3>
                <p className="text-gray-500 dark:text-gray-400">
                  Upload an image and click "Analyze Plant" to see predictions
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="fixed bottom-4 right-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg shadow-lg flex items-center gap-3 max-w-md">
            <AlertCircle size={20} className="text-red-500 flex-shrink-0" />
            <p className="text-red-700 dark:text-red-300 text-sm">{error}</p>
            <button
              onClick={() => setError(null)}
              className="text-red-500 hover:text-red-600"
            >
              ×
            </button>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;