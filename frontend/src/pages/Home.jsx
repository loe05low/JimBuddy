import { FaDumbbell, FaUsers, FaStar, FaMapMarkedAlt } from 'react-icons/fa';
import MapView from '../components/MapView';

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          Find Your Perfect <span className="text-primary">Gym Buddy</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Connect with motivated workout partners in your area. Create sessions, find buddies, and achieve your fitness goals together!
        </p>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-4 gap-6 mb-12">
        <div className="card text-center">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaMapMarkedAlt className="text-3xl text-primary" />
          </div>
          <h3 className="font-bold text-lg mb-2">Interactive Map</h3>
          <p className="text-sm text-gray-600">Browse active workout sessions on an interactive map of București gyms</p>
        </div>

        <div className="card text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaUsers className="text-3xl text-secondary" />
          </div>
          <h3 className="font-bold text-lg mb-2">Connect</h3>
          <p className="text-sm text-gray-600">Send buddy requests and connect with like-minded fitness enthusiasts</p>
        </div>

        <div className="card text-center">
          <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaStar className="text-3xl text-yellow-500" />
          </div>
          <h3 className="font-bold text-lg mb-2">Rate & Review</h3>
          <p className="text-sm text-gray-600">Build your reputation through ratings and reviews from workout partners</p>
        </div>

        <div className="card text-center">
          <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <FaDumbbell className="text-3xl text-purple-600" />
          </div>
          <h3 className="font-bold text-lg mb-2">Track Progress</h3>
          <p className="text-sm text-gray-600">Keep track of your workouts and watch your stats grow</p>
        </div>
      </div>

      {/* Map Section */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-3xl font-bold text-gray-800">Active Workout Sessions</h2>
          <div className="text-sm text-gray-600">
            <span className="font-semibold">Tip:</span> Click on gym markers to create a session, or session markers to join!
          </div>
        </div>
        <MapView />
      </div>

      {/* How It Works */}
      <div className="card bg-gradient-to-br from-blue-50 to-purple-50 mt-12">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
              1
            </div>
            <h3 className="font-bold mb-2">Create or Find Sessions</h3>
            <p className="text-sm text-gray-600">
              Browse the map for active sessions or create your own at your favorite gym
            </p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
              2
            </div>
            <h3 className="font-bold mb-2">Connect & Workout</h3>
            <p className="text-sm text-gray-600">
              Send buddy requests, review profiles, and meet up for your workout session
            </p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-primary text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
              3
            </div>
            <h3 className="font-bold mb-2">Rate & Build Trust</h3>
            <p className="text-sm text-gray-600">
              After your workout, rate your buddy and build your fitness community reputation
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
