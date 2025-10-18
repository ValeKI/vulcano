import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from '../pages/Home';
import Chat from '../pages/Chat';
import { AuthProvider } from '../context/AuthContext';
import ProtectedRoute from './ProtectedRoute';

const AppRouter = () => (
  <AuthProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  </AuthProvider>
);

export default AppRouter;