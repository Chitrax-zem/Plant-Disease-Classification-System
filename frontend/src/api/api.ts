/**
 * API service for Plant Disease Classification System
 */

const API_BASE_URL = "https://plant-disease-classification-system-81dx.onrender.com";

// Types
export interface Prediction {
  disease: string;
  confidence: number;
  confidence_percentage: string;
}

export interface TreatmentInfo {
  description: string;
  treatment: string[];
  prevention: string[];
}

export interface PredictionResponse {
  success: boolean;
  primary_prediction: Prediction;
  all_predictions: Prediction[];
  treatment: TreatmentInfo;
  image_info?: {
    filename: string;
    original_filename: string;
  };
}

export interface HealthResponse {
  status: string;
  service: string;
  timestamp: string;
  version: string;
}

export interface ClassesResponse {
  success: boolean;
  count: number;
  classes: string[];
}

export interface ModelInfoResponse {
  success: boolean;
  model_type: string;
  input_shape: number[];
  num_classes: number;
  classes: string[];
  model_loaded: boolean;
  total_params?: number;
  output_shape?: number[];
}

/**
 * Check API health
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('Health check failed');
  }
  return response.json();
}

/**
 * Get all disease classes
 */
export async function getClasses(): Promise<ClassesResponse> {
  const response = await fetch(`${API_BASE_URL}/classes`);
  if (!response.ok) {
    throw new Error('Failed to fetch classes');
  }
  return response.json();
}

/**
 * Get disease information
 */
export async function getDiseaseInfo(diseaseName: string): Promise<{ success: boolean; disease: string; info: TreatmentInfo }> {
  const response = await fetch(`${API_BASE_URL}/disease/${encodeURIComponent(diseaseName)}`);
  if (!response.ok) {
    throw new Error('Failed to fetch disease info');
  }
  return response.json();
}

/**
 * Predict disease from image file
 */
export async function predictFromImage(file: File): Promise<PredictionResponse> {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Prediction failed');
  }

  return response.json();
}

/**
 * Predict disease from base64 encoded image
 */
export async function predictFromBase64(base64Image: string): Promise<PredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/predict/base64`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: base64Image }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Prediction failed');
  }

  return response.json();
}

/**
 * Get model information
 */
export async function getModelInfo(): Promise<ModelInfoResponse> {
  const response = await fetch(`${API_BASE_URL}/model/info`);
  if (!response.ok) {
    throw new Error('Failed to fetch model info');
  }
  return response.json();
}

/**
 * Convert File to base64 string
 */
export function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });
}

/**
 * Format disease name for display
 */
export function formatDiseaseName(disease: string): string {
  return disease
    .replace(/___/g, ' - ')
    .replace(/_/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Get confidence color class
 */
export function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.8) return 'bg-green-500';
  if (confidence >= 0.6) return 'bg-yellow-500';
  if (confidence >= 0.4) return 'bg-orange-500';
  return 'bg-red-500';
}

/**
 * Get confidence text color class
 */
export function getConfidenceTextColor(confidence: number): string {
  if (confidence >= 0.8) return 'text-green-600 dark:text-green-400';
  if (confidence >= 0.6) return 'text-yellow-600 dark:text-yellow-400';
  if (confidence >= 0.4) return 'text-orange-600 dark:text-orange-400';
  return 'text-red-600 dark:text-red-400';
}