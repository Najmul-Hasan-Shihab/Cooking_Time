import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const Header = () => {
  const { isAuthenticated, user, logout } = useAuthStore();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <header className="bg-white shadow-md">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and main nav */}
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold text-orange-600">🍳 Cooking Time</span>
            </Link>
            <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
              <Link
                to="/recipes"
                className="inline-flex items-center px-1 pt-1 text-gray-900 hover:text-orange-600 transition-colors"
              >
                Recipes
              </Link>
              {isAuthenticated && (
                <Link
                  to="/recipes/create"
                  className="inline-flex items-center px-1 pt-1 text-gray-900 hover:text-orange-600 transition-colors"
                >
                  Create Recipe
                </Link>
              )}
            </div>
          </div>

          {/* Right side - Auth buttons or user menu */}
          <div className="flex items-center space-x-4">
            {isAuthenticated && user ? (
              <>
                <Link
                  to="/profile"
                  className="flex items-center space-x-2 text-gray-700 hover:text-orange-600 transition-colors"
                >
                  <div className="text-right">
                    <div className="text-sm font-medium">{user.username}</div>
                    <div className="text-xs text-gray-500">
                      Level {user.level} • {user.xp} XP
                    </div>
                  </div>
                  {user.avatar_url ? (
                    <img
                      src={user.avatar_url}
                      alt={user.username}
                      className="h-10 w-10 rounded-full"
                    />
                  ) : (
                    <div className="h-10 w-10 rounded-full bg-orange-500 flex items-center justify-center text-white font-bold">
                      {user.username[0].toUpperCase()}
                    </div>
                  )}
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-700 hover:text-orange-600 transition-colors text-sm font-medium"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-orange-600 transition-colors text-sm font-medium"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-colors text-sm font-medium"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
