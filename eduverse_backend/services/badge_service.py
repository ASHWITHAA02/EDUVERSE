from sqlalchemy.orm import Session
from models.badge import Badge, UserBadge
from models.user import User
from datetime import datetime

def award_badge_to_user(user_id: int, badge_criteria: str, db: Session):
    """Award a badge to a user based on criteria"""
    
    # Find badge by criteria
    badge = db.query(Badge).filter(Badge.criteria == badge_criteria).first()
    if not badge:
        return None
    
    # Check if user already has this badge
    existing = db.query(UserBadge).filter(
        UserBadge.user_id == user_id,
        UserBadge.badge_id == badge.id
    ).first()
    
    if existing:
        return None  # Already has badge
    
    # Award badge
    user_badge = UserBadge(
        user_id=user_id,
        badge_id=badge.id,
        earned_at=datetime.utcnow()
    )
    db.add(user_badge)
    
    # Award XP to user
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.total_xp += badge.xp_reward
        user.level = (user.total_xp // 1000) + 1
    
    db.commit()
    db.refresh(user_badge)
    
    return user_badge

def get_user_badges(user_id: int, db: Session):
    """Get all badges earned by a user"""
    
    user_badges = db.query(UserBadge).filter(
        UserBadge.user_id == user_id
    ).all()
    
    return user_badges

def get_available_badges(user_id: int, db: Session):
    """Get badges that user hasn't earned yet"""
    
    earned_badge_ids = db.query(UserBadge.badge_id).filter(
        UserBadge.user_id == user_id
    ).all()
    
    earned_ids = [badge_id[0] for badge_id in earned_badge_ids]
    
    available_badges = db.query(Badge).filter(
        ~Badge.id.in_(earned_ids)
    ).all()
    
    return available_badges