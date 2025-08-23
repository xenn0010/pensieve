import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Chessboard from './pages/Chessboard';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/chessboard" element={<Chessboard />} />
          <Route path="/signals" element={<div className="p-6 text-center">Signals Page - Coming Soon</div>} />
          <Route path="/vendors" element={<div className="p-6 text-center">Vendors Page - Coming Soon</div>} />
          <Route path="/actions" element={<div className="p-6 text-center">Actions Page - Coming Soon</div>} />
          <Route path="/settings" element={<div className="p-6 text-center">Settings Page - Coming Soon</div>} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
