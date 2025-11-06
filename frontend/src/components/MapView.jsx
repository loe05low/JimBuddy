import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Icon } from 'leaflet';
import { gymAPI, sessionAPI } from '../services/api';
import { FaDumbbell, FaUser, FaClock, FaInfoCircle } from 'react-icons/fa';
import SessionForm from './SessionForm';
import SessionDetails from './SessionDetails';

// Custom marker icons
const gymIcon = new Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/2936/2936886.png',
  iconSize: [35, 35],
  iconAnchor: [17, 35],
  popupAnchor: [0, -35],
});

const sessionIcon = new Icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/3118/3118203.png',
  iconSize: [40, 40],
  iconAnchor: [20, 40],
  popupAnchor: [0, -40],
});

const MapView = () => {
  const [gyms, setGyms] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [selectedGym, setSelectedGym] = useState(null);
  const [selectedSession, setSelectedSession] = useState(null);
  const [showSessionForm, setShowSessionForm] = useState(false);
  const [loading, setLoading] = useState(true);

  // București center coordinates
  const bucharestCenter = [44.4268, 26.1025];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [gymsResponse, sessionsResponse] = await Promise.all([
        gymAPI.getAll(),
        sessionAPI.getAll({ status: 'activ' }),
      ]);

      setGyms(gymsResponse.data.results || gymsResponse.data);
      setSessions(sessionsResponse.data.results || sessionsResponse.data);
    } catch (error) {
      console.error('Error fetching map data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGymClick = (gym) => {
    setSelectedGym(gym);
    setShowSessionForm(true);
    setSelectedSession(null);
  };

  const handleSessionClick = (session) => {
    setSelectedSession(session);
    setShowSessionForm(false);
    setSelectedGym(null);
  };

  const handleSessionCreated = () => {
    setShowSessionForm(false);
    setSelectedGym(null);
    fetchData(); // Refresh sessions
  };

  if (loading) {
    return (
      <div className="h-96 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-primary border-solid mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading map...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative">
      <div className="h-[600px] rounded-lg overflow-hidden shadow-lg">
        <MapContainer
          center={bucharestCenter}
          zoom={12}
          className="h-full w-full"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Gym Markers */}
          {gyms.map((gym) => (
            <Marker
              key={gym.id}
              position={[parseFloat(gym.latitudine), parseFloat(gym.longitudine)]}
              icon={gymIcon}
              eventHandlers={{
                click: () => handleGymClick(gym),
              }}
            >
              <Popup>
                <div className="p-2">
                  <div className="flex items-center space-x-2 mb-2">
                    <FaDumbbell className="text-primary" />
                    <h3 className="font-bold text-lg">{gym.nume}</h3>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">{gym.adresa}</p>
                  <button
                    onClick={() => handleGymClick(gym)}
                    className="btn-primary text-sm w-full"
                  >
                    Create Session Here
                  </button>
                </div>
              </Popup>
            </Marker>
          ))}

          {/* Active Session Markers */}
          {sessions.map((session) => (
            <Marker
              key={session.id}
              position={[
                parseFloat(session.sala_details.latitudine),
                parseFloat(session.sala_details.longitudine),
              ]}
              icon={sessionIcon}
              eventHandlers={{
                click: () => handleSessionClick(session),
              }}
            >
              <Popup>
                <div className="p-2 min-w-[200px]">
                  <div className="flex items-center space-x-2 mb-2">
                    <FaUser className="text-secondary" />
                    <h3 className="font-bold">{session.user_details.nume}</h3>
                  </div>
                  <div className="space-y-1 text-sm">
                    <div className="flex items-center space-x-2">
                      <FaDumbbell className="text-gray-500" />
                      <span>{session.tip_antrenament}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <FaClock className="text-gray-500" />
                      <span>{session.interval_orar}</span>
                    </div>
                    <div className="flex items-center space-x-1 mt-2">
                      <span className="badge-info text-xs">
                        {session.user_details.grad}
                      </span>
                      <span className="badge-success text-xs">
                        ⭐ {session.user_details.rating}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => handleSessionClick(session)}
                    className="btn-secondary text-sm w-full mt-3"
                  >
                    View Details
                  </button>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      {/* Session Form Modal */}
      {showSessionForm && selectedGym && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] p-4">
          <div className="bg-white rounded-lg max-w-md w-full max-h-[90vh] overflow-y-auto">
            <SessionForm
              gym={selectedGym}
              onClose={() => {
                setShowSessionForm(false);
                setSelectedGym(null);
              }}
              onSuccess={handleSessionCreated}
            />
          </div>
        </div>
      )}

      {/* Session Details Modal */}
      {selectedSession && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999] p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <SessionDetails
              session={selectedSession}
              onClose={() => setSelectedSession(null)}
              onRequestSent={() => {
                setSelectedSession(null);
                fetchData();
              }}
            />
          </div>
        </div>
      )}

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 z-[1000]">
        <h4 className="font-bold text-sm mb-2 flex items-center space-x-1">
          <FaInfoCircle className="text-primary" />
          <span>Legend</span>
        </h4>
        <div className="space-y-2 text-sm">
          <div className="flex items-center space-x-2">
            <img src="https://cdn-icons-png.flaticon.com/512/2936/2936886.png" alt="gym" className="w-6 h-6" />
            <span>Gym Location</span>
          </div>
          <div className="flex items-center space-x-2">
            <img src="https://cdn-icons-png.flaticon.com/512/3118/3118203.png" alt="session" className="w-6 h-6" />
            <span>Active Session</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MapView;
