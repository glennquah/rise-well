'use client';
import { Button } from '@/components/ui/button';
import { FileText } from 'lucide-react';
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
    <div className="space-y-4 py-4">
      <div className="glass-panel rounded-2xl p-6 soft-shadow">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
          <div>
            <h2 className="text-xl font-semibold text-foreground">
              Alarm Analytics Report
            </h2>
            <p className="text-foreground/60 mt-1">
              Generate comprehensive insights from your alarm data.
            </p>
          </div>
          <Button
            onClick={generateReport}
            className="bg-black hover:bg-blue-600 text-white flex items-center gap-2"
            disabled={loading}
          >
            <FileText className="h-4 w-4" />
            <span>{loading ? 'Generating...' : 'AI Generate Report'}</span>
          </Button>
        </div>
        {report ? (
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
              className="rounded bg-black px-4 py-2 font-semibold text-white hover:bg-blue-600 disabled:bg-gray-400"
            >
              {saving ? 'Saving...' : 'Save Report'}
            </button>
          </div>
        ) : (
          <div className="p-8 text-center">
            <p className="text-foreground/70">
              Click the button above to generate an AI-powered analysis of your
              alarm patterns.
            </p>
          </div>
        )}
      </div>
      {error && <p className="text-red-500 text-center">{error}</p>}
    </div>
  );
}
