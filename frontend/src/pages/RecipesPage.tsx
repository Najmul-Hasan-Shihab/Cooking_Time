import { useState } from 'react';
import { useRecipes } from '../hooks/useRecipes';
import RecipeCard from '../components/RecipeCard';
import { RecipeFilters } from '../types';

const RecipesPage = () => {
  const [filters, setFilters] = useState<RecipeFilters>({
    q: '',
    difficulty: undefined,
    cuisine: '',
    tags: [],
    time_max: undefined,
    sort: '-created_at',
    page: 1,
  });

  const { data, isLoading, error } = useRecipes(filters);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({ ...filters, q: e.target.value, page: 1 });
  };

  const handleDifficultyChange = (difficulty: 'easy' | 'medium' | 'hard' | undefined) => {
    setFilters({ ...filters, difficulty, page: 1 });
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilters({ ...filters, sort: e.target.value, page: 1 });
  };

  const handleTimeMaxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value ? parseInt(e.target.value) : undefined;
    setFilters({ ...filters, time_max: value, page: 1 });
  };

  const handlePageChange = (newPage: number) => {
    setFilters({ ...filters, page: newPage });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const clearFilters = () => {
    setFilters({
      q: '',
      difficulty: undefined,
      cuisine: '',
      tags: [],
      time_max: undefined,
      sort: '-created_at',
      page: 1,
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Discover Recipes</h1>
        <p className="text-gray-600">Browse through our collection of delicious recipes</p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        {/* Search Bar */}
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search recipes..."
            value={filters.q || ''}
            onChange={handleSearchChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500"
          />
        </div>

        {/* Filters Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Difficulty Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty
            </label>
            <div className="flex space-x-2">
              <button
                onClick={() => handleDifficultyChange(undefined)}
                className={`flex-1 px-3 py-2 text-sm rounded-md ${
                  !filters.difficulty
                    ? 'bg-orange-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                All
              </button>
              <button
                onClick={() => handleDifficultyChange('easy')}
                className={`flex-1 px-3 py-2 text-sm rounded-md ${
                  filters.difficulty === 'easy'
                    ? 'bg-green-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Easy
              </button>
              <button
                onClick={() => handleDifficultyChange('medium')}
                className={`flex-1 px-3 py-2 text-sm rounded-md ${
                  filters.difficulty === 'medium'
                    ? 'bg-yellow-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Medium
              </button>
              <button
                onClick={() => handleDifficultyChange('hard')}
                className={`flex-1 px-3 py-2 text-sm rounded-md ${
                  filters.difficulty === 'hard'
                    ? 'bg-red-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Hard
              </button>
            </div>
          </div>

          {/* Time Filter */}
          <div>
            <label htmlFor="time" className="block text-sm font-medium text-gray-700 mb-2">
              Max Time (min)
            </label>
            <input
              id="time"
              type="number"
              min="0"
              placeholder="Any"
              value={filters.time_max || ''}
              onChange={handleTimeMaxChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
            />
          </div>

          {/* Sort */}
          <div>
            <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-2">
              Sort By
            </label>
            <select
              id="sort"
              value={filters.sort}
              onChange={handleSortChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="-created_at">Newest First</option>
              <option value="created_at">Oldest First</option>
              <option value="-views">Most Popular</option>
              <option value="-rating_stats.average">Highest Rated</option>
            </select>
          </div>

          {/* Clear Filters */}
          <div className="flex items-end">
            <button
              onClick={clearFilters}
              className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md">
          Error loading recipes. Please try again later.
        </div>
      )}

      {/* Results Count */}
      {data && (
        <div className="mb-4 text-sm text-gray-600">
          Found {data.count} {data.count === 1 ? 'recipe' : 'recipes'}
        </div>
      )}

      {/* Recipe Grid */}
      {data && data.results && data.results.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {data.results.map((recipe) => (
              <RecipeCard key={recipe.id} recipe={recipe} />
            ))}
          </div>

          {/* Pagination */}
          {data.count > 20 && (
            <div className="flex justify-center items-center space-x-2">
              <button
                onClick={() => handlePageChange((filters.page || 1) - 1)}
                disabled={!data.previous}
                className="px-4 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <span className="px-4 py-2 text-gray-700">
                Page {filters.page || 1}
              </span>
              <button
                onClick={() => handlePageChange((filters.page || 1) + 1)}
                disabled={!data.next}
                className="px-4 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          )}
        </>
      ) : (
        !isLoading && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No recipes found</h3>
            <p className="text-gray-500 mb-4">Try adjusting your filters or search terms</p>
            <button
              onClick={clearFilters}
              className="text-orange-600 hover:text-orange-700 font-medium"
            >
              Clear all filters
            </button>
          </div>
        )
      )}
    </div>
  );
};

export default RecipesPage;
