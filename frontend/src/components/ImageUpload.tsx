import React, { useState, useCallback, useRef, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Upload,
  Camera,
  X,
  Image as ImageIcon,
  Leaf,
  AlertCircle,
} from 'lucide-react';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  onClear: () => void;
  selectedImage: string | null;
  isProcessing: boolean;
}

const ImageUpload: React.FC<ImageUploadProps> = ({
  onImageSelect,
  onClear,
  selectedImage,
  isProcessing,
}) => {
  const [error, setError] = useState<string | null>(null);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setError(null);
      const file = acceptedFiles[0];
      if (!file) return;

      if (!file.type.startsWith('image/')) {
        setError('Please upload a valid image file');
        return;
      }

      if (file.size > 16 * 1024 * 1024) {
        setError('Image size must be less than 16MB');
        return;
      }

      onImageSelect(file);
    },
    [onImageSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'],
    },
    maxFiles: 1,
    disabled: isProcessing,
  });

  const openCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' },
      });

      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      setIsCameraOpen(true);
    } catch {
      setError('Could not access camera. Please check permissions.');
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext('2d');

      if (ctx) {
        ctx.drawImage(video, 0, 0);

        canvas.toBlob(
          (blob) => {
            if (blob) {
              const file = new File([blob], 'capture.jpg', {
                type: 'image/jpeg',
              });
              onImageSelect(file);
            }
          },
          'image/jpeg',
          0.9
        );
      }

      closeCamera();
    }
  };

  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsCameraOpen(false);
  };

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div className="w-full">

      {/* CAMERA MODE */}
      {isCameraOpen ? (
        <div className="relative">

          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="w-full rounded-xl bg-black"
          />

          <canvas ref={canvasRef} className="hidden" />

          <div className="absolute bottom-4 left-0 right-0 flex justify-center gap-4">

            <button
              type="button"
              aria-label="Close camera"
              onClick={closeCamera}
              className="p-4 bg-red-500 hover:bg-red-600 rounded-full text-white transition-all"
            >
              <X size={24} />
            </button>

            <button
              type="button"
              aria-label="Capture photo"
              onClick={capturePhoto}
              className="p-4 bg-white hover:bg-gray-100 rounded-full text-gray-800 transition-all"
            >
              <Camera size={24} />
            </button>

          </div>
        </div>
      ) : selectedImage ? (

        /* IMAGE PREVIEW */
        <div className="relative group">

          <div className="card p-2">
            <img
              src={selectedImage}
              alt="Selected plant leaf for disease detection"
              className="w-full h-64 md:h-80 object-contain rounded-lg bg-gray-50 dark:bg-gray-900"
            />
          </div>

          {!isProcessing && (
            <button
              type="button"
              aria-label="Remove selected image"
              onClick={onClear}
              className="absolute top-4 right-4 p-2 bg-red-500 hover:bg-red-600 rounded-full text-white transition-all shadow-lg"
            >
              <X size={20} />
            </button>
          )}

          {isProcessing && (
            <div className="absolute inset-0 bg-black/50 rounded-xl flex items-center justify-center">
              <div className="text-center text-white">
                <div className="spinner w-12 h-12 mx-auto mb-4"></div>
                <p className="text-lg font-medium">Analyzing leaf...</p>
                <p className="text-sm opacity-80">This may take a moment</p>
              </div>
            </div>
          )}

        </div>
      ) : (

        /* UPLOAD AREA */
        <div
          {...getRootProps()}
          className={`
            relative border-2 border-dashed rounded-xl p-8 md:p-12 text-center cursor-pointer
            transition-all duration-300
            ${isDragActive
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 scale-[1.02]'
              : 'border-gray-300 dark:border-gray-600 hover:border-primary-400 hover:bg-gray-50 dark:hover:bg-gray-800/50'
            }
            ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />

          <div className="flex flex-col items-center gap-4">

            <div
              className={`
                p-4 rounded-full transition-all duration-300
                ${isDragActive
                  ? 'bg-primary-500 text-white'
                  : 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400'
                }
              `}
            >
              {isDragActive ? <Leaf size={32} /> : <Upload size={32} />}
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-200">
                {isDragActive ? 'Drop your image here' : 'Upload a leaf image'}
              </h3>

              <p className="text-gray-500 dark:text-gray-400 mt-1">
                Drag & drop or click to select
              </p>
            </div>

            <div className="flex items-center gap-2 text-sm text-gray-400">
              <ImageIcon size={16} />
              <span>PNG, JPG, WEBP up to 16MB</span>
            </div>

          </div>

          {/* CAMERA BUTTON */}

          <button
            type="button"
            aria-label="Open camera to capture leaf image"
            onClick={(e) => {
              e.stopPropagation();
              openCamera();
            }}
            disabled={isProcessing}
            className="mt-6 flex items-center gap-2 mx-auto px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg text-gray-700 dark:text-gray-200 transition-all"
          >
            <Camera size={18} />
            <span>Take Photo</span>
          </button>

        </div>
      )}

      {/* ERROR MESSAGE */}

      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center gap-3 text-red-700 dark:text-red-400">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

    </div>
  );
};

export default ImageUpload;