import { useState } from 'react';
import { requestAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { FaTimes, FaUser, FaDumbbell, FaClock, FaMapMarkerAlt, FaStar, FaInfoCircle } from 'react-icons/fa';

const SessionDetails = ({ session, onClose, onRequestSent }) => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const isOwnSession = user?.profile?.id === session.user_details.id;

  const handleSendRequest = async () => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await requestAPI.create({ sesiune: session.id });
      setSuccess('Request sent successfully!');
      setTimeout(() => {
        onRequestSent();
      }, 1500);
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Failed to send request';
      setError(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Session Details</h2>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
          <FaTimes className="text-2xl" />
        </button>
      </div>

      {/* Messages */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4 text-sm">
          {error}
        </div>
      )}
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-4">
          {success}
        </div>
      )}

      {/* User Info */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center text-white text-2xl font-bold">
              {session.user_details.nume.charAt(0).toUpperCase()}
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-800">{session.user_details.nume}</h3>
              <div className="flex items-center space-x-2 mt-1">
                <span className="badge-info text-xs">{session.user_details.grad}</span>
                <span className="badge-success text-xs flex items-center space-x-1">
                  <FaStar className="text-xs" />
                  <span>{session.user_details.rating}</span>
                </span>
              </div>
            </div>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">Workouts</p>
            <p className="text-2xl font-bold text-primary">{session.user_details.nr_antrenamente}</p>
          </div>
        </div>
      </div>

      {/* Session Info */}
      <div className="space-y-3 mb-6">
        <div className="flex items-start space-x-3">
          <FaDumbbell className="text-primary mt-1" />
          <div>
            <p className="text-sm text-gray-600">Workout Type</p>
            <p className="font-semibold">{session.tip_antrenament}</p>
          </div>
        </div>

        <div className="flex items-start space-x-3">
          <FaClock className="text-primary mt-1" />
          <div>
            <p className="text-sm text-gray-600">Time Slot</p>
            <p className="font-semibold">{session.interval_orar}</p>
          </div>
        </div>

        <div className="flex items-start space-x-3">
          <FaMapMarkerAlt className="text-primary mt-1" />
          <div>
            <p className="text-sm text-gray-600">Location</p>
            <p className="font-semibold">{session.sala_details.nume}</p>
            <p className="text-sm text-gray-500">{session.sala_details.adresa}</p>
          </div>
        </div>

        {session.descriere && (
          <div className="flex items-start space-x-3">
            <FaInfoCircle className="text-primary mt-1" />
            <div>
              <p className="text-sm text-gray-600">Description</p>
              <p className="text-gray-700">{session.descriere}</p>
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      {!isOwnSession && (
        <div className="border-t pt-4">
          <button
            onClick={handleSendRequest}
            disabled={loading}
            className="w-full btn-secondary disabled:opacity-50"
          >
            {loading ? 'Sending Request...' : 'Send Buddy Request'}
          </button>
          <p className="text-xs text-gray-500 text-center mt-2">
            The session owner will review your profile before accepting
          </p>
        </div>
      )}

      {isOwnSession && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800 text-center">
            This is your session. Check "My Requests" to see who wants to join!
          </p>
        </div>
      )}
    </div>
  );
};

export default SessionDetails;
