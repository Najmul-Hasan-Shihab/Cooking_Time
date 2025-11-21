import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const HomePage = () => {
  const { isAuthenticated, user } = useAuthStore();

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-orange-500 to-red-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-6">
              Welcome to Cooking Time! 🍳
            </h1>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              Discover delicious recipes, share your culinary creations, and level up your cooking skills with our gamified platform.
            </p>
            <div className="flex justify-center space-x-4">
              <Link
                to="/recipes"
                className="bg-white text-orange-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Browse Recipes
              </Link>
              {!isAuthenticated && (
                <Link
                  to="/register"
                  className="bg-transparent border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-orange-600 transition-colors"
                >
                  Get Started
                </Link>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Why Cooking Time?</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4">📚</div>
            <h3 className="text-xl font-semibold mb-2">Discover Recipes</h3>
            <p className="text-gray-600">
              Browse thousands of recipes with detailed instructions, ingredients, and cooking times.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4">🎮</div>
            <h3 className="text-xl font-semibold mb-2">Earn XP & Badges</h3>
            <p className="text-gray-600">
              Level up by cooking recipes, sharing your creations, and engaging with the community.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="text-4xl mb-4">👥</div>
            <h3 className="text-xl font-semibold mb-2">Join Community</h3>
            <p className="text-gray-600">
              Follow other cooks, share your recipes, and get inspired by the community.
            </p>
          </div>
        </div>
      </div>

      {/* Stats Section (if authenticated) */}
      {isAuthenticated && user && (
        <div className="bg-gray-100 py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-center mb-12">Your Progress</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-md text-center">
                <div className="text-3xl font-bold text-orange-600">{user.level}</div>
                <div className="text-gray-600 mt-2">Level</div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md text-center">
                <div className="text-3xl font-bold text-orange-600">{user.xp}</div>
                <div className="text-gray-600 mt-2">XP</div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md text-center">
                <div className="text-3xl font-bold text-orange-600">{user.badges.length}</div>
                <div className="text-gray-600 mt-2">Badges</div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-md text-center">
                <div className="text-3xl font-bold text-orange-600">{user.followers_count}</div>
                <div className="text-gray-600 mt-2">Followers</div>
              </div>
            </div>
            <div className="text-center mt-8">
              <Link
                to="/profile"
                className="text-orange-600 hover:text-orange-700 font-semibold"
              >
                View Full Profile →
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* CTA Section */}
      <div className="bg-orange-600 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Cooking?</h2>
          <p className="text-xl mb-8">
            Join our community of food lovers and start your culinary journey today!
          </p>
          <Link
            to={isAuthenticated ? "/recipes/create" : "/register"}
            className="bg-white text-orange-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-block"
          >
            {isAuthenticated ? "Create Your First Recipe" : "Sign Up Now"}
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
