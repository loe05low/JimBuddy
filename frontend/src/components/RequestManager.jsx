import { useEffect, useState } from 'react';
import { requestAPI, profileAPI } from '../services/api';
import { FaCheck, FaTimes, FaUser, FaDumbbell, FaClock, FaStar } from 'react-icons/fa';

const RequestManager = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await requestAPI.getAll();
      setRequests(response.data.results || response.data);
    } catch (err) {
      setError('Failed to load requests');
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = async (requestId) => {
    try {
      await requestAPI.accept(requestId);
      fetchRequests();
    } catch (err) {
      alert('Failed to accept request');
    }
  };

  const handleReject = async (requestId) => {
    try {
      await requestAPI.reject(requestId);
      fetchRequests();
    } catch (err) {
      alert('Failed to reject request');
    }
  };

  const receivedRequests = requests.filter(
    (req) => req.sesiune_details?.user_details && req.status === 'pending'
  );
  const sentRequests = requests.filter((req) => req.applicant_details);

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-primary border-solid mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading requests...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Received Requests */}
      <div>
        <h2 className="text-2xl font-bold mb-4 flex items-center space-x-2">
          <FaUser className="text-primary" />
          <span>Requests Received</span>
        </h2>

        {receivedRequests.length === 0 ? (
          <div className="card text-center text-gray-500">
            <p>No pending requests</p>
          </div>
        ) : (
          <div className="space-y-3">
            {receivedRequests.map((request) => (
              <div key={request.id} className="card">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold">
                        {request.applicant_details.nume.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <h3 className="font-bold text-lg">{request.applicant_details.nume}</h3>
                        <div className="flex items-center space-x-2">
                          <span className="badge-info text-xs">{request.applicant_details.grad}</span>
                          <span className="badge-success text-xs flex items-center space-x-1">
                            <FaStar />
                            <span>{request.applicant_details.rating}</span>
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="ml-15 space-y-1 text-sm text-gray-600">
                      <div className="flex items-center space-x-2">
                        <FaDumbbell />
                        <span>{request.sesiune_details.tip_antrenament}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <FaClock />
                        <span>{request.sesiune_details.interval_orar}</span>
                      </div>
                      <p className="text-xs">Workouts: {request.applicant_details.nr_antrenamente}</p>
                    </div>
                  </div>
                  <div className="flex flex-col space-y-2">
                    <button
                      onClick={() => handleAccept(request.id)}
                      className="btn-secondary flex items-center space-x-1 text-sm"
                    >
                      <FaCheck />
                      <span>Accept</span>
                    </button>
                    <button
                      onClick={() => handleReject(request.id)}
                      className="btn-danger flex items-center space-x-1 text-sm"
                    >
                      <FaTimes />
                      <span>Reject</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Sent Requests */}
      <div>
        <h2 className="text-2xl font-bold mb-4">My Sent Requests</h2>

        {sentRequests.length === 0 ? (
          <div className="card text-center text-gray-500">
            <p>You haven't sent any requests yet</p>
          </div>
        ) : (
          <div className="space-y-3">
            {sentRequests.map((request) => (
              <div key={request.id} className="card">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <FaDumbbell className="text-primary" />
                      <h3 className="font-bold">{request.sesiune_details.tip_antrenament}</h3>
                    </div>
                    <div className="space-y-1 text-sm text-gray-600">
                      <div className="flex items-center space-x-2">
                        <FaClock />
                        <span>{request.sesiune_details.interval_orar}</span>
                      </div>
                      <p>To: {request.sesiune_details.user_details.nume}</p>
                    </div>
                  </div>
                  <div>
                    {request.status === 'pending' && <span className="badge-warning">Pending</span>}
                    {request.status === 'acceptat' && <span className="badge-success">Accepted</span>}
                    {request.status === 'refuzat' && <span className="badge-danger">Rejected</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RequestManager;
