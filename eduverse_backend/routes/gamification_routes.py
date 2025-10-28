from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.badge import Badge, UserBadge
from models.leaderboard import Leaderboard
from routes.auth import get_current_user
from typing import List

router = APIRouter()

@router.get("/badges")
def get_all_badges(db: Session = Depends(get_db)):
    badges = db.query(Badge).all()
    return badges

@router.get("/badges/user")
def get_user_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_badges = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id
    ).all()
    return user_badges

@router.post("/badges/award/{badge_id}")
def award_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if badge exists
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(status_code=404, detail="Badge not found")
    
    # Check if user already has this badge
    existing = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id,
        UserBadge.badge_id == badge_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Badge already earned")
    
    # Award badge
    user_badge = UserBadge(user_id=current_user.id, badge_id=badge_id)
    db.add(user_badge)
    
    # Award XP
    current_user.total_xp += badge.xp_reward
    current_user.level = (current_user.total_xp // 1000) + 1
    
    db.commit()
    db.refresh(user_badge)
    
    return {"message": "Badge awarded successfully", "badge": badge, "xp_earned": badge.xp_reward}

@router.get("/leaderboard")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.total_xp.desc()).limit(limit).all()
    
    leaderboard = []
    for idx, user in enumerate(users, 1):
        leaderboard.append({
            "rank": idx,
            "username": user.username,
            "total_xp": user.total_xp,
            "level": user.level,
            "streak_days": user.streak_days
        })
    
    return leaderboard

@router.get("/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get user's rank
    users = db.query(User).order_by(User.total_xp.desc()).all()
    rank = next((idx + 1 for idx, user in enumerate(users) if user.id == current_user.id), None)
    
    # Get badge count
    badge_count = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).count()
    
    return {
        "username": current_user.username,
        "total_xp": current_user.total_xp,
        "level": current_user.level,
        "rank": rank,
        "streak_days": current_user.streak_days,
        "badges_earned": badge_count
    }