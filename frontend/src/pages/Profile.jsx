import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { profileAPI, sessionAPI } from '../services/api';
import { FaUser, FaStar, FaDumbbell, FaClock, FaMapMarkerAlt, FaComment, FaCheck, FaTimes } from 'react-icons/fa';
import RequestManager from '../components/RequestManager';

const Profile = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [ratings, setRatings] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [activeTab, setActiveTab] = useState('sessions');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?.profile?.id) {
      fetchProfileData();
    }
  }, [user]);

  const fetchProfileData = async () => {
    try {
      const [profileRes, ratingsRes, sessionsRes] = await Promise.all([
        profileAPI.getMyProfile(),
        profileAPI.getRatings(user.profile.id),
        sessionAPI.getMySessions(),
      ]);

      setProfile(profileRes.data);
      setRatings(ratingsRes.data.ratings || []);
      setSessions(sessionsRes.data.results || sessionsRes.data);
    } catch (err) {
      console.error('Error fetching profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteSession = async (sessionId) => {
    if (!confirm('Mark this session as completed? This will update your workout count.')) {
      return;
    }

    try {
      await sessionAPI.complete(sessionId);
      // Refresh data
      fetchProfileData();
      alert('Session completed! 💪');
    } catch (err) {
      console.error('Error completing session:', err);
      alert('Failed to complete session. Please try again.');
    }
  };

  const handleCancelSession = async (sessionId) => {
    if (!confirm('Are you sure you want to cancel this session?')) {
      return;
    }

    try {
      await sessionAPI.cancel(sessionId);
      // Refresh data
      fetchProfileData();
      alert('Session cancelled.');
    } catch (err) {
      console.error('Error cancelling session:', err);
      alert('Failed to cancel session. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary border-solid mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Profile Header */}
      <div className="card mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div className="w-24 h-24 bg-gradient-to-br from-purple-600 via-pink-600 to-red-600 rounded-full flex items-center justify-center text-white text-4xl font-bold shadow-lg">
              {profile?.nume.charAt(0).toUpperCase()}
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">{profile?.nume}</h1>
              <p className="text-gray-600 mt-1">@{user?.username}</p>
              <div className="flex items-center space-x-3 mt-2">
                <span className="badge-info">{profile?.grad}</span>
                <span className="badge-success flex items-center space-x-1">
                  <FaStar />
                  <span>{profile?.rating} Rating</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Progress Tracking Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Total Workouts */}
        <div className="bg-gradient-to-br from-purple-500 to-purple-700 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-all">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-200 text-sm font-medium">Total Workouts</p>
              <p className="text-5xl font-black mt-2">{profile?.nr_antrenamente}</p>
              <p className="text-purple-200 text-xs mt-2">Sessions completed</p>
            </div>
            <FaDumbbell className="text-6xl text-purple-300 opacity-50" />
          </div>
        </div>

        {/* Average Rating */}
        <div className="bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-all">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-100 text-sm font-medium">Average Rating</p>
              <div className="flex items-center space-x-2 mt-2">
                <p className="text-5xl font-black">{profile?.rating}</p>
                <FaStar className="text-3xl text-yellow-200" />
              </div>
              <p className="text-yellow-100 text-xs mt-2">Out of 5.0 stars</p>
            </div>
          </div>
        </div>

        {/* Fitness Level */}
        <div className="bg-gradient-to-br from-pink-500 to-red-600 rounded-2xl shadow-xl p-6 text-white transform hover:scale-105 transition-all">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-pink-200 text-sm font-medium">Fitness Level</p>
              <p className="text-3xl font-black mt-2">{profile?.grad}</p>
              <p className="text-pink-200 text-xs mt-2">Keep pushing forward!</p>
            </div>
            <div className="text-5xl">💪</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-6">
        <div className="flex space-x-2 border-b">
          <button
            onClick={() => setActiveTab('sessions')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'sessions'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 hover:text-primary'
            }`}
          >
            My Sessions
          </button>
          <button
            onClick={() => setActiveTab('requests')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'requests'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 hover:text-primary'
            }`}
          >
            Requests
          </button>
          <button
            onClick={() => setActiveTab('ratings')}
            className={`px-6 py-3 font-semibold transition ${
              activeTab === 'ratings'
                ? 'border-b-4 border-primary text-primary'
                : 'text-gray-600 hover:text-primary'
            }`}
          >
            Ratings ({ratings.length})
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'sessions' && (
        <div>
          <h2 className="text-2xl font-bold mb-4">My Workout Sessions</h2>
          {sessions.length === 0 ? (
            <div className="card text-center text-gray-500">
              <p>You haven't created any sessions yet</p>
              <p className="text-sm mt-2">Go to the map and create your first session!</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {sessions.map((session) => (
                <div key={session.id} className="card">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <FaDumbbell className="text-primary" />
                        <h3 className="font-bold text-lg">{session.tip_antrenament}</h3>
                        {session.status === 'activ' && <span className="badge-success text-xs">Active</span>}
                        {session.status === 'completat' && <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-semibold">✓ Completed</span>}
                        {session.status === 'anulat' && <span className="bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs font-semibold">Cancelled</span>}
                        {session.status === 'arhivat' && <span className="badge-danger text-xs">Archived</span>}
                      </div>
                      <div className="space-y-1 text-sm text-gray-600 ml-6">
                        <div className="flex items-center space-x-2">
                          <FaClock />
                          <span>{session.interval_orar}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <FaMapMarkerAlt />
                          <span>{session.sala_details.nume}</span>
                        </div>
                        {session.descriere && (
                          <p className="text-gray-700 mt-2">{session.descriere}</p>
                        )}
                      </div>
                    </div>

                    {/* Action Buttons for Active Sessions */}
                    {session.status === 'activ' && (
                      <div className="flex space-x-2 ml-4">
                        <button
                          onClick={() => handleCompleteSession(session.id)}
                          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition"
                          title="Mark as completed"
                        >
                          <FaCheck />
                          <span>Complete</span>
                        </button>
                        <button
                          onClick={() => handleCancelSession(session.id)}
                          className="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition"
                          title="Cancel session"
                        >
                          <FaTimes />
                          <span>Cancel</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'requests' && <RequestManager />}

      {activeTab === 'ratings' && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Ratings & Reviews</h2>
          {ratings.length === 0 ? (
            <div className="card text-center text-gray-500">
              <p>No ratings yet</p>
              <p className="text-sm mt-2">Complete workouts to receive ratings from your buddies!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {ratings.map((rating) => (
                <div key={rating.id} className="card">
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold">
                      {rating.from_user_details.nume.charAt(0).toUpperCase()}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <h3 className="font-bold">{rating.from_user_details.nume}</h3>
                          <p className="text-sm text-gray-600">{rating.from_user_details.grad}</p>
                        </div>
                        <div className="flex items-center space-x-1 text-yellow-500">
                          {'⭐'.repeat(Math.floor(rating.rating))}
                          <span className="ml-2 font-bold">{rating.rating}</span>
                        </div>
                      </div>
                      {rating.comentariu && (
                        <div className="bg-gray-50 rounded-lg p-3 flex items-start space-x-2">
                          <FaComment className="text-gray-400 mt-1" />
                          <p className="text-gray-700 flex-1">{rating.comentariu}</p>
                        </div>
                      )}
                      <p className="text-xs text-gray-500 mt-2">
                        {new Date(rating.data).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Profile;
