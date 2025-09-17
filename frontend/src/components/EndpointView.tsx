import React, { useState } from 'react';
import { openApiAPI } from '../services/api';

const EndpointView = ({ path, pathDef }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({});
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (paramName, value) => {
    setFormData((prev) => ({ ...prev, [paramName]: value }));
  };

  const handleTryItOut = async (method) => {
    setLoading(true);
    const params = {};
    const pathParams = {};
    let body = null;

    pathDef[method].parameters?.forEach((param) => {
      if (param.in === 'query') {
        params[param.name] = formData[param.name];
      } else if (param.in === 'path') {
        pathParams[param.name] = formData[param.name];
      }
    });

    if (pathDef[method].requestBody) {
      body = JSON.parse(formData['requestBody']);
    }

    let finalPath = path;
    Object.entries(pathParams).forEach(([key, value]) => {
      finalPath = finalPath.replace(`{${key}}`, value);
    });

    const result = await openApiAPI.makeRequest(method, finalPath, params, body);
    setResponse(result);
    setLoading(false);
  };

  const getMethodColor = (method) => {
    switch (method.toUpperCase()) {
      case 'GET':
        return 'bg-blue-500';
      case 'POST':
        return 'bg-green-500';
      case 'PUT':
        return 'bg-yellow-500';
      case 'DELETE':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="border border-white/20 rounded-lg overflow-hidden">
      {Object.entries(pathDef).map(([method, def]) => (
        <div key={method}>
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="w-full flex items-center justify-between p-4 bg-white/5 hover:bg-white/10 transition-colors"
          >
            <div className="flex items-center space-x-4 space-x-reverse">
              <span
                className={`w-20 text-center font-bold text-white py-1 rounded ${getMethodColor(
                  method
                )}`}
              >
                {method.toUpperCase()}
              </span>
              <span className="font-mono text-lg text-white">{path}</span>
            </div>
            <span className="text-white/80">{def.summary}</span>
          </button>
          {isOpen && (
            <div className="p-4 bg-black/20">
              <p className="text-white/80 mb-4">{def.description}</p>

              <div className="space-y-4">
                {def.parameters && (
                  <div>
                    <h4 className="text-lg font-bold text-white mb-2">Parameters</h4>
                    {def.parameters.map((param) => (
                      <div key={param.name} className="flex items-center space-x-4 space-x-reverse mb-2">
                        <span className="text-white/80 w-32">{param.name}</span>
                        <input
                          type={param.schema.type === 'integer' ? 'number' : 'text'}
                          placeholder={param.schema.title}
                          className="input-field flex-1"
                          onChange={(e) => handleInputChange(param.name, e.target.value)}
                        />
                      </div>
                    ))}
                  </div>
                )}

                {def.requestBody && (
                  <div>
                    <h4 className="text-lg font-bold text-white mb-2">Request Body</h4>
                    <textarea
                      placeholder="Enter JSON body"
                      className="input-field w-full h-32 resize-none"
                      onChange={(e) => handleInputChange('requestBody', e.target.value)}
                    />
                  </div>
                )}

                <button
                  className="btn-primary"
                  onClick={() => handleTryItOut(method)}
                  disabled={loading}
                >
                  {loading ? 'Loading...' : 'Try it out'}
                </button>

                {response && (
                  <div className="mt-4">
                    <h4 className="text-lg font-bold text-white mb-2">Response</h4>
                    <pre className="bg-black/50 text-white p-4 rounded-lg">
                      {JSON.stringify(response, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default EndpointView;
