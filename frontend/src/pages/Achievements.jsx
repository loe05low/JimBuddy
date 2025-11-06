import { useEffect, useState } from 'react';
import { achievementAPI } from '../services/api';
import { FaTrophy, FaLock, FaStar } from 'react-icons/fa';

const Achievements = () => {
  const [achievements, setAchievements] = useState([]);
  const [stats, setStats] = useState({ total: 0, unlocked: 0, in_progress: 0, total_xp: 0 });
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, unlocked, locked

  useEffect(() => {
    fetchAchievements();
  }, []);

  const fetchAchievements = async () => {
    try {
      const response = await achievementAPI.getMyAchievements();
      setAchievements(response.data.achievements || []);
      setStats(response.data.stats || { total: 0, unlocked: 0, in_progress: 0, total_xp: 0 });
    } catch (err) {
      console.error('Error fetching achievements:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckAchievements = async () => {
    try {
      const response = await achievementAPI.checkAchievements();
      if (response.data.achievements && response.data.achievements.length > 0) {
        alert(`🎉 ${response.data.message}`);
        fetchAchievements(); // Refresh to show new unlocks
      } else {
        alert('No new achievements unlocked. Keep working out! 💪');
      }
    } catch (err) {
      console.error('Error checking achievements:', err);
      alert('Failed to check achievements.');
    }
  };

  const getRarityColor = (rarity) => {
    switch (rarity) {
      case 'common':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      case 'rare':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'epic':
        return 'bg-purple-100 text-purple-800 border-purple-300';
      case 'legendary':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const filteredAchievements = achievements.filter((achievement) => {
    if (filter === 'unlocked') return achievement.is_unlocked;
    if (filter === 'locked') return !achievement.is_unlocked;
    return true;
  });

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary border-solid mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading achievements...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2 flex items-center space-x-3">
            <FaTrophy className="text-yellow-500" />
            <span>Achievements</span>
          </h1>
          <p className="text-gray-600 dark:text-gray-300">Track your progress and unlock rewards!</p>
        </div>
        <button
          onClick={handleCheckAchievements}
          className="bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white px-6 py-3 rounded-lg flex items-center space-x-2 font-semibold transition shadow-lg"
        >
          <FaTrophy />
          <span>Check Progress</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl shadow-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-100 text-sm font-medium">Total XP</p>
              <p className="text-4xl font-black mt-2">{stats.total_xp}</p>
            </div>
            <FaStar className="text-5xl text-yellow-200 opacity-50" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-400 to-green-600 rounded-2xl shadow-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">Unlocked</p>
              <p className="text-4xl font-black mt-2">{stats.unlocked}</p>
              <p className="text-green-100 text-xs mt-1">of {stats.total}</p>
            </div>
            <FaTrophy className="text-5xl text-green-200 opacity-50" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl shadow-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">In Progress</p>
              <p className="text-4xl font-black mt-2">{stats.in_progress}</p>
            </div>
            <div className="text-5xl">�</div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl shadow-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm font-medium">Completion</p>
              <p className="text-4xl font-black mt-2">
                {stats.total > 0 ? Math.round((stats.unlocked / stats.total) * 100) : 0}%
              </p>
            </div>
            <div className="text-5xl">=�</div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex space-x-2 mb-6">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            filter === 'all'
              ? 'bg-primary text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All ({achievements.length})
        </button>
        <button
          onClick={() => setFilter('unlocked')}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            filter === 'unlocked'
              ? 'bg-primary text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Unlocked ({stats.unlocked})
        </button>
        <button
          onClick={() => setFilter('locked')}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            filter === 'locked'
              ? 'bg-primary text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Locked ({achievements.length - stats.unlocked})
        </button>
      </div>

      {/* Achievements Grid */}
      {filteredAchievements.length === 0 ? (
        <div className="card text-center text-gray-500 py-12">
          <FaTrophy className="text-6xl text-gray-300 mx-auto mb-4" />
          <p className="text-lg">No achievements found</p>
          <p className="text-sm mt-2">Keep working out to unlock achievements!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAchievements.map((achievement) => (
            <div
              key={achievement.id}
              className={`card relative overflow-hidden transition-all hover:shadow-xl ${
                achievement.is_unlocked ? 'border-2 border-yellow-400' : 'opacity-75'
              }`}
            >
              {/* Rarity Badge */}
              <div className="absolute top-4 right-4">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${getRarityColor(
                    achievement.achievement?.rarity || 'common'
                  )}`}
                >
                  {(achievement.achievement?.rarity || 'common').toUpperCase()}
                </span>
              </div>

              {/* Icon */}
              <div className="flex justify-center mb-4">
                <div
                  className={`w-20 h-20 rounded-full flex items-center justify-center text-4xl ${
                    achievement.is_unlocked
                      ? 'bg-gradient-to-br from-yellow-400 to-orange-500 shadow-lg'
                      : 'bg-gray-200'
                  }`}
                >
                  {achievement.is_unlocked ? (
                    achievement.achievement_icon
                  ) : (
                    <FaLock className="text-gray-500 text-2xl" />
                  )}
                </div>
              </div>

              {/* Details */}
              <div className="text-center mb-4">
                <h3 className="font-bold text-lg mb-1">{achievement.achievement_name}</h3>
                <p className="text-sm text-gray-600 mb-3">{achievement.achievement_description}</p>

                {/* XP Reward */}
                <div className="flex items-center justify-center space-x-2 text-yellow-600">
                  <FaStar />
                  <span className="font-bold">{achievement.xp_reward} XP</span>
                </div>
              </div>

              {/* Progress Bar */}
              {!achievement.is_unlocked && achievement.progress > 0 && (
                <div className="mt-4">
                  <div className="flex justify-between text-xs text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>
                      {achievement.progress}/{achievement.required_count}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full transition-all"
                      style={{
                        width: `${Math.min(
                          100,
                          (achievement.progress / achievement.required_count) * 100
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              )}

              {/* Unlocked Badge */}
              {achievement.is_unlocked && achievement.unlocked_at && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <p className="text-xs text-center text-green-600 font-semibold">
                     Unlocked on {new Date(achievement.unlocked_at).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Achievements;
