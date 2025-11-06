import { useState, useEffect } from 'react';
import { socialAPI } from '../services/api';
import { FaUserPlus, FaUserCheck } from 'react-icons/fa';

const FollowButton = ({ userId, initialFollowing = false, onFollowChange }) => {
  const [isFollowing, setIsFollowing] = useState(initialFollowing);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check if following on mount
    checkFollowStatus();
  }, [userId]);

  const checkFollowStatus = async () => {
    try {
      const response = await socialAPI.isFollowing(userId);
      setIsFollowing(response.data.is_following);
    } catch (error) {
      console.error('Error checking follow status:', error);
    }
  };

  const handleFollow = async () => {
    setLoading(true);
    try {
      await socialAPI.follow(userId);
      setIsFollowing(true);
      // toast.success('Following! 👥'); // Uncomment after installing react-hot-toast
      if (onFollowChange) onFollowChange(true);
    } catch (error) {
      console.error('Error following user:', error);
      // toast.error('Failed to follow'); // Uncomment after installing react-hot-toast
    } finally {
      setLoading(false);
    }
  };

  const handleUnfollow = async () => {
    setLoading(true);
    try {
      await socialAPI.unfollow(userId);
      setIsFollowing(false);
      // toast.success('Unfollowed'); // Uncomment after installing react-hot-toast
      if (onFollowChange) onFollowChange(false);
    } catch (error) {
      console.error('Error unfollowing user:', error);
      // toast.error('Failed to unfollow'); // Uncomment after installing react-hot-toast
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={isFollowing ? handleUnfollow : handleFollow}
      disabled={loading}
      className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-semibold transition-all disabled:opacity-50 ${
        isFollowing
          ? 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white hover:bg-gray-300 dark:hover:bg-gray-600'
          : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700'
      }`}
    >
      {isFollowing ? (
        <>
          <FaUserCheck />
          <span>{loading ? 'Loading...' : 'Following'}</span>
        </>
      ) : (
        <>
          <FaUserPlus />
          <span>{loading ? 'Loading...' : 'Follow'}</span>
        </>
      )}
    </button>
  );
};

export default FollowButton;
