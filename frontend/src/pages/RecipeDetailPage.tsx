import { useParams, Link, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useRecipe } from '../hooks/useRecipes';
import { useAuthStore } from '../store/authStore';
import { Clock, Users, ChefHat, Star, Eye, Heart, Share2, BookmarkPlus, Award, Send, Edit2, Trash2, ThumbsUp } from 'lucide-react';
import { recipeService } from '../services/recipes';
import { commentService, Comment } from '../services/comments';
import toast from 'react-hot-toast';

const RecipeDetailPage = () => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuthStore();
  const { data: recipe, isLoading, error } = useRecipe(slug!);
  const [comment, setComment] = useState('');
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);
  const [isMarkingCooked, setIsMarkingCooked] = useState(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentsCount, setCommentsCount] = useState(0);
  const [isLoadingComments, setIsLoadingComments] = useState(false);
  const [editingCommentId, setEditingCommentId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState('');

  // Fetch comments
  useEffect(() => {
    if (slug) {
      setIsLoadingComments(true);
      commentService.getComments(slug)
        .then(data => {
          setComments(data.comments || []);
          setCommentsCount(data.pagination?.total || 0);
        })
        .catch(() => toast.error('Failed to load comments'))
        .finally(() => setIsLoadingComments(false));
    }
  }, [slug]);

  const handleMarkAsCooked = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to mark recipes as cooked');
      navigate('/login');
      return;
    }
    
    setIsMarkingCooked(true);
    try {
      const result = await recipeService.markAsCooked(slug!);
      toast.success(`Recipe marked as cooked! 🎉 +${result.xp_awarded} XP`);
      // Optionally refresh user data here
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to mark recipe as cooked');
    } finally {
      setIsMarkingCooked(false);
    }
  };

  const handleSaveRecipe = async () => {
    if (!isAuthenticated) {
      toast.error('Please login to save recipes');
      navigate('/login');
      return;
    }
    
    try {
      const result = await recipeService.toggleSaveRecipe(slug!);
      if (result.is_saved) {
        toast.success('Recipe saved to your collection! 📚');
      } else {
        toast.success('Recipe removed from your collection');
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to save recipe');
    }
  };

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isAuthenticated) {
      toast.error('Please login to comment');
      navigate('/login');
      return;
    }
    
    if (!comment.trim()) {
      toast.error('Please enter a comment');
      return;
    }

    setIsSubmittingComment(true);
    try {
      const result = await commentService.createComment(slug!, comment);
      toast.success(`Comment posted! +${result.xp_awarded} XP 💬`);
      setComment('');
      // Add new comment to the list
      setComments([result.comment, ...comments]);
      setCommentsCount(commentsCount + 1);
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to post comment');
    } finally {
      setIsSubmittingComment(false);
    }
  };

  const handleEditComment = async (commentId: string) => {
    if (!editContent.trim()) {
      toast.error('Comment cannot be empty');
      return;
    }

    try {
      const updated = await commentService.updateComment(slug!, commentId, editContent);
      setComments(comments.map(c => c.id === commentId ? updated : c));
      setEditingCommentId(null);
      setEditContent('');
      toast.success('Comment updated!');
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to update comment');
    }
  };

  const handleDeleteComment = async (commentId: string) => {
    if (!confirm('Are you sure you want to delete this comment?')) return;

    try {
      await commentService.deleteComment(slug!, commentId);
      setComments(comments.filter(c => c.id !== commentId));
      setCommentsCount(commentsCount - 1);
      toast.success('Comment deleted');
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to delete comment');
    }
  };

  const handleLikeComment = async (commentId: string) => {
    if (!isAuthenticated) {
      toast.error('Please login to like comments');
      navigate('/login');
      return;
    }

    try {
      const result = await commentService.toggleLike(slug!, commentId);
      setComments(comments.map(c => 
        c.id === commentId 
          ? { ...c, is_liked: result.is_liked, likes_count: result.likes_count }
          : c
      ));
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to like comment');
    }
  };

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    toast.success('Recipe link copied to clipboard! 🔗');
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'text-green-600 bg-green-50 border-green-200';
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'hard': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getRarityDisplay = (rarity: string) => {
    const configs = {
      common: { emoji: '⚪', color: 'text-gray-600', bg: 'bg-gray-100', label: 'Common' },
      uncommon: { emoji: '🟢', color: 'text-green-600', bg: 'bg-green-100', label: 'Uncommon' },
      rare: { emoji: '🔵', color: 'text-blue-600', bg: 'bg-blue-100', label: 'Rare' },
      legendary: { emoji: '🟠', color: 'text-orange-600', bg: 'bg-orange-100', label: 'Legendary' }
    };
    return configs[rarity as keyof typeof configs] || configs.common;
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading recipe...</p>
        </div>
      </div>
    );
  }

  if (error || !recipe) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-red-800 mb-2">Recipe Not Found</h2>
          <p className="text-red-600 mb-4">The recipe you're looking for doesn't exist or has been removed.</p>
          <Link to="/recipes" className="text-orange-600 hover:text-orange-700 font-medium">
            ← Back to Recipes
          </Link>
        </div>
      </div>
    );
  }

  const rarityConfig = getRarityDisplay(recipe.rarity);
  const mainImage = recipe.images[0] || '';

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <div className="mb-6 text-sm text-gray-600">
        <Link to="/" className="hover:text-orange-600">Home</Link>
        {' / '}
        <Link to="/recipes" className="hover:text-orange-600">Recipes</Link>
        {' / '}
        <span className="text-gray-900">{recipe.title}</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-8">
          {/* Header */}
          <div>
            <div className="flex items-center gap-3 mb-3">
              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${rarityConfig.bg} ${rarityConfig.color}`}>
                {rarityConfig.emoji} {rarityConfig.label}
              </span>
              <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getDifficultyColor(recipe.difficulty)}`}>
                {recipe.difficulty.toUpperCase()}
              </span>
            </div>
            
            <h1 className="text-4xl font-bold text-gray-900 mb-4">{recipe.title}</h1>
            
            <p className="text-lg text-gray-600 mb-6">{recipe.description}</p>

            {/* Author & Stats */}
            <div className="flex items-center justify-between border-y border-gray-200 py-4">
              <Link 
                to={`/profile/${recipe.author.id}`}
                className="flex items-center gap-3 hover:opacity-80 transition"
              >
                <div className="w-12 h-12 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center text-white font-bold">
                  {recipe.author.username[0].toUpperCase()}
                </div>
                <div>
                  <p className="font-semibold text-gray-900">{recipe.author.username}</p>
                  <p className="text-sm text-gray-500">Level {recipe.author.level}</p>
                </div>
              </Link>

              <div className="flex items-center gap-6 text-sm text-gray-600">
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                  <span className="font-semibold">{recipe.rating_stats.average.toFixed(1)}</span>
                  <span>({recipe.rating_stats.count})</span>
                </div>
                <div className="flex items-center gap-1">
                  <Eye className="w-4 h-4" />
                  <span>{recipe.views}</span>
                </div>
                <div className="flex items-center gap-1">
                  <ChefHat className="w-4 h-4" />
                  <span>{recipe.cook_count} cooked</span>
                </div>
              </div>
            </div>
          </div>

          {/* Main Image */}
          <div className="relative h-96 bg-gray-200 rounded-xl overflow-hidden">
            {mainImage ? (
              <img src={mainImage} alt={recipe.title} className="w-full h-full object-cover" />
            ) : (
              <div className="flex items-center justify-center h-full text-6xl">
                {recipe.cuisine === 'Italian' ? '🍝' : 
                 recipe.cuisine === 'Chinese' ? '🥡' :
                 recipe.cuisine === 'Japanese' ? '🍱' :
                 recipe.cuisine === 'Mexican' ? '🌮' : '🍽️'}
              </div>
            )}
          </div>

          {/* Ingredients */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              📋 Ingredients
              <span className="text-sm font-normal text-gray-500">({recipe.servings} servings)</span>
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {recipe.ingredients.map((ingredient, index) => (
                <div key={index} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                  <input 
                    type="checkbox" 
                    className="mt-1 w-5 h-5 text-orange-600 rounded focus:ring-orange-500" 
                  />
                  <div className="flex-1">
                    <span className="font-medium text-gray-900">{ingredient.quantity} {ingredient.unit}</span>
                    {' '}
                    <span className="text-gray-700">{ingredient.name}</span>
                    {ingredient.optional && (
                      <span className="text-xs text-gray-500 ml-2">(optional)</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Instructions */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">👨‍🍳 Instructions</h2>
            <div className="space-y-6">
              {recipe.steps.map((step) => (
                <div key={step.step_number} className="flex gap-4">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-orange-600 text-white rounded-full flex items-center justify-center font-bold">
                      {step.step_number}
                    </div>
                  </div>
                  <div className="flex-1 pt-1">
                    <p className="text-gray-700 leading-relaxed">{step.text}</p>
                    {step.step_time && (
                      <p className="text-sm text-gray-500 mt-2">⏱️ ~{step.step_time} minutes</p>
                    )}
                    {step.image && (
                      <img 
                        src={step.image} 
                        alt={`Step ${step.step_number}`} 
                        className="mt-3 rounded-lg w-full max-w-md"
                      />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Nutrition Info */}
          {recipe.nutrition_info && (
            <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-xl border border-green-200 p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">🥗 Nutrition Info</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {recipe.nutrition_info.calories && (
                  <div className="bg-white rounded-lg p-4 text-center">
                    <p className="text-2xl font-bold text-gray-900">{recipe.nutrition_info.calories}</p>
                    <p className="text-sm text-gray-600">Calories</p>
                  </div>
                )}
                {recipe.nutrition_info.protein && (
                  <div className="bg-white rounded-lg p-4 text-center">
                    <p className="text-2xl font-bold text-gray-900">{recipe.nutrition_info.protein}g</p>
                    <p className="text-sm text-gray-600">Protein</p>
                  </div>
                )}
                {recipe.nutrition_info.carbs && (
                  <div className="bg-white rounded-lg p-4 text-center">
                    <p className="text-2xl font-bold text-gray-900">{recipe.nutrition_info.carbs}g</p>
                    <p className="text-sm text-gray-600">Carbs</p>
                  </div>
                )}
                {recipe.nutrition_info.fat && (
                  <div className="bg-white rounded-lg p-4 text-center">
                    <p className="text-2xl font-bold text-gray-900">{recipe.nutrition_info.fat}g</p>
                    <p className="text-sm text-gray-600">Fat</p>
                  </div>
                )}
                {recipe.nutrition_info.fiber && (
                  <div className="bg-white rounded-lg p-4 text-center">
                    <p className="text-2xl font-bold text-gray-900">{recipe.nutrition_info.fiber}g</p>
                    <p className="text-sm text-gray-600">Fiber</p>
                  </div>
                )}
                {recipe.nutrition_info.sugar && (
                  <div className="bg-white rounded-lg p-4 text-center">
                    <p className="text-2xl font-bold text-gray-900">{recipe.nutrition_info.sugar}g</p>
                    <p className="text-sm text-gray-600">Sugar</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Tags */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {recipe.tags.map((tag) => (
                <span 
                  key={tag}
                  className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition cursor-pointer"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-8 space-y-4">
            {/* Quick Stats Card */}
            <div className="bg-white rounded-xl border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Info</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Clock className="w-5 h-5" />
                    <span className="text-sm">Prep Time</span>
                  </div>
                  <span className="font-semibold text-gray-900">{recipe.prep_time} min</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Clock className="w-5 h-5" />
                    <span className="text-sm">Cook Time</span>
                  </div>
                  <span className="font-semibold text-gray-900">{recipe.cook_time} min</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Clock className="w-5 h-5" />
                    <span className="text-sm">Total Time</span>
                  </div>
                  <span className="font-semibold text-orange-600">{recipe.total_time} min</span>
                </div>
                <div className="flex items-center justify-between pt-2 border-t border-gray-200">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Users className="w-5 h-5" />
                    <span className="text-sm">Servings</span>
                  </div>
                  <span className="font-semibold text-gray-900">{recipe.servings}</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Award className="w-5 h-5" />
                    <span className="text-sm">Cuisine</span>
                  </div>
                  <span className="font-semibold text-gray-900">{recipe.cuisine}</span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="space-y-3">
              <button
                onClick={handleMarkAsCooked}
                disabled={isMarkingCooked}
                className="w-full bg-orange-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition flex items-center justify-center gap-2 shadow-lg shadow-orange-200"
              >
                <ChefHat className="w-5 h-5" />
                {isMarkingCooked ? 'Marking...' : 'Mark as Cooked'}
              </button>
              
              <button
                onClick={handleSaveRecipe}
                className="w-full bg-white text-gray-700 py-3 px-4 rounded-lg font-semibold hover:bg-gray-50 transition border border-gray-300 flex items-center justify-center gap-2"
              >
                <BookmarkPlus className="w-5 h-5" />
                Save Recipe
              </button>
              
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={handleShare}
                  className="bg-white text-gray-700 py-3 px-4 rounded-lg font-semibold hover:bg-gray-50 transition border border-gray-300 flex items-center justify-center gap-2"
                >
                  <Share2 className="w-4 h-4" />
                  Share
                </button>
                <button
                  className="bg-white text-gray-700 py-3 px-4 rounded-lg font-semibold hover:bg-gray-50 transition border border-gray-300 flex items-center justify-center gap-2"
                >
                  <Heart className="w-4 h-4" />
                  Like
                </button>
              </div>
            </div>

            {/* Categories */}
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Categories</h3>
              <div className="flex flex-wrap gap-2">
                {recipe.categories.map((category) => (
                  <span 
                    key={category}
                    className="px-3 py-1 bg-white text-purple-700 rounded-full text-sm font-medium border border-purple-200"
                  >
                    {category}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Comments Section - Full Width */}
      <div className="mt-8">
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
              💬 Comments
              <span className="text-sm font-normal text-gray-500">({commentsCount})</span>
            </h2>

            {/* Comment Input */}
            {isAuthenticated ? (
              <form onSubmit={handleSubmitComment} className="mb-8">
                <div className="flex gap-3">
                  <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-semibold flex-shrink-0">
                    {user?.username?.charAt(0).toUpperCase() || 'U'}
                  </div>
                  <div className="flex-1">
                    <textarea
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      placeholder="Share your thoughts about this recipe..."
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
                      rows={3}
                      disabled={isSubmittingComment}
                    />
                    <div className="flex justify-between items-center mt-2">
                      <span className="text-xs text-gray-500">💡 Earn +2 XP for commenting!</span>
                      <button
                        type="submit"
                        disabled={isSubmittingComment || !comment.trim()}
                        className="px-6 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition flex items-center gap-2"
                      >
                        <Send className="w-4 h-4" />
                        {isSubmittingComment ? 'Posting...' : 'Post'}
                      </button>
                    </div>
                  </div>
                </div>
              </form>
            ) : (
              <div className="mb-8 p-4 bg-gray-50 rounded-lg border border-gray-200 text-center">
                <p className="text-gray-600">
                  Please{' '}
                  <button onClick={() => navigate('/login')} className="text-orange-600 hover:underline font-medium">
                    login
                  </button>
                  {' '}to leave a comment
                </p>
              </div>
            )}

            {/* Comments List */}
            {isLoadingComments ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
              </div>
            ) : comments && comments.length > 0 ? (
              <div className="space-y-4">
                {comments.map((cmt) => (
                  <div key={cmt.id} className="border-b border-gray-200 pb-4 last:border-0">
                    <div className="flex gap-3">
                      <div className="w-10 h-10 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-semibold flex-shrink-0">
                        {cmt.author.username.charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-1">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-gray-900">{cmt.author.username}</span>
                            <span className="text-xs text-gray-500">Level {cmt.author.level}</span>
                            <span className="text-xs text-gray-400">•</span>
                            <span className="text-xs text-gray-500">
                              {new Date(cmt.created_at).toLocaleDateString()}
                            </span>
                          </div>
                          {isAuthenticated && user?.id === cmt.author.id && (
                            <div className="flex items-center gap-2">
                              <button
                                onClick={() => {
                                  setEditingCommentId(cmt.id);
                                  setEditContent(cmt.content);
                                }}
                                className="text-gray-400 hover:text-orange-600 transition"
                              >
                                <Edit2 className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteComment(cmt.id)}
                                className="text-gray-400 hover:text-red-600 transition"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          )}
                        </div>
                        
                        {editingCommentId === cmt.id ? (
                          <div className="mt-2">
                            <textarea
                              value={editContent}
                              onChange={(e) => setEditContent(e.target.value)}
                              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent resize-none"
                              rows={2}
                            />
                            <div className="flex gap-2 mt-2">
                              <button
                                onClick={() => handleEditComment(cmt.id)}
                                className="px-3 py-1 bg-orange-600 text-white rounded text-sm hover:bg-orange-700"
                              >
                                Save
                              </button>
                              <button
                                onClick={() => {
                                  setEditingCommentId(null);
                                  setEditContent('');
                                }}
                                className="px-3 py-1 bg-gray-200 text-gray-700 rounded text-sm hover:bg-gray-300"
                              >
                                Cancel
                              </button>
                            </div>
                          </div>
                        ) : (
                          <p className="text-gray-700">{cmt.content}</p>
                        )}
                        
                        <div className="flex items-center gap-4 mt-2">
                          <button
                            onClick={() => handleLikeComment(cmt.id)}
                            className={`flex items-center gap-1 text-sm transition ${
                              cmt.is_liked 
                                ? 'text-orange-600 font-medium' 
                                : 'text-gray-500 hover:text-orange-600'
                            }`}
                          >
                            <ThumbsUp className={`w-4 h-4 ${cmt.is_liked ? 'fill-orange-600' : ''}`} />
                            <span>{cmt.likes_count}</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>No comments yet. Be the first to share your experience!</p>
              </div>
            )}
          </div>
        </div>
    </div>
  );
};

export default RecipeDetailPage;
