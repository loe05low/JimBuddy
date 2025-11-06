import { useEffect, useState } from 'react';
import { socialAPI } from '../services/api';
import { FaUsers, FaUserPlus, FaStar, FaDumbbell } from 'react-icons/fa';
import FollowButton from '../components/FollowButton';
import { Link } from 'react-router-dom';

const Friends = () => {
  const [followers, setFollowers] = useState([]);
  const [following, setFollowing] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [activeTab, setActiveTab] = useState('followers');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      const [followersRes, followingRes, suggestionsRes] = await Promise.all([
        socialAPI.getFollowers(),
        socialAPI.getFollowing(),
        socialAPI.getSuggestions(),
      ]);

      setFollowers(followersRes.data.followers || []);
      setFollowing(followingRes.data.following || []);
      setSuggestions(suggestionsRes.data.suggestions || []);
    } catch (err) {
      console.error('Error fetching friends data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFollowChange = () => {
    // Refresh data after follow/unfollow
    fetchAllData();
  };

  const UserCard = ({ user, showFollowButton = false, isFollowing = false }) => (
    <div className="card hover:shadow-lg transition-all">
      <div className="flex items-center justify-between">
        <Link to={`/profile/${user.id}`} className="flex items-center space-x-4 flex-1">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-600 via-pink-600 to-red-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
            {user.nume?.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1">
            <h3 className="font-bold text-lg text-gray-800 dark:text-white hover:text-primary transition">
              {user.nume}
            </h3>
            <div className="flex items-center space-x-3 mt-1">
              <span className="badge-info text-xs">{user.grad}</span>
              <span className="flex items-center space-x-1 text-yellow-600 text-sm">
                <FaStar />
                <span className="font-semibold">{user.rating}</span>
              </span>
              <span className="flex items-center space-x-1 text-purple-600 text-sm">
                <FaDumbbell />
                <span className="font-semibold">{user.nr_antrenamente}</span>
              </span>
            </div>
          </div>
        </Link>
        {showFollowButton && (
          <FollowButton
            userId={user.id}
            initialFollowing={isFollowing}
            onFollowChange={handleFollowChange}
          />
        )}
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary border-solid mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading friends...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-2 flex items-center space-x-3">
          <FaUsers className="text-primary" />
          <span>Friends</span>
        </h1>
        <p className="text-gray-600 dark:text-gray-300">Connect with your gym buddies!</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-400 to-blue-600 rounded-2xl shadow-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">Followers</p>
              <p className="text-4xl font-black mt-2">{followers.length}</p>
            </div>
            <FaUsers className="text-5xl text-blue-200 opacity-50" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-400 to-purple-600 rounded-2xl shadow-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm font-medium">Following</p>
              <p className="text-4xl font-black mt-2">{following.length}</p>
            </div>
            <FaUserPlus className="text-5xl text-purple-200 opacity-50" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-pink-400 to-pink-600 rounded-2xl shadow-xl p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-pink-100 text-sm font-medium">Suggestions</p>
              <p className="text-4xl font-black mt-2">{suggestions.length}</p>
            </div>
            <div className="text-5xl">=¡</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-6">
        <div className="flex space-x-2 border-b">
          <button
            onClick={() => setActiveTab('followers')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'followers'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 dark:text-gray-400 hover:text-primary'
            }`}
          >
            Followers ({followers.length})
          </button>
          <button
            onClick={() => setActiveTab('following')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'following'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 dark:text-gray-400 hover:text-primary'
            }`}
          >
            Following ({following.length})
          </button>
          <button
            onClick={() => setActiveTab('suggestions')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'suggestions'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 dark:text-gray-400 hover:text-primary'
            }`}
          >
            Suggestions ({suggestions.length})
          </button>
        </div>
      </div>

      {/* Followers Tab */}
      {activeTab === 'followers' && (
        <div>
          {followers.length === 0 ? (
            <div className="card text-center text-gray-500 py-12">
              <FaUsers className="text-6xl text-gray-300 mx-auto mb-4" />
              <p className="text-lg">No followers yet</p>
              <p className="text-sm mt-2">Share your profile to get more followers!</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {followers.map((item) => (
                <UserCard
                  key={item.follower.id}
                  user={item.follower}
                  showFollowButton={true}
                  isFollowing={false}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Following Tab */}
      {activeTab === 'following' && (
        <div>
          {following.length === 0 ? (
            <div className="card text-center text-gray-500 py-12">
              <FaUserPlus className="text-6xl text-gray-300 mx-auto mb-4" />
              <p className="text-lg">Not following anyone yet</p>
              <p className="text-sm mt-2">Check out the suggestions tab to find people!</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {following.map((item) => (
                <UserCard
                  key={item.following.id}
                  user={item.following}
                  showFollowButton={true}
                  isFollowing={true}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Suggestions Tab */}
      {activeTab === 'suggestions' && (
        <div>
          <div className="bg-blue-50 dark:bg-blue-900 border border-blue-200 dark:border-blue-700 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-800 dark:text-blue-200">
              =¡ <strong>Friend Suggestions:</strong> Based on your fitness level and interests
            </p>
          </div>

          {suggestions.length === 0 ? (
            <div className="card text-center text-gray-500 py-12">
              <div className="text-6xl mx-auto mb-4"><¯</div>
              <p className="text-lg">No suggestions available</p>
              <p className="text-sm mt-2">We'll find the perfect gym buddies for you soon!</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {suggestions.map((user) => (
                <UserCard
                  key={user.id}
                  user={user}
                  showFollowButton={true}
                  isFollowing={false}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Friends;
