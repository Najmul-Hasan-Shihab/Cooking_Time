import { useForm, useFieldArray } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { Plus, Trash2, ImagePlus } from 'lucide-react';
import toast from 'react-hot-toast';
import { recipeService } from '../services/recipes';

interface IngredientInput {
  name: string;
  quantity: string;
  unit: string;
  optional: boolean;
}

interface StepInput {
  step_number: number;
  text: string;
  image?: string;
  step_time?: number;
}

interface RecipeFormData {
  title: string;
  description: string;
  images: string[];
  imageInput: string;
  ingredients: IngredientInput[];
  steps: StepInput[];
  prep_time: number;
  cook_time: number;
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
  tags: string;
  categories: string;
  cuisine: string;
}

const CreateRecipePage = () => {
  const navigate = useNavigate();
  const { register, control, handleSubmit, watch, setValue, formState: { errors, isSubmitting } } = useForm<RecipeFormData>({
    defaultValues: {
      title: '',
      description: '',
      images: [],
      imageInput: '',
      ingredients: [{ name: '', quantity: '', unit: '', optional: false }],
      steps: [{ step_number: 1, text: '', image: '', step_time: undefined }],
      prep_time: 0,
      cook_time: 0,
      servings: 4,
      difficulty: 'medium',
      tags: '',
      categories: '',
      cuisine: '',
    }
  });

  const { fields: ingredientFields, append: appendIngredient, remove: removeIngredient } = useFieldArray({
    control,
    name: 'ingredients'
  });

  const { fields: stepFields, append: appendStep, remove: removeStep } = useFieldArray({
    control,
    name: 'steps'
  });

  const images = watch('images');
  const imageInput = watch('imageInput');

  const handleAddImage = () => {
    if (imageInput.trim()) {
      const currentImages = images || [];
      setValue('images', [...currentImages, imageInput.trim()]);
      setValue('imageInput', '');
      toast.success('Image added!');
    }
  };

  const handleRemoveImage = (index: number) => {
    const currentImages = images || [];
    setValue('images', currentImages.filter((_, i) => i !== index));
    toast.success('Image removed');
  };

  const onSubmit = async (data: RecipeFormData) => {
    try {
      // Process tags and categories
      const tags = data.tags.split(',').map(t => t.trim()).filter(t => t);
      const categories = data.categories.split(',').map(c => c.trim()).filter(c => c);

      // Prepare recipe data
      const recipeData = {
        title: data.title,
        description: data.description,
        images: data.images,
        ingredients: data.ingredients.filter(ing => ing.name && ing.quantity),
        steps: data.steps.map((step, index) => ({
          ...step,
          step_number: index + 1,
        })).filter(step => step.text),
        prep_time: Number(data.prep_time),
        cook_time: Number(data.cook_time),
        servings: Number(data.servings),
        difficulty: data.difficulty,
        tags,
        categories,
        cuisine: data.cuisine,
      };

      // Submit to API
      const response = await recipeService.createRecipe(recipeData);
      
      toast.success('Recipe created successfully! 🎉');
      navigate(`/recipes/${response.slug}`);
    } catch (error: any) {
      console.error('Error creating recipe:', error);
      toast.error(error.response?.data?.message || 'Failed to create recipe');
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Create New Recipe</h1>
        <p className="text-gray-600">Share your culinary masterpiece with the community! 👨‍🍳</p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {/* Basic Information */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">📝 Basic Information</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Recipe Title <span className="text-red-500">*</span>
              </label>
              <input
                {...register('title', { required: 'Title is required' })}
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="e.g., Grandma's Chocolate Chip Cookies"
              />
              {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description <span className="text-red-500">*</span>
              </label>
              <textarea
                {...register('description', { required: 'Description is required' })}
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Tell us about your recipe... What makes it special?"
              />
              {errors.description && <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Prep Time (min) <span className="text-red-500">*</span>
                </label>
                <input
                  {...register('prep_time', { required: 'Prep time is required', min: 0 })}
                  type="number"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
                {errors.prep_time && <p className="mt-1 text-sm text-red-600">{errors.prep_time.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cook Time (min) <span className="text-red-500">*</span>
                </label>
                <input
                  {...register('cook_time', { required: 'Cook time is required', min: 0 })}
                  type="number"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
                {errors.cook_time && <p className="mt-1 text-sm text-red-600">{errors.cook_time.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Servings <span className="text-red-500">*</span>
                </label>
                <input
                  {...register('servings', { required: 'Servings is required', min: 1 })}
                  type="number"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                />
                {errors.servings && <p className="mt-1 text-sm text-red-600">{errors.servings.message}</p>}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Difficulty <span className="text-red-500">*</span>
              </label>
              <select
                {...register('difficulty')}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value="easy">Easy 🟢</option>
                <option value="medium">Medium 🟡</option>
                <option value="hard">Hard 🔴</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Cuisine
                </label>
                <input
                  {...register('cuisine')}
                  type="text"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="e.g., Italian, Chinese, Mexican"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tags (comma-separated)
                </label>
                <input
                  {...register('tags')}
                  type="text"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="e.g., dessert, chocolate, holiday"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Categories (comma-separated)
              </label>
              <input
                {...register('categories')}
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="e.g., Breakfast, Main Course, Dessert"
              />
            </div>
          </div>
        </div>

        {/* Images */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">📸 Images</h2>
          
          <div className="space-y-4">
            <div className="flex gap-2">
              <input
                {...register('imageInput')}
                type="url"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Enter image URL"
              />
              <button
                type="button"
                onClick={handleAddImage}
                className="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition flex items-center gap-2"
              >
                <ImagePlus className="w-4 h-4" />
                Add
              </button>
            </div>

            {images && images.length > 0 && (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {images.map((image, index) => (
                  <div key={index} className="relative group">
                    <img 
                      src={image} 
                      alt={`Recipe ${index + 1}`}
                      className="w-full h-32 object-cover rounded-lg border border-gray-200"
                      onError={(e) => {
                        e.currentTarget.src = 'https://via.placeholder.com/200x200?text=Invalid+URL';
                      }}
                    />
                    <button
                      type="button"
                      onClick={() => handleRemoveImage(index)}
                      className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Ingredients */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">🥘 Ingredients</h2>
          
          <div className="space-y-3">
            {ingredientFields.map((field, index) => (
              <div key={field.id} className="flex gap-2 items-start">
                <div className="flex-1 grid grid-cols-12 gap-2">
                  <input
                    {...register(`ingredients.${index}.quantity` as const)}
                    type="text"
                    placeholder="1"
                    className="col-span-2 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                  <input
                    {...register(`ingredients.${index}.unit` as const)}
                    type="text"
                    placeholder="cup"
                    className="col-span-2 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                  <input
                    {...register(`ingredients.${index}.name` as const)}
                    type="text"
                    placeholder="Ingredient name"
                    className="col-span-6 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                  <label className="col-span-2 flex items-center gap-2 text-sm text-gray-600">
                    <input
                      {...register(`ingredients.${index}.optional` as const)}
                      type="checkbox"
                      className="w-4 h-4 text-orange-600 rounded focus:ring-orange-500"
                    />
                    Optional
                  </label>
                </div>
                {ingredientFields.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeIngredient(index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={() => appendIngredient({ name: '', quantity: '', unit: '', optional: false })}
            className="mt-4 w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-orange-500 hover:text-orange-600 transition flex items-center justify-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Add Ingredient
          </button>
        </div>

        {/* Steps */}
        <div className="bg-white rounded-xl border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">👨‍🍳 Instructions</h2>
          
          <div className="space-y-4">
            {stepFields.map((field, index) => (
              <div key={field.id} className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 bg-orange-600 text-white rounded-full flex items-center justify-center font-bold">
                  {index + 1}
                </div>
                <div className="flex-1 space-y-2">
                  <textarea
                    {...register(`steps.${index}.text` as const)}
                    rows={3}
                    placeholder="Describe this step in detail..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                  <div className="grid grid-cols-2 gap-2">
                    <input
                      {...register(`steps.${index}.image` as const)}
                      type="url"
                      placeholder="Step image URL (optional)"
                      className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm"
                    />
                    <input
                      {...register(`steps.${index}.step_time` as const)}
                      type="number"
                      placeholder="Time (min)"
                      className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent text-sm"
                    />
                  </div>
                </div>
                {stepFields.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeStep(index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition h-fit"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={() => appendStep({ step_number: stepFields.length + 1, text: '', image: '', step_time: undefined })}
            className="mt-4 w-full py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-orange-500 hover:text-orange-600 transition flex items-center justify-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Add Step
          </button>
        </div>

        {/* Submit Buttons */}
        <div className="flex gap-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex-1 bg-orange-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-orange-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Creating...' : 'Create Recipe 🎉'}
          </button>
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateRecipePage;
