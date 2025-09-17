import React, { useState, useEffect } from 'react';
import { openApiAPI } from '../services/api';
import EndpointView from './EndpointView';

// Basic types for OpenAPI schema
interface OpenApiParameter {
  name: string;
  in: string;
  required: boolean;
  schema: {
    type: string;
    title: string;
  };
}

interface OpenApiRequestBody {
  content: {
    [contentType: string]: {
      schema: Record<string, unknown>;
    };
  };
}

interface OpenApiResponse {
  description: string;
  content?: {
    [contentType:string]: {
      schema: Record<string, unknown>;
    };
  };
}

interface OpenApiPath {
  [method: string]: {
    summary: string;
    description: string;
    parameters?: OpenApiParameter[];
    requestBody?: OpenApiRequestBody;
    responses: {
      [statusCode: string]: OpenApiResponse;
    };
  };
}

interface OpenApiSchema {
  paths: {
    [path: string]: OpenApiPath;
  };
}

const ApiExplorer: React.FC = () => {
  const [schema, setSchema] = useState<OpenApiSchema | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSchema = async () => {
      try {
        const response = await openApiAPI.getSchema();
        setSchema(response);
      } catch {
        setError('Failed to load API schema. Is the backend running?');
      } finally {
        setLoading(false);
      }
    };

    fetchSchema();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg text-center">
        {error}
      </div>
    );
  }

  if (!schema) {
    return (
      <div className="text-center py-12">
        <h3 className="text-2xl font-bold text-gray-900 mb-2">No API schema found</h3>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8">API Explorer</h1>
      <div className="space-y-8">
        {Object.entries(schema.paths).map(([path, pathDef]) => (
          <EndpointView key={path} path={path} pathDef={pathDef} />
        ))}
      </div>
    </div>
  );
};

export default ApiExplorer;
