// src/components/CSSFixGuide.jsx
import React, { useState } from 'react';
import { CheckCircle, AlertCircle, Copy, FileText, Settings } from 'lucide-react';

const CSSFixGuide = () => {
  const [activeTab, setActiveTab] = useState('diagnose');

  const installCommand = 'npm install -D @tailwindcss/vite tailwindcss postcss autoprefixer';
  const viteConfig = `// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    hmr: {
      overlay: false
    }
  }
})`;

  const postcssConfig = `// postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}`;

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <AlertCircle className="text-orange-500" />
        CSS Configuration Issues
      </h1>

      <div className="mb-6 border-b border-gray-200">
        <nav className="flex space-x-2">
          <button
            onClick={() => setActiveTab('diagnose')}
            className={`py-2 px-4 font-medium rounded-t-md ${activeTab === 'diagnose' ? 'bg-blue-100 text-blue-800 border-b-2 border-blue-500' : 'text-gray-600 hover:text-gray-800'}`}
          >
            Diagnosis
          </button>
          <button
            onClick={() => setActiveTab('solutions')}
            className={`py-2 px-4 font-medium rounded-t-md ${activeTab === 'solutions' ? 'bg-blue-100 text-blue-800 border-b-2 border-blue-500' : 'text-gray-600 hover:text-gray-800'}`}
          >
            Solutions
          </button>
          <button
            onClick={() => setActiveTab('config')}
            className={`py-2 px-4 font-medium rounded-t-md ${activeTab === 'config' ? 'bg-blue-100 text-blue-800 border-b-2 border-blue-500' : 'text-gray-600 hover:text-gray-800'}`}
          >
            Config Files
          </button>
        </nav>
      </div>

      {activeTab === 'diagnose' && (
        <div className="space-y-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h2 className="text-lg font-semibold text-blue-800 mb-2">Issue Detected</h2>
            <p className="text-blue-700">
              Your CSS file has the proper Tailwind directives, but PostCSS is reporting that 
              "@layer base" is used without a matching "@tailwind base" directive.
            </p>
          </div>

          <div className="bg-yellow-50 p-4 rounded-lg">
            <h2 className="text-lg font-semibold text-yellow-800 mb-2">Possible Causes</h2>
            <ul className="list-disc pl-5 space-y-2 text-yellow-700">
              <li>PostCSS is not processing your CSS file</li>
              <li>Tailwind CSS Vite plugin is not configured correctly</li>
              <li>Multiple CSS files with conflicting configurations</li>
              <li>Incorrect import order in your main JavaScript/TypeScript file</li>
            </ul>
          </div>
        </div>
      )}

      {activeTab === 'solutions' && (
        <div className="space-y-6">
          <div className="bg-green-50 p-4 rounded-lg">
            <h2 className="text-lg font-semibold text-green-800 mb-2">Step 1: Install Dependencies</h2>
            <div className="bg-black text-green-400 p-3 rounded font-mono text-sm mb-3 flex justify-between items-center">
              <code>{installCommand}</code>
              <button 
                onClick={() => copyToClipboard(installCommand)}
                className="text-white bg-gray-700 p-1 rounded hover:bg-gray-600"
              >
                <Copy size={14} />
              </button>
            </div>
            <p className="text-green-700 text-sm">
              Make sure you have the latest Tailwind CSS Vite plugin installed.
            </p>
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h2 className="text-lg font-semibold text-green-800 mb-2">Step 2: Check CSS Import Order</h2>
            <p className="text-green-700 mb-2">
              Ensure your main CSS file is imported in your main JavaScript/TypeScript file:
            </p>
            <div className="bg-black text-green-400 p-3 rounded font-mono text-sm">
              <code>import './index.css'</code>
            </div>
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h2 className="text-lg font-semibold text-green-800 mb-2">Step 3: Verify CSS File Structure</h2>
            <p className="text-green-700">
              Your CSS file should have the Tailwind directives at the very top:
            </p>
            <div className="bg-black text-green-400 p-3 rounded font-mono text-sm mt-2">
              <code>@tailwind base;</code><br />
              <code>@tailwind components;</code><br />
              <code>@tailwind utilities;</code><br />
              <code>@layer base &#123; ... &#125;</code>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'config' && (
        <div className="space-y-6">
          <div>
            <h2 className="text-lg font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <Settings size={18} />
              Vite Configuration
            </h2>
            <div className="bg-gray-100 p-4 rounded-lg relative">
              <button 
                onClick={() => copyToClipboard(viteConfig)}
                className="absolute top-2 right-2 text-gray-700 bg-white p-1 rounded hover:bg-gray-200"
              >
                <Copy size={14} />
              </button>
              <pre className="text-sm overflow-x-auto">{viteConfig}</pre>
            </div>
          </div>

          <div>
            <h2 className="text-lg font-semibold text-gray-800 mb-2 flex items-center gap-2">
              <FileText size={18} />
              PostCSS Configuration
            </h2>
            <div className="bg-gray-100 p-4 rounded-lg relative">
              <button 
                onClick={() => copyToClipboard(postcssConfig)}
                className="absolute top-2 right-2 text-gray-700 bg-white p-1 rounded hover:bg-gray-200"
              >
                <Copy size={14} />
              </button>
              <pre className="text-sm overflow-x-auto">{postcssConfig}</pre>
            </div>
          </div>
        </div>
      )}

      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Additional Checks</h3>
        <ul className="list-disc pl-5 space-y-1 text-gray-700">
          <li>Ensure you don't have multiple Tailwind CSS installations</li>
          <li>Check that your CSS file is not being imported multiple times</li>
          <li>Verify that your tailwind.config.js file exists and is properly configured</li>
          <li>Restart your Vite dev server after making configuration changes</li>
        </ul>
      </div>
    </div>
  );
};

export default CSSFixGuide;