import { useState } from 'react';
import { FaFilter, FaTimes, FaDumbbell, FaStar, FaUser } from 'react-icons/fa';

const FilterPanel = ({ onFilterChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filters, setFilters] = useState({
    workoutType: '',
    minRating: 0,
    level: '',
    timeSlot: '',
  });

  const workoutTypes = [
    'All Types',
    'Cardio',
    'Strength',
    'CrossFit',
    'Yoga',
    'Pilates',
    'Powerlifting',
    'Bodybuilding',
    'HIIT',
    'Functional',
    'Calisthenics',
  ];

  const levels = ['All Levels', 'Începător', 'Intermediar', 'Avansat', 'Sportiv', 'Expert', 'Veteran'];

  const timeSlots = [
    'All Times',
    'Morning (06:00 - 12:00)',
    'Afternoon (12:00 - 18:00)',
    'Evening (18:00 - 22:00)',
  ];

  const handleFilterChange = (key, value) => {
    const newFilters = {
      ...filters,
      [key]: value === filters[key] ? '' : value,
    };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    const emptyFilters = {
      workoutType: '',
      minRating: 0,
      level: '',
      timeSlot: '',
    };
    setFilters(emptyFilters);
    onFilterChange(emptyFilters);
  };

  const hasActiveFilters = filters.workoutType || filters.minRating > 0 || filters.level || filters.timeSlot;

  return (
    <>
      {/* Filter Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed top-24 right-4 z-[1001] bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-full shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all flex items-center space-x-2 ${
          hasActiveFilters ? 'animate-pulse' : ''
        }`}
      >
        <FaFilter />
        <span className="font-semibold">Filters</span>
        {hasActiveFilters && (
          <span className="bg-yellow-400 text-purple-900 px-2 py-0.5 rounded-full text-xs font-bold">
            Active
          </span>
        )}
      </button>

      {/* Filter Panel */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-[1002] flex items-start justify-end p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md mt-20 mr-4 max-h-[80vh] overflow-y-auto">
            {/* Header */}
            <div className="sticky top-0 bg-gradient-to-r from-purple-600 to-pink-600 p-6 rounded-t-2xl">
              <div className="flex justify-between items-center">
                <div className="flex items-center space-x-3">
                  <FaFilter className="text-2xl text-white" />
                  <h2 className="text-2xl font-bold text-white">Filter Sessions</h2>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-full transition-all"
                >
                  <FaTimes className="text-xl" />
                </button>
              </div>
              {hasActiveFilters && (
                <button
                  onClick={clearFilters}
                  className="mt-3 bg-white text-purple-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-gray-100 transition-all"
                >
                  Clear All Filters
                </button>
              )}
            </div>

            {/* Filter Content */}
            <div className="p-6 space-y-6">
              {/* Workout Type */}
              <div>
                <div className="flex items-center space-x-2 mb-3">
                  <FaDumbbell className="text-purple-600" />
                  <label className="font-semibold text-gray-800">Workout Type</label>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {workoutTypes.map((type) => (
                    <button
                      key={type}
                      onClick={() =>
                        handleFilterChange('workoutType', type === 'All Types' ? '' : type)
                      }
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        (type === 'All Types' && !filters.workoutType) ||
                        filters.workoutType === type
                          ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* Fitness Level */}
              <div>
                <div className="flex items-center space-x-2 mb-3">
                  <FaUser className="text-purple-600" />
                  <label className="font-semibold text-gray-800">Fitness Level</label>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {levels.map((level) => (
                    <button
                      key={level}
                      onClick={() =>
                        handleFilterChange('level', level === 'All Levels' ? '' : level)
                      }
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                        (level === 'All Levels' && !filters.level) || filters.level === level
                          ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {level}
                    </button>
                  ))}
                </div>
              </div>

              {/* Minimum Rating */}
              <div>
                <div className="flex items-center space-x-2 mb-3">
                  <FaStar className="text-yellow-500" />
                  <label className="font-semibold text-gray-800">Minimum Rating</label>
                </div>
                <div className="flex items-center space-x-2">
                  {[0, 3, 3.5, 4, 4.5, 5].map((rating) => (
                    <button
                      key={rating}
                      onClick={() => handleFilterChange('minRating', rating)}
                      className={`flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                        filters.minRating === rating
                          ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white shadow-lg'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {rating === 0 ? 'Any' : `${rating}+`}
                    </button>
                  ))}
                </div>
              </div>

              {/* Time Slot */}
              <div>
                <div className="flex items-center space-x-2 mb-3">
                  <span className="text-purple-600 text-lg">🕐</span>
                  <label className="font-semibold text-gray-800">Time Slot</label>
                </div>
                <div className="space-y-2">
                  {timeSlots.map((slot) => (
                    <button
                      key={slot}
                      onClick={() =>
                        handleFilterChange('timeSlot', slot === 'All Times' ? '' : slot)
                      }
                      className={`w-full px-4 py-3 rounded-lg text-sm font-medium transition-all text-left ${
                        (slot === 'All Times' && !filters.timeSlot) ||
                        filters.timeSlot === slot
                          ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {slot}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default FilterPanel;
