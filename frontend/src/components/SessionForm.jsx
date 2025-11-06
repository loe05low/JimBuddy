import { useState } from 'react';
import { sessionAPI } from '../services/api';
import { FaTimes, FaDumbbell } from 'react-icons/fa';

const SessionForm = ({ gym, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    tip_antrenament: '',
    interval_orar: '',
    descriere: '',
    data_expirare: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Convert datetime-local to ISO format with timezone
      const expirationDate = new Date(formData.data_expirare);
      const isoExpiration = expirationDate.toISOString();

      await sessionAPI.create({
        ...formData,
        data_expirare: isoExpiration,
        sala: gym.id,
      });

      onSuccess();
    } catch (err) {
      console.error('Session creation error:', err.response?.data);
      setError(err.response?.data?.error || 'Failed to create session');
    } finally {
      setLoading(false);
    }
  };

  // Set default expiration to 24 hours from now
  const getDefaultExpiration = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().slice(0, 16);
  };

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Create Workout Session</h2>
          <p className="text-sm text-gray-600 mt-1">at {gym.nume}</p>
        </div>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
          <FaTimes className="text-2xl" />
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Workout Type *
          </label>
          <input
            type="text"
            name="tip_antrenament"
            value={formData.tip_antrenament}
            onChange={handleChange}
            required
            className="input-field"
            placeholder="e.g., Cardio, Strength, CrossFit"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Time Slot *
          </label>
          <input
            type="text"
            name="interval_orar"
            value={formData.interval_orar}
            onChange={handleChange}
            required
            className="input-field"
            placeholder="e.g., 18:00 - 20:00"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description (Optional)
          </label>
          <textarea
            name="descriere"
            value={formData.descriere}
            onChange={handleChange}
            rows="3"
            className="input-field"
            placeholder="Add details about your workout plan..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Expires At *
          </label>
          <input
            type="datetime-local"
            name="data_expirare"
            value={formData.data_expirare || getDefaultExpiration()}
            onChange={handleChange}
            required
            className="input-field"
          />
          <p className="text-xs text-gray-500 mt-1">
            Session will be automatically archived after this time
          </p>
        </div>

        <div className="flex space-x-3 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 btn-primary disabled:opacity-50"
          >
            {loading ? 'Creating...' : 'Create Session'}
          </button>
          <button
            type="button"
            onClick={onClose}
            className="flex-1 btn-outline"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default SessionForm;
