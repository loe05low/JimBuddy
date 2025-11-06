import { useEffect, useState } from 'react';
import { socialAPI } from '../services/api';
import { FaFire, FaStar, FaTrophy, FaDumbbell, FaLevelUpAlt, FaUsers } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const ActivityFeed = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchActivityFeed();
  }, []);

  const fetchActivityFeed = async () => {
    try {
      const response = await socialAPI.getActivityFeed();
      setActivities(response.data.activities || []);
    } catch (err) {
      console.error('Error fetching activity feed:', err);
    } finally {
      setLoading(false);
    }
  };

  const getActivityIcon = (activityType) => {
    switch (activityType) {
      case 'workout_completed':
        return <FaDumbbell className="text-purple-600" />;
      case 'rating_given':
        return <FaStar className="text-yellow-500" />;
      case 'achievement_unlocked':
        return <FaTrophy className="text-yellow-600" />;
      case 'session_created':
        return <FaUsers className="text-blue-600" />;
      case 'level_up':
        return <FaLevelUpAlt className="text-green-600" />;
      default:
        return <FaFire className="text-orange-500" />;
    }
  };

  const getActivityColor = (activityType) => {
    switch (activityType) {
      case 'workout_completed':
        return 'bg-purple-50 border-purple-200';
      case 'rating_given':
        return 'bg-yellow-50 border-yellow-200';
      case 'achievement_unlocked':
        return 'bg-yellow-50 border-yellow-300';
      case 'session_created':
        return 'bg-blue-50 border-blue-200';
      case 'level_up':
        return 'bg-green-50 border-green-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);

    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`;
    return date.toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary border-solid mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading activity feed...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2 flex items-center space-x-3">
          <FaFire className="text-orange-500" />
          <span>Activity Feed</span>
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          See what your friends are up to!
        </p>
      </div>

      {/* Activity Feed */}
      {activities.length === 0 ? (
        <div className="card text-center text-gray-500 py-12">
          <FaFire className="text-6xl text-gray-300 mx-auto mb-4" />
          <p className="text-lg">No activities yet</p>
          <p className="text-sm mt-2">
            Follow some friends to see their workout activities here!
          </p>
          <Link
            to="/friends"
            className="mt-4 inline-block bg-primary hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition"
          >
            Find Friends
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {activities.map((activity) => (
            <div
              key={activity.id}
              className={`card border-l-4 ${getActivityColor(activity.activity_type)} transition-all hover:shadow-lg`}
            >
              <div className="flex items-start space-x-4">
                {/* User Avatar */}
                <Link to={`/profile/${activity.user_details.id}`}>
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-600 via-pink-600 to-red-600 rounded-full flex items-center justify-center text-white font-bold shadow-md hover:scale-105 transition-transform">
                    {activity.user_details.nume.charAt(0).toUpperCase()}
                  </div>
                </Link>

                {/* Activity Content */}
                <div className="flex-1">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <Link
                        to={`/profile/${activity.user_details.id}`}
                        className="font-bold text-gray-800 dark:text-white hover:text-primary transition"
                      >
                        {activity.user_details.nume}
                      </Link>
                      <p className="text-gray-700 dark:text-gray-300 mt-1">
                        {activity.description}
                      </p>
                      {activity.related_user_details && (
                        <Link
                          to={`/profile/${activity.related_user_details.id}`}
                          className="text-primary hover:underline text-sm mt-1 inline-block"
                        >
                          @{activity.related_user_details.nume}
                        </Link>
                      )}
                    </div>

                    {/* Activity Icon */}
                    <div className="ml-4 text-2xl">
                      {getActivityIcon(activity.activity_type)}
                    </div>
                  </div>

                  {/* Timestamp */}
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                    {formatTimeAgo(activity.created_at)}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Load More Button (if needed) */}
      {activities.length >= 50 && (
        <div className="mt-6 text-center">
          <button
            onClick={fetchActivityFeed}
            className="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-6 py-2 rounded-lg font-semibold transition"
          >
            Load More
          </button>
        </div>
      )}
    </div>
  );
};

export default ActivityFeed;
