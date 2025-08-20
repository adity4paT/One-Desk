
const MeetingSummarizer = () => {
  const [transcript, setTranscript] = useState('');
  const [fileName, setFileName] = useState('');
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    setFileName(file.name);
    const text = await file.text();
    setTranscript(text);
  };

  const handleSummarize = async () => {
    setLoading(true);
    setSummary([]);
    try {
      const res = await fetch('http://localhost:5000/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript }),
      });
      const data = await res.json();
      setSummary(data.summary || []);
    } catch (err) {
      setSummary(['Error summarizing transcript.']);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">Meeting Summarizer</h1>
      <textarea
        className="w-full p-4 border rounded mb-4"
        rows={8}
        placeholder="Paste meeting transcript here..."
        value={transcript}
        onChange={e => setTranscript(e.target.value)}
      />
      <div className="flex items-center gap-4 mb-4">
        <input
          type="file"
          accept=".txt"
          onChange={handleFileChange}
          id="transcript-upload"
          style={{ display: 'none' }}
        />
        <label htmlFor="transcript-upload">
          <ReusableButton variant="outlined" size="small">
            Upload .txt File
          </ReusableButton>
        </label>
        {fileName && <span className="text-sm text-gray-600">{fileName}</span>}
      </div>
      <ReusableButton
        onClick={handleSummarize}
        disabled={!transcript || loading}
        fullWidth
        startIcon="📝"
      >
        {loading ? 'Summarizing...' : 'Summarize'}
      </ReusableButton>
      {summary.length > 0 && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-2">Summary</h2>
          <ul className="list-disc pl-6">
            {summary.map((point, idx) => (
              <li key={idx} className="mb-2">{point}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MeetingSummarizer;
