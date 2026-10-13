import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ScrollManager from './components/ScrollManager';
import Home from './pages/Home';
import AllHackathons from './pages/AllHackathons';
import HackathonDetail from './pages/HackathonDetail';
import Feedback from './pages/Feedback';
import Credits from './pages/Credits';

export default function App() {
  return (
    <BrowserRouter>
      <ScrollManager />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/hackathons" element={<AllHackathons />} />
        <Route path="/hackathon/:id" element={<HackathonDetail />} />
        <Route path="/feedback" element={<Feedback />} />
        <Route path="/credits" element={<Credits />} />
      </Routes>
    </BrowserRouter>
  );
}
