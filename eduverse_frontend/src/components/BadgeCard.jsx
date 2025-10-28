const BadgeCard = ({ badge, earned = false }) => {
  return (
    <div
      className={`p-4 rounded-xl border-2 transition-all ${
        earned
          ? "bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 border-yellow-400"
          : "bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-600 opacity-60"
      }`}
    >
      <div className="text-center">
        <div className="text-5xl mb-2">{badge.icon}</div>
        <h3 className="font-bold text-gray-800 dark:text-white mb-1">
          {badge.name}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          {badge.description}
        </p>
        <div className="flex items-center justify-center gap-1 text-yellow-600 dark:text-yellow-400">
          <span className="font-bold">+{badge.xp_reward} XP</span>
        </div>
      </div>
    </div>
  );
};

export default BadgeCard;