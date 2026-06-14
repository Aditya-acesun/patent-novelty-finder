import { Routes, Route, Navigate } from 'react-router-dom';

// Phase 3 will replace these stubs with real pages
function ComingSoon({ name }: { name: string }) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'monospace' }}>
      <h2>⚙️ {name}</h2>
      <p>This page will be built in the upcoming phase.</p>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/"          element={<ComingSoon name="Dashboard" />} />
      <Route path="/login"     element={<ComingSoon name="Login" />} />
      <Route path="/register"  element={<ComingSoon name="Register" />} />
      <Route path="/search"    element={<ComingSoon name="Search" />} />
      <Route path="/novelty"   element={<ComingSoon name="Novelty Score" />} />
      <Route path="/reports"   element={<ComingSoon name="Reports" />} />
      <Route path="*"          element={<Navigate to="/" replace />} />
    </Routes>
  );
}
