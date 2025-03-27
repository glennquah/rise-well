'use client';

import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { toast } from 'sonner';
import { AlarmReportDto } from '../api/dtos/alarm-report';

export default function AlarmReport() {
  const [report, setReport] = useState<AlarmReportDto | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchReport = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/alarm-report', {
        method: 'GET',
        credentials: 'include',
      });

      if (!res.ok) {
        const { message } = await res.json();
        throw new Error(message || 'No saved report found.');
      }

      const data: AlarmReportDto = await res.json();
      setReport(data);
    } catch (err) {
      console.error(err);

      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  const generateReport = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/alarm-report-gen', {
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
      toast.success('Report Generated successfully!');
    } catch (err) {
      console.error(err);

      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  const saveReport = async () => {
    if (!report) return;

    setSaving(true);
    try {
      const res = await fetch('/api/alarm-report', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(report),
      });

      if (!res.ok) {
        const { message } = await res.json();
        throw new Error(message || 'Failed to save report.');
      }

      toast.success('Report saved successfully!');
    } catch (err) {
      console.error(err);
      if (err instanceof Error) {
        toast.error(err.message);
      } else {
        toast.error('An unknown error occurred');
      }
    } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, []);

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
          {loading ? 'Generating...' : 'Generate Alarm Report'}
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
                  {report.suggestions.map((suggestion, idx) => (
                    <tr key={idx}>
                      <td className="border px-4 py-2 align-top font-semibold">
                        {idx + 1}
                      </td>
                      <td className="border px-4 py-2">
                        <ReactMarkdown
                          components={{
                            a: ({ ...props }) => (
                              <a
                                {...props}
                                className="text-blue-500 underline font-bold"
                                target="_blank"
                                rel="noopener noreferrer"
                              />
                            ),
                          }}
                        >
                          {suggestion}
                        </ReactMarkdown>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <button
            onClick={saveReport}
            disabled={saving}
            className="rounded bg-primary px-4 py-2 font-semibold text-white hover:bg-green-600 disabled:bg-gray-400"
          >
            {saving ? 'Saving...' : 'Save Report'}
          </button>
        </div>
      )}
    </div>
  );
}
