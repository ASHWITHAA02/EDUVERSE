from sqlalchemy.orm import Session
from models.user import User
from models.badge import Badge, UserBadge
from models.progress import LessonProgress
from datetime import datetime

def check_and_award_badges(user_id: int, db: Session):
    """Check if user qualifies for any badges and award them"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    awarded_badges = []
    
    # Check "First Steps" badge
    first_lesson = db.query(LessonProgress).filter(
        LessonProgress.user_id == user_id,
        LessonProgress.is_completed == True
    ).first()
    
    if first_lesson:
        badge = db.query(Badge).filter(Badge.criteria == "complete_first_lesson").first()
        if badge:
            existing = db.query(UserBadge).filter(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge.id
            ).first()
            
            if not existing:
                user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
                db.add(user_badge)
                user.total_xp += badge.xp_reward
                awarded_badges.append(badge)
    
    # Check "Streak Champion" badge
    if user.streak_days >= 7:
        badge = db.query(Badge).filter(Badge.criteria == "7_day_streak").first()
        if badge:
            existing = db.query(UserBadge).filter(
                UserBadge.user_id == user_id,
                UserBadge.badge_id == badge.id
            ).first()
            
            if not existing:
                user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
                db.add(user_badge)
                user.total_xp += badge.xp_reward
                awarded_badges.append(badge)
    
    # Update user level
    user.level = (user.total_xp // 1000) + 1
    
    db.commit()
    return awarded_badges

def update_streak(user_id: int, db: Session):
    """Update user's learning streak"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    
    now = datetime.utcnow()
    last_activity = user.last_activity
    
    if last_activity:
        days_diff = (now - last_activity).days
        
        if days_diff == 1:
            # Consecutive day - increment streak
            user.streak_days += 1
        elif days_diff > 1:
            # Streak broken - reset
            user.streak_days = 1
        # If same day, don't change streak
    else:
        user.streak_days = 1
    
    user.last_activity = now
    db.commit()