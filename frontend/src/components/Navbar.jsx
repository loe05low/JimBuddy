import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FaDumbbell, FaUser, FaSignOutAlt, FaHome, FaStar } from 'react-icons/fa';
import NotificationBell from './NotificationBell';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 shadow-2xl sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3 hover:scale-105 transition-transform">
              <div className="bg-white p-2 rounded-xl shadow-lg">
                <FaDumbbell className="text-2xl text-purple-600" />
              </div>
              <span className="text-2xl font-black text-white drop-shadow-lg">SpotMe</span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-2">
            <Link
              to="/"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white backdrop-blur-sm transition-all"
            >
              <FaHome />
              <span className="hidden sm:inline font-semibold">Home</span>
            </Link>

            {user && (
              <>
                <Link
                  to="/profile"
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white backdrop-blur-sm transition-all"
                >
                  <FaUser />
                  <span className="hidden sm:inline font-semibold">{user.profile?.nume || user.username}</span>
                  <div className="bg-yellow-400 text-purple-900 px-2 py-1 rounded-full flex items-center space-x-1 text-xs font-bold shadow-md">
                    <FaStar />
                    <span>{user.profile?.rating || '5.0'}</span>
                  </div>
                </Link>

                <NotificationBell />

                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-red-500/90 hover:bg-red-600 text-white backdrop-blur-sm transition-all font-semibold shadow-lg"
                >
                  <FaSignOutAlt />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
