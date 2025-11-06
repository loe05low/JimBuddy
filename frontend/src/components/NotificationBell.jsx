import { useState, useEffect } from 'react';
import { FaBell, FaTimes, FaCheck, FaCheckDouble } from 'react-icons/fa';
import { notificationAPI } from '../services/api';

const NotificationBell = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchNotifications();
    fetchUnreadCount();

    // Poll for new notifications every 30 seconds
    const interval = setInterval(() => {
      fetchUnreadCount();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await notificationAPI.getAll();
      setNotifications(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  const fetchUnreadCount = async () => {
    try {
      const response = await notificationAPI.getUnreadCount();
      setUnreadCount(response.data.unread_count);
    } catch (error) {
      console.error('Error fetching unread count:', error);
    }
  };

  const handleMarkAsRead = async (id) => {
    try {
      await notificationAPI.markAsRead(id);
      setNotifications(notifications.map(n =>
        n.id === id ? { ...n, citit: true } : n
      ));
      setUnreadCount(Math.max(0, unreadCount - 1));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  const handleMarkAllAsRead = async () => {
    setLoading(true);
    try {
      await notificationAPI.markAllAsRead();
      setNotifications(notifications.map(n => ({ ...n, citit: true })));
      setUnreadCount(0);
    } catch (error) {
      console.error('Error marking all as read:', error);
    } finally {
      setLoading(false);
    }
  };

  const getNotificationIcon = (tip) => {
    switch (tip) {
      case 'cerere_noua':
        return '🤝';
      case 'cerere_acceptata':
        return '🎉';
      case 'cerere_refuzata':
        return '😔';
      case 'rating_nou':
        return '⭐';
      case 'sesiune_reminder':
        return '⏰';
      case 'achievement_unlocked':
        return '🏆';
      case 'follow_nou':
        return '👥';
      default:
        return '🔔';
    }
  };

  const getTimeAgo = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="relative">
      {/* Bell Icon */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-white hover:bg-white hover:bg-opacity-20 rounded-full transition-all"
      >
        <FaBell className="text-xl" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center animate-pulse">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown Panel */}
          <div className="absolute right-0 mt-2 w-96 bg-white rounded-2xl shadow-2xl z-50 max-h-[600px] overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <FaBell className="text-white text-xl" />
                  <h3 className="text-white font-bold text-lg">Notifications</h3>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-full transition-all"
                >
                  <FaTimes />
                </button>
              </div>

              {unreadCount > 0 && (
                <button
                  onClick={handleMarkAllAsRead}
                  disabled={loading}
                  className="mt-3 bg-white text-purple-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-gray-100 transition-all w-full disabled:opacity-50"
                >
                  <FaCheckDouble className="inline mr-2" />
                  Mark All as Read
                </button>
              )}
            </div>

            {/* Notifications List */}
            <div className="max-h-[500px] overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  <FaBell className="text-5xl mx-auto mb-4 text-gray-300" />
                  <p className="text-lg font-semibold">No notifications yet</p>
                  <p className="text-sm mt-2">We'll notify you when something happens!</p>
                </div>
              ) : (
                notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 border-b border-gray-100 hover:bg-gray-50 transition-all cursor-pointer ${
                      !notification.citit ? 'bg-blue-50' : ''
                    }`}
                    onClick={() => !notification.citit && handleMarkAsRead(notification.id)}
                  >
                    <div className="flex items-start space-x-3">
                      {/* Icon */}
                      <div className="text-3xl flex-shrink-0">
                        {getNotificationIcon(notification.tip)}
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between">
                          <h4 className="font-semibold text-gray-800 text-sm">
                            {notification.titlu}
                          </h4>
                          {!notification.citit && (
                            <div className="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0 ml-2 mt-1" />
                          )}
                        </div>
                        <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                          {notification.mesaj}
                        </p>
                        <p className="text-xs text-gray-400 mt-2">
                          {getTimeAgo(notification.data_creare)}
                        </p>
                      </div>

                      {/* Mark as Read Button */}
                      {!notification.citit && (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleMarkAsRead(notification.id);
                          }}
                          className="text-gray-400 hover:text-green-600 transition-colors flex-shrink-0"
                          title="Mark as read"
                        >
                          <FaCheck />
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default NotificationBell;
