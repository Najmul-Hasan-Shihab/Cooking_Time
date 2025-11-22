import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { useRecipes } from '../hooks/useRecipes';
import { recipeService } from '../services/recipes';
import { Link } from 'react-router-dom';
import { ChefHat, Users, BookOpen, TrendingUp, Lock, Star } from 'lucide-react';
import RecipeCard from '../components/RecipeCard';
import toast from 'react-hot-toast';

const ProfilePage = () => {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState<'recipes' | 'cooked' | 'saved'>('recipes');
  const [cookedRecipes, setCookedRecipes] = useState<any[]>([]);
  const [savedRecipes, setSavedRecipes] = useState<any[]>([]);
  const [cookedCount, setCookedCount] = useState(0);
  const [savedCount, setSavedCount] = useState(0);
  const [isLoadingCooked, setIsLoadingCooked] = useState(false);
  const [isLoadingSaved, setIsLoadingSaved] = useState(false);
  
  // Fetch user's recipes (filtered by author)
  const { data: recipesData, isLoading } = useRecipes(user?.id ? { author: user.id } : {});

  // Fetch cooked recipes
  useEffect(() => {
    if (user && activeTab === 'cooked') {
      setIsLoadingCooked(true);
      recipeService.getCookedRecipes()
        .then(data => {
          setCookedRecipes(data.results);
          setCookedCount(data.count);
        })
        .catch(() => toast.error('Failed to load cooked recipes'))
        .finally(() => setIsLoadingCooked(false));
    }
  }, [user, activeTab]);

  // Fetch saved recipes
  useEffect(() => {
    if (user && activeTab === 'saved') {
      setIsLoadingSaved(true);
      recipeService.getSavedRecipes()
        .then(data => {
          setSavedRecipes(data.results);
          setSavedCount(data.count);
        })
        .catch(() => toast.error('Failed to load saved recipes'))
        .finally(() => setIsLoadingSaved(false));
    }
  }, [user, activeTab]);

  // Fetch cooked count for stats
  useEffect(() => {
    if (user) {
      recipeService.getCookedRecipes()
        .then(data => setCookedCount(data.count))
        .catch(() => {});
    }
  }, [user]);

  if (!user) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Please Log In</h2>
          <Link to="/login" className="text-orange-600 hover:text-orange-700 font-medium">
            Go to Login →
          </Link>
        </div>
      </div>
    );
  }

  // Calculate XP progress to next level
  const xpForNextLevel = user.level * 100;
  const xpProgress = (user.xp % 100);
  const progressPercentage = (xpProgress / 100) * 100;

  // Sample badges data (would come from API in real app)
  const allBadges = [
    { id: '1', name: 'First Recipe', description: 'Create your first recipe', icon: '📝', earned: true },
    { id: '2', name: 'Chef Apprentice', description: 'Cook 10 recipes', icon: '👨‍🍳', earned: true },
    { id: '3', name: 'Recipe Master', description: 'Create 10 recipes', icon: '⭐', earned: false },
    { id: '4', name: 'Social Butterfly', description: 'Get 50 followers', icon: '🦋', earned: false },
    { id: '5', name: 'Rising Star', description: 'Get 100 likes', icon: '✨', earned: true },
    { id: '6', name: 'Master Chef', description: 'Cook 50 recipes', icon: '🏆', earned: false },
    { id: '7', name: 'Food Critic', description: 'Rate 20 recipes', icon: '⚖️', earned: false },
    { id: '8', name: 'Early Adopter', description: 'Join in the first month', icon: '🎉', earned: true },
  ];

  const earnedBadges = allBadges.filter(b => b.earned);
  const lockedBadges = allBadges.filter(b => !b.earned);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Profile Header */}
      <div className="bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl p-8 mb-8 text-white">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center text-4xl font-bold text-orange-600 shadow-lg">
              {user.username[0].toUpperCase()}
            </div>
            <div>
              <h1 className="text-3xl font-bold mb-2">{user.username}</h1>
              <p className="text-orange-100 mb-3">{user.email}</p>
              {user.bio && <p className="text-white/90 max-w-md">{user.bio}</p>}
            </div>
          </div>
          <Link
            to="/profile/edit"
            className="px-4 py-2 bg-white text-orange-600 rounded-lg font-semibold hover:bg-orange-50 transition"
          >
            Edit Profile
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Level & XP Card */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Level & XP</h3>
              <div className="flex items-center gap-2 text-orange-600">
                <TrendingUp className="w-5 h-5" />
                <span className="text-2xl font-bold">Level {user.level}</span>
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between text-sm text-gray-600">
                <span>{user.xp} XP</span>
                <span>{xpForNextLevel} XP</span>
              </div>
              <div className="relative h-4 bg-gray-200 rounded-full overflow-hidden">
                <div
                  className="absolute inset-y-0 left-0 bg-gradient-to-r from-orange-500 to-red-500 rounded-full transition-all duration-500"
                  style={{ width: `${progressPercentage}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 text-center">
                {100 - xpProgress} XP to Level {user.level + 1}
              </p>
            </div>
          </div>

          {/* Stats Card */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Statistics</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                    <BookOpen className="w-5 h-5 text-orange-600" />
                  </div>
                  <span className="text-gray-700">Recipes Created</span>
                </div>
                <span className="text-xl font-bold text-gray-900">
                  {recipesData?.count || 0}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <ChefHat className="w-5 h-5 text-green-600" />
                  </div>
                  <span className="text-gray-700">Recipes Cooked</span>
                </div>
                <span className="text-xl font-bold text-gray-900">{cookedCount}</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Users className="w-5 h-5 text-blue-600" />
                  </div>
                  <span className="text-gray-700">Followers</span>
                </div>
                <span className="text-xl font-bold text-gray-900">{user.followers_count}</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Users className="w-5 h-5 text-purple-600" />
                  </div>
                  <span className="text-gray-700">Following</span>
                </div>
                <span className="text-xl font-bold text-gray-900">{user.following_count}</span>
              </div>
            </div>
          </div>

          {/* Badges Card */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Badges</h3>
              <span className="text-sm text-gray-500">
                {earnedBadges.length}/{allBadges.length}
              </span>
            </div>

            {/* Earned Badges */}
            <div className="mb-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Earned</h4>
              <div className="grid grid-cols-4 gap-2">
                {earnedBadges.map((badge) => (
                  <div
                    key={badge.id}
                    className="relative group"
                    title={`${badge.name}: ${badge.description}`}
                  >
                    <div className="aspect-square bg-gradient-to-br from-orange-100 to-yellow-100 rounded-lg flex items-center justify-center text-3xl border-2 border-orange-300 shadow-sm hover:scale-110 transition cursor-pointer">
                      {badge.icon}
                    </div>
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block">
                      <div className="bg-gray-900 text-white text-xs rounded px-2 py-1 whitespace-nowrap">
                        {badge.name}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Locked Badges */}
            {lockedBadges.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Locked</h4>
                <div className="grid grid-cols-4 gap-2">
                  {lockedBadges.map((badge) => (
                    <div
                      key={badge.id}
                      className="relative group"
                      title={`${badge.name}: ${badge.description}`}
                    >
                      <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center text-3xl grayscale opacity-40 border-2 border-gray-200 cursor-pointer">
                        {badge.icon}
                        <Lock className="absolute w-4 h-4 text-gray-400" />
                      </div>
                      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-10">
                        <div className="bg-gray-900 text-white text-xs rounded px-2 py-1 whitespace-nowrap">
                          {badge.name}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Preferences Card */}
          {user.preferences && (
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h3>
              
              {user.preferences.cuisines && user.preferences.cuisines.length > 0 && (
                <div className="mb-3">
                  <p className="text-sm font-medium text-gray-700 mb-2">Favorite Cuisines</p>
                  <div className="flex flex-wrap gap-2">
                    {user.preferences.cuisines.map((cuisine) => (
                      <span key={cuisine} className="px-2 py-1 bg-orange-100 text-orange-700 rounded-full text-xs">
                        {cuisine}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {user.preferences.dietary_restrictions && user.preferences.dietary_restrictions.length > 0 && (
                <div className="mb-3">
                  <p className="text-sm font-medium text-gray-700 mb-2">Dietary Restrictions</p>
                  <div className="flex flex-wrap gap-2">
                    {user.preferences.dietary_restrictions.map((restriction) => (
                      <span key={restriction} className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs">
                        {restriction}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {user.preferences.favorite_tags && user.preferences.favorite_tags.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">Favorite Tags</p>
                  <div className="flex flex-wrap gap-2">
                    {user.preferences.favorite_tags.map((tag) => (
                      <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Main Content */}
        <div className="lg:col-span-2">
          {/* Tabs */}
          <div className="bg-white rounded-xl border border-gray-200 mb-6">
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('recipes')}
                className={`flex-1 px-6 py-4 text-sm font-medium transition ${
                  activeTab === 'recipes'
                    ? 'text-orange-600 border-b-2 border-orange-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                My Recipes ({recipesData?.count || 0})
              </button>
              <button
                onClick={() => setActiveTab('cooked')}
                className={`flex-1 px-6 py-4 text-sm font-medium transition ${
                  activeTab === 'cooked'
                    ? 'text-orange-600 border-b-2 border-orange-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Cooked ({cookedCount})
              </button>
              <button
                onClick={() => setActiveTab('saved')}
                className={`flex-1 px-6 py-4 text-sm font-medium transition ${
                  activeTab === 'saved'
                    ? 'text-orange-600 border-b-2 border-orange-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Saved ({savedCount})
              </button>
            </div>
          </div>

          {/* Content */}
          <div>
            {activeTab === 'recipes' && (
              <div>
                {isLoading ? (
                  <div className="flex justify-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
                  </div>
                ) : recipesData?.results && recipesData.results.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {recipesData.results.map((recipe) => (
                      <RecipeCard key={recipe.id} recipe={recipe} />
                    ))}
                  </div>
                ) : (
                  <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <BookOpen className="w-8 h-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">No recipes yet</h3>
                    <p className="text-gray-600 mb-4">Start sharing your culinary creations with the community!</p>
                    <Link
                      to="/recipes/create"
                      className="inline-flex items-center gap-2 px-6 py-3 bg-orange-600 text-white rounded-lg font-semibold hover:bg-orange-700 transition"
                    >
                      <BookOpen className="w-5 h-5" />
                      Create Your First Recipe
                    </Link>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'cooked' && (
              <div>
                {isLoadingCooked ? (
                  <div className="flex justify-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
                  </div>
                ) : cookedRecipes.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {cookedRecipes.map((recipe) => (
                      <RecipeCard key={recipe.id} recipe={recipe} />
                    ))}
                  </div>
                ) : (
                  <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <ChefHat className="w-8 h-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">No recipes cooked yet</h3>
                    <p className="text-gray-600">Start cooking and mark recipes as cooked to track your progress!</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'saved' && (
              <div>
                {isLoadingSaved ? (
                  <div className="flex justify-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
                  </div>
                ) : savedRecipes.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {savedRecipes.map((recipe) => (
                      <RecipeCard key={recipe.id} recipe={recipe} />
                    ))}
                  </div>
                ) : (
                  <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Star className="w-8 h-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">No saved recipes yet</h3>
                    <p className="text-gray-600">Save your favorite recipes to easily find them later!</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
