'use client';

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { AlarmReportDto } from '../api/dtos/alarm-report';

export default function AlarmReport() {
  const [report, setReport] = useState<AlarmReportDto | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateReport = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/report-gen', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!res.ok) {
        const { message } = await res.json();
        throw new Error(message || 'Failed to generate report.');
      }

      const data: AlarmReportDto = await res.json();
      setReport(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 py-4">
      <div className="border-b pb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight lg:text-4xl">
          Your Alarm Usage Report
        </h1>

        <button
          onClick={generateReport}
          disabled={loading}
          className="rounded bg-primary px-4 py-2 font-semibold text-white hover:bg-primary/80 disabled:bg-gray-400"
        >
          {loading ? 'Generating Report...' : 'Generate Alarm Report'}
        </button>
      </div>

      {error && <p className="text-red-500">{error}</p>}

      {report && (
        <div className="prose prose-sm mt-2 space-y-8">
          <section>
            <ReactMarkdown>{report.overview}</ReactMarkdown>
          </section>

          <section>
            <h2 className="mb-2 border-b pb-2 text-3xl font-semibold tracking-tight">
              🔍 Frequent Patterns
            </h2>
            <ReactMarkdown>{report.frequentPatterns}</ReactMarkdown>
          </section>

          <section>
            <h2 className="mb-2 border-b pb-2 text-3xl font-semibold tracking-tight">
              ⏰ Wake Up Regularity
            </h2>
            <ReactMarkdown>{report.wakeUpRegularity}</ReactMarkdown>
          </section>

          <section>
            <h2 className="mb-2 border-b pb-2 text-3xl font-semibold tracking-tight">
              🔄 Retrigger Analysis
            </h2>
            <ReactMarkdown>{report.retriggerAnalysis}</ReactMarkdown>
          </section>

          <section>
            <h2 className="mb-4 border-b pb-2 text-3xl font-semibold tracking-tight">
              💡 Suggestions
            </h2>
            <div className="overflow-auto">
              <table className="w-full border-collapse border">
                <thead>
                  <tr className="bg-muted">
                    <th className="border px-4 py-2 text-left">#</th>
                    <th className="border px-4 py-2 text-left">Suggestion</th>
                  </tr>
                </thead>
                <tbody>
                  {report.suggestions.map((suggestion: string, idx) => (
                    <tr key={idx}>
                      <td className="border px-4 py-2 align-top font-semibold">
                        {idx + 1}
                      </td>
                      <td className="border px-4 py-2">
                        <ReactMarkdown>{suggestion}</ReactMarkdown>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
