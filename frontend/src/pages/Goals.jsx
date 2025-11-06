import { useEffect, useState } from 'react';
import { goalAPI } from '../services/api';
import { FaTarget, FaPlus, FaTimes, FaCheck, FaFire, FaArrowUp } from 'react-icons/fa';

const Goals = () => {
  const [activeGoals, setActiveGoals] = useState([]);
  const [completedGoals, setCompletedGoals] = useState([]);
  const [goalTemplates, setGoalTemplates] = useState([]);
  const [stats, setStats] = useState({ total: 0, active: 0, completed: 0, failed: 0, completion_rate: 0 });
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [activeTab, setActiveTab] = useState('active'); // active, completed

  useEffect(() => {
    fetchGoals();
    fetchGoalTemplates();
    fetchStats();
  }, []);

  const fetchGoals = async () => {
    try {
      const [activeRes, completedRes] = await Promise.all([
        goalAPI.getActiveGoals(),
        goalAPI.getCompletedGoals(),
      ]);
      setActiveGoals(activeRes.data.goals || []);
      setCompletedGoals(completedRes.data.goals || []);
    } catch (err) {
      console.error('Error fetching goals:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchGoalTemplates = async () => {
    try {
      const response = await goalAPI.getAll();
      setGoalTemplates(response.data.results || response.data);
    } catch (err) {
      console.error('Error fetching goal templates:', err);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await goalAPI.getStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handleCreateGoal = async (goalId) => {
    try {
      await goalAPI.createGoal({ goal_id: goalId });
      setShowCreateModal(false);
      fetchGoals();
      fetchStats();
      alert('Goal created successfully! <�');
    } catch (err) {
      console.error('Error creating goal:', err);
      alert(err.response?.data?.error || 'Failed to create goal. You may already have an active goal of this type.');
    }
  };

  const handleAbandonGoal = async (goalId) => {
    if (!confirm('Are you sure you want to abandon this goal?')) {
      return;
    }

    try {
      await goalAPI.abandonGoal(goalId);
      fetchGoals();
      fetchStats();
      alert('Goal abandoned.');
    } catch (err) {
      console.error('Error abandoning goal:', err);
      alert('Failed to abandon goal.');
    }
  };

  const handleIncrementProgress = async (goalId) => {
    try {
      const response = await goalAPI.incrementProgress(goalId, 1);
      if (response.data.completed) {
        alert('🎉 Goal completed! Congratulations!');
      }
      fetchGoals();
      fetchStats();
    } catch (err) {
      console.error('Error incrementing progress:', err);
      alert('Failed to update progress.');
    }
  };

  const handleUpdateStreak = async (goalId) => {
    try {
      const response = await goalAPI.updateStreak(goalId);
      if (response.data.completed) {
        alert('🎉 Goal completed! You maintained the streak!');
      } else {
        alert(`Streak updated! Current streak: ${response.data.current_streak} days 🔥`);
      }
      fetchGoals();
      fetchStats();
    } catch (err) {
      console.error('Error updating streak:', err);
      alert('Failed to update streak.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary border-solid mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading goals...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center space-x-3">
            <FaTarget className="text-primary" />
            <span>Goals</span>
          </h1>
          <p className="text-gray-600">Set and track your fitness goals!</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-primary hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center space-x-2 font-semibold transition shadow-lg"
        >
          <FaPlus />
          <span>New Goal</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl shadow-xl p-6 text-white">
          <div>
            <p className="text-blue-100 text-sm font-medium">Active Goals</p>
            <p className="text-4xl font-black mt-2">{stats.active}</p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-400 to-green-600 rounded-2xl shadow-xl p-6 text-white">
          <div>
            <p className="text-green-100 text-sm font-medium">Completed</p>
            <p className="text-4xl font-black mt-2">{stats.completed}</p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-red-400 to-red-600 rounded-2xl shadow-xl p-6 text-white">
          <div>
            <p className="text-red-100 text-sm font-medium">Failed</p>
            <p className="text-4xl font-black mt-2">{stats.failed}</p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl shadow-xl p-6 text-white">
          <div>
            <p className="text-purple-100 text-sm font-medium">Success Rate</p>
            <p className="text-4xl font-black mt-2">{stats.completion_rate}%</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-6">
        <div className="flex space-x-2 border-b">
          <button
            onClick={() => setActiveTab('active')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'active'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 hover:text-primary'
            }`}
          >
            Active Goals ({activeGoals.length})
          </button>
          <button
            onClick={() => setActiveTab('completed')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'completed'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 hover:text-primary'
            }`}
          >
            Completed ({completedGoals.length})
          </button>
        </div>
      </div>

      {/* Active Goals */}
      {activeTab === 'active' && (
        <div>
          {activeGoals.length === 0 ? (
            <div className="card text-center text-gray-500 py-12">
              <FaTarget className="text-6xl text-gray-300 mx-auto mb-4" />
              <p className="text-lg">No active goals</p>
              <p className="text-sm mt-2">Click "New Goal" to create your first goal!</p>
            </div>
          ) : (
            <div className="grid gap-6">
              {activeGoals.map((goal) => (
                <div key={goal.id} className="card border-l-4 border-primary">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-3">
                        <span className="text-3xl">{goal.goal_icon}</span>
                        <div>
                          <h3 className="font-bold text-xl">{goal.goal_name}</h3>
                          <p className="text-sm text-gray-600">{goal.goal_description}</p>
                        </div>
                      </div>

                      {/* Progress Bar */}
                      <div className="mb-3">
                        <div className="flex justify-between text-sm text-gray-600 mb-2">
                          <span className="font-semibold">Progress</span>
                          <span>
                            {goal.current_value} / {goal.target_value}
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div
                            className="bg-gradient-to-r from-primary to-secondary h-3 rounded-full transition-all"
                            style={{ width: `${goal.progress_percentage}%` }}
                          />
                        </div>
                        <div className="flex justify-between items-center mt-2">
                          <span className="text-lg font-bold text-primary">{goal.progress_percentage}%</span>
                          <span className="text-sm text-gray-500">
                            Deadline: {new Date(goal.deadline).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="ml-4 flex flex-col space-y-2">
                      {/* Increment Progress Button */}
                      <button
                        onClick={() => handleIncrementProgress(goal.id)}
                        className="bg-primary hover:bg-blue-700 text-white px-3 py-2 rounded-lg flex items-center space-x-2 transition text-sm font-semibold"
                        title="Increment progress"
                      >
                        <FaArrowUp />
                        <span>+1</span>
                      </button>

                      {/* Update Streak Button (only for streak goals) */}
                      {goal.goal_name && goal.goal_name.toLowerCase().includes('streak') && (
                        <button
                          onClick={() => handleUpdateStreak(goal.id)}
                          className="bg-orange-500 hover:bg-orange-600 text-white px-3 py-2 rounded-lg flex items-center space-x-2 transition text-sm font-semibold"
                          title="Update streak"
                        >
                          <FaFire />
                          <span>Streak</span>
                        </button>
                      )}

                      {/* Abandon Button */}
                      <button
                        onClick={() => handleAbandonGoal(goal.id)}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-700 p-2 rounded-lg transition"
                        title="Abandon goal"
                      >
                        <FaTimes />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Completed Goals */}
      {activeTab === 'completed' && (
        <div>
          {completedGoals.length === 0 ? (
            <div className="card text-center text-gray-500 py-12">
              <FaCheck className="text-6xl text-gray-300 mx-auto mb-4" />
              <p className="text-lg">No completed goals yet</p>
              <p className="text-sm mt-2">Complete your active goals to see them here!</p>
            </div>
          ) : (
            <div className="grid gap-6">
              {completedGoals.map((goal) => (
                <div key={goal.id} className="card border-l-4 border-green-500 bg-green-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="text-3xl">{goal.goal_icon}</span>
                        <div>
                          <h3 className="font-bold text-xl">{goal.goal_name}</h3>
                          <p className="text-sm text-gray-600">{goal.goal_description}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4 mt-3">
                        <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold flex items-center space-x-1">
                          <FaCheck />
                          <span>Completed</span>
                        </span>
                        <span className="text-sm text-gray-600">
                          {new Date(goal.completed_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Create Goal Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b flex items-center justify-between sticky top-0 bg-white">
              <h2 className="text-2xl font-bold">Choose a Goal</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600 text-2xl"
              >
                <FaTimes />
              </button>
            </div>

            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {goalTemplates.map((template) => (
                  <div
                    key={template.id}
                    className="card border-2 border-gray-200 hover:border-primary transition cursor-pointer"
                    onClick={() => handleCreateGoal(template.id)}
                  >
                    <div className="flex items-start space-x-3">
                      <span className="text-4xl">{template.icon}</span>
                      <div className="flex-1">
                        <h3 className="font-bold text-lg mb-1">{template.name}</h3>
                        <p className="text-sm text-gray-600 mb-3">{template.description}</p>
                        <div className="flex items-center justify-between">
                          <span className="badge-info text-xs">{template.period}</span>
                          <span className="text-sm font-semibold text-primary">
                            Target: {template.target_value}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {goalTemplates.length === 0 && (
                <div className="text-center text-gray-500 py-12">
                  <p>No goal templates available</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Goals;
