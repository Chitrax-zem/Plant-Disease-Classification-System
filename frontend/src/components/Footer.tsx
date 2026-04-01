import { Leaf, Heart, Github, Twitter } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-50 dark:bg-gray-800/50 border-t border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Leaf size={20} className="text-primary-500" />
              <span className="font-bold text-gray-900 dark:text-white">
                Plant Disease Classifier
              </span>
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              AI-powered plant disease detection using deep learning and EfficientNetB0 transfer learning.
            </p>
          </div>

          {/* Technology */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Technology</h3>
            <ul className="space-y-2 text-sm text-gray-500 dark:text-gray-400">
              <li>TensorFlow / Keras</li>
              <li>EfficientNetB0</li>
              <li>React + TypeScript</li>
              <li>Flask API</li>
            </ul>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="text-gray-500 dark:text-gray-400 hover:text-primary-500 transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-500 dark:text-gray-400 hover:text-primary-500 transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-500 dark:text-gray-400 hover:text-primary-500 transition-colors">
                  Model Training
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
            Made with <Heart size={14} className="text-red-500" /> by Chitrax-zem
          </p>
          <div className="flex items-center gap-4">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            >
              <Github size={20} />
            </a>
            <a
              href="https://twitter.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-blue-500 transition-colors"
            >
              <Twitter size={20} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;