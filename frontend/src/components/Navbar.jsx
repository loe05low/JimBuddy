import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FaDumbbell, FaUser, FaSignOutAlt, FaHome, FaStar } from 'react-icons/fa';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2 hover:opacity-80 transition">
              <FaDumbbell className="text-3xl text-primary" />
              <span className="text-2xl font-bold text-gray-800">SpotMe</span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-4">
            <Link
              to="/"
              className="flex items-center space-x-1 px-3 py-2 rounded-lg hover:bg-gray-100 transition"
            >
              <FaHome />
              <span className="hidden sm:inline">Home</span>
            </Link>

            {user && (
              <>
                <Link
                  to="/profile"
                  className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100 transition"
                >
                  <FaUser />
                  <span className="hidden sm:inline">{user.profile?.nume || user.username}</span>
                  <span className="badge-info flex items-center space-x-1">
                    <FaStar className="text-xs" />
                    <span>{user.profile?.rating || '5.0'}</span>
                  </span>
                </Link>

                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 px-3 py-2 rounded-lg hover:bg-red-50 text-red-600 transition"
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
