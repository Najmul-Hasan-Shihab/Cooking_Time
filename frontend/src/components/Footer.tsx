const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-bold mb-4">🍳 Cooking Time</h3>
            <p className="text-gray-400 text-sm">
              Share your favorite recipes and discover new culinary adventures. 
              Earn XP, unlock badges, and level up your cooking skills!
            </p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-gray-400 text-sm">
              <li><a href="/recipes" className="hover:text-white transition-colors">Browse Recipes</a></li>
              <li><a href="/recipes/create" className="hover:text-white transition-colors">Create Recipe</a></li>
              <li><a href="/profile" className="hover:text-white transition-colors">My Profile</a></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">About</h3>
            <p className="text-gray-400 text-sm">
              Built with Django REST Framework, MongoDB, React, and TypeScript.
              <br />
              <span className="text-orange-500">Phase 2: Frontend UI ✨</span>
            </p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; {new Date().getFullYear()} Cooking Time. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
