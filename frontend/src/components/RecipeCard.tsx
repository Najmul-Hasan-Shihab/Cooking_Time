import { Link } from 'react-router-dom';
import { RecipeListItem } from '../types';

interface RecipeCardProps {
  recipe: RecipeListItem;
}

const RecipeCard = ({ recipe }: RecipeCardProps) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'hard':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRarityEmoji = (rarity: string) => {
    switch (rarity) {
      case 'legendary':
        return '⭐';
      case 'rare':
        return '💎';
      case 'uncommon':
        return '🔷';
      default:
        return '';
    }
  };

  return (
    <Link to={`/recipes/${recipe.slug}`} className="block group">
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
        {/* Image */}
        <div className="relative h-48 bg-gray-200 overflow-hidden">
          {recipe.images && recipe.images.length > 0 ? (
            <img
              src={recipe.images[0]}
              alt={recipe.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400 text-6xl">
              🍳
            </div>
          )}
          {/* Rarity badge */}
          {recipe.rarity !== 'common' && (
            <div className="absolute top-2 right-2 bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-sm font-semibold">
              {getRarityEmoji(recipe.rarity)} {recipe.rarity}
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-4">
          {/* Title */}
          <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-orange-600 transition-colors">
            {recipe.title}
          </h3>

          {/* Description */}
          <p className="text-sm text-gray-600 mb-3 line-clamp-2">
            {recipe.description}
          </p>

          {/* Tags */}
          <div className="flex flex-wrap gap-1 mb-3">
            {recipe.tags.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full"
              >
                #{tag}
              </span>
            ))}
            {recipe.tags.length > 3 && (
              <span className="text-xs text-gray-500 px-2 py-1">
                +{recipe.tags.length - 3} more
              </span>
            )}
          </div>

          {/* Meta info */}
          <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
            <div className="flex items-center space-x-3">
              <span className="flex items-center">
                ⏱️ {recipe.total_time} min
              </span>
              <span className="flex items-center">
                🍽️ {recipe.servings}
              </span>
            </div>
            <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(recipe.difficulty)}`}>
              {recipe.difficulty}
            </span>
          </div>

          {/* Stats */}
          <div className="flex items-center justify-between pt-3 border-t border-gray-100">
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <span>👁️ {recipe.views}</span>
              <span>•</span>
              <span>🔥 {recipe.cook_count}</span>
              {recipe.rating_stats.count > 0 && (
                <>
                  <span>•</span>
                  <span>⭐ {recipe.rating_stats.average.toFixed(1)}</span>
                </>
              )}
            </div>
            <div className="flex items-center space-x-1 text-xs text-gray-500">
              {recipe.author.avatar_url ? (
                <img
                  src={recipe.author.avatar_url}
                  alt={recipe.author.username}
                  className="w-5 h-5 rounded-full"
                />
              ) : (
                <div className="w-5 h-5 rounded-full bg-orange-500 flex items-center justify-center text-white text-xs">
                  {recipe.author.username[0].toUpperCase()}
                </div>
              )}
              <span className="font-medium">{recipe.author.username}</span>
              <span className="text-orange-600">Lv{recipe.author.level}</span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default RecipeCard;
