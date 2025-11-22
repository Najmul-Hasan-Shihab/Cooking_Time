import { useState, useEffect } from 'react';
import { leaderboardService, LeaderboardUser } from '../services/leaderboard';
import { Trophy, TrendingUp, ChefHat, BookOpen, Award, Crown } from 'lucide-react';
import toast from 'react-hot-toast';

type LeaderboardType = 'xp' | 'recipes' | 'cooked';
type Timeframe = 'all' | 'week' | 'month' | 'year';

const LeaderboardPage = () => {
  const [activeType, setActiveType] = useState<LeaderboardType>('xp');
  const [timeframe, setTimeframe] = useState<Timeframe>('all');
  const [leaderboard, setLeaderboard] = useState<LeaderboardUser[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchLeaderboard();
  }, [activeType, timeframe, page]);

  const fetchLeaderboard = async () => {
    setIsLoading(true);
    try {
      let data;
      if (activeType === 'xp') {
        data = await leaderboardService.getByXP(timeframe, page);
      } else if (activeType === 'recipes') {
        data = await leaderboardService.getByRecipes(page);
      } else {
        data = await leaderboardService.getByCooked(page);
      }
      setLeaderboard(data.results);
      setTotalPages(data.total_pages);
    } catch (error) {
      toast.error('Failed to load leaderboard');
    } finally {
      setIsLoading(false);
    }
  };

  const getRankDisplay = (rank: number) => {
    if (rank === 1) return { icon: <Crown className="w-6 h-6 text-yellow-500" />, color: 'text-yellow-600 bg-yellow-50' };
    if (rank === 2) return { icon: <Award className="w-6 h-6 text-gray-400" />, color: 'text-gray-600 bg-gray-50' };
    if (rank === 3) return { icon: <Award className="w-6 h-6 text-orange-500" />, color: 'text-orange-600 bg-orange-50' };
    return { icon: <span className="text-lg font-bold text-gray-600">#{rank}</span>, color: 'text-gray-600' };
  };

  const getTypeIcon = (type: LeaderboardType) => {
    switch (type) {
      case 'xp': return <TrendingUp className="w-5 h-5" />;
      case 'recipes': return <BookOpen className="w-5 h-5" />;
      case 'cooked': return <ChefHat className="w-5 h-5" />;
    }
  };

  const getTypeLabel = (type: LeaderboardType) => {
    switch (type) {
      case 'xp': return 'Top XP';
      case 'recipes': return 'Most Recipes';
      case 'cooked': return 'Most Cooked';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-3">
          <Trophy className="w-10 h-10 text-orange-600" />
          <h1 className="text-4xl font-bold text-gray-900">Leaderboard</h1>
        </div>
        <p className="text-lg text-gray-600">
          Compete with the best chefs in the community!
        </p>
      </div>

      {/* Type Tabs */}
      <div className="bg-white rounded-xl border border-gray-200 mb-6">
        <div className="flex overflow-x-auto">
          {(['xp', 'recipes', 'cooked'] as LeaderboardType[]).map((type) => (
            <button
              key={type}
              onClick={() => {
                setActiveType(type);
                setPage(1);
              }}
              className={`flex-1 px-6 py-4 text-sm font-medium transition flex items-center justify-center gap-2 whitespace-nowrap ${
                activeType === type
                  ? 'text-orange-600 border-b-2 border-orange-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {getTypeIcon(type)}
              {getTypeLabel(type)}
            </button>
          ))}
        </div>
      </div>

      {/* Timeframe Filter (only for XP) */}
      {activeType === 'xp' && (
        <div className="bg-white rounded-xl border border-gray-200 p-4 mb-6">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-medium text-gray-700">Timeframe:</span>
            {(['all', 'year', 'month', 'week'] as Timeframe[]).map((tf) => (
              <button
                key={tf}
                onClick={() => {
                  setTimeframe(tf);
                  setPage(1);
                }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                  timeframe === tf
                    ? 'bg-orange-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {tf.charAt(0).toUpperCase() + tf.slice(1)}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Leaderboard Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
          </div>
        ) : leaderboard.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Rank</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">User</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Level</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                    {activeType === 'xp' ? 'XP' : activeType === 'recipes' ? 'Recipes' : 'Cooked'}
                  </th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Stats</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {leaderboard.map((entry) => {
                  const rankDisplay = getRankDisplay(entry.rank);
                  return (
                    <tr key={entry.user.id} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4">
                        <div className={`flex items-center justify-center w-12 h-12 rounded-full ${rankDisplay.color}`}>
                          {rankDisplay.icon}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-semibold">
                            {entry.user.username.charAt(0).toUpperCase()}
                          </div>
                          <span className="font-semibold text-gray-900">{entry.user.username}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium">
                          Level {entry.user.level}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-lg font-bold text-gray-900">
                          {activeType === 'xp' 
                            ? entry.user.xp.toLocaleString()
                            : activeType === 'recipes'
                            ? entry.stats.recipes_created
                            : entry.stats.recipes_cooked}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                          <div className="flex items-center gap-1">
                            <BookOpen className="w-4 h-4" />
                            <span>{entry.stats.recipes_created}</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <ChefHat className="w-4 h-4" />
                            <span>{entry.stats.recipes_cooked}</span>
                          </div>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <Trophy className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No data yet</h3>
            <p className="text-gray-600">Start cooking to appear on the leaderboard!</p>
          </div>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="mt-6 flex items-center justify-center gap-2">
          <button
            onClick={() => setPage(page - 1)}
            disabled={page === 1}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="px-4 py-2 text-sm text-gray-700">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(page + 1)}
            disabled={page === totalPages}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default LeaderboardPage;
