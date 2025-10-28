from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.game_score import GameScore
from schemas.game import GameScoreSubmit, GameScoreResponse, GameLeaderboardEntry
from routes.auth import get_current_user
from typing import List

router = APIRouter()

# Define available games
AVAILABLE_GAMES = {
    "coding_challenge": {
        "name": "Coding Challenge",
        "description": "Solve coding problems to earn points",
        "xp_multiplier": 2,
        "instructions": "Write code to solve the given problem. Each correct solution earns you points!"
    },
    "memory_match": {
        "name": "Memory Match",
        "description": "Match programming concepts with their definitions",
        "xp_multiplier": 1.5,
        "instructions": "Click cards to flip them. Match pairs of related concepts to score points!"
    },
    "speed_typing": {
        "name": "Code Speed Typing",
        "description": "Type code snippets as fast as you can",
        "xp_multiplier": 1.5,
        "instructions": "Type the code shown on screen as quickly and accurately as possible!"
    },
    "syntax_puzzle": {
        "name": "Syntax Puzzle",
        "description": "Arrange code blocks in the correct order",
        "xp_multiplier": 2,
        "instructions": "Drag and drop code blocks to create a working program!"
    },
    "bug_hunter": {
        "name": "Bug Hunter",
        "description": "Find and fix bugs in code",
        "xp_multiplier": 2.5,
        "instructions": "Identify bugs in the code and fix them. Faster fixes earn more points!"
    },
    "algorithm_race": {
        "name": "Algorithm Race",
        "description": "Solve algorithmic challenges against the clock",
        "xp_multiplier": 3,
        "instructions": "Solve algorithm problems as quickly as possible. Time matters!"
    }
}

@router.get("/list")
def get_available_games():
    """Get list of all available games"""
    games_list = []
    for game_id, game_info in AVAILABLE_GAMES.items():
        games_list.append({
            "name": game_id,  # This is the game identifier (e.g., "coding_challenge")
            "display_name": game_info["name"],  # This is the display name (e.g., "Coding Challenge")
            "description": game_info["description"],
            "instructions": game_info["instructions"],
            "xp_multiplier": game_info["xp_multiplier"],
            "difficulty": "Medium"  # Default difficulty
        })
    return games_list

@router.get("/game/{game_name}")
def get_game_info(game_name: str):
    """Get information about a specific game"""
    
    if game_name not in AVAILABLE_GAMES:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_info = AVAILABLE_GAMES[game_name]
    return {
        "id": game_name,
        "name": game_info["name"],
        "description": game_info["description"],
        "instructions": game_info["instructions"],
        "xp_multiplier": game_info["xp_multiplier"]
    }

@router.post("/submit-score", response_model=GameScoreResponse)
def submit_game_score(
    score_data: GameScoreSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit game score"""
    
    # Validate game name
    if score_data.game_name not in AVAILABLE_GAMES:
        raise HTTPException(status_code=400, detail="Invalid game name")
    
    # Calculate XP based on score and game multiplier
    game_info = AVAILABLE_GAMES[score_data.game_name]
    xp_earned = int(score_data.score * game_info["xp_multiplier"])
    
    # Create game score record
    game_score = GameScore(
        user_id=current_user.id,
        game_name=score_data.game_name,
        score=score_data.score,
        time_taken_seconds=score_data.time_taken_seconds,
        difficulty_level=score_data.difficulty_level,
        xp_earned=xp_earned
    )
    
    db.add(game_score)
    
    # Award XP to user
    current_user.total_xp += xp_earned
    current_user.level = (current_user.total_xp // 1000) + 1
    
    db.commit()
    db.refresh(game_score)
    
    return game_score

@router.get("/my-scores", response_model=List[GameScoreResponse])
def get_my_scores(
    game_name: str = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's game scores"""
    
    query = db.query(GameScore).filter(GameScore.user_id == current_user.id)
    
    if game_name:
        query = query.filter(GameScore.game_name == game_name)
    
    scores = query.order_by(GameScore.created_at.desc()).limit(limit).all()
    
    return scores

@router.get("/leaderboard/{game_name}", response_model=List[GameLeaderboardEntry])
def get_game_leaderboard(
    game_name: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get leaderboard for a specific game"""
    
    if game_name not in AVAILABLE_GAMES:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Get top scores for this game
    from sqlalchemy import func
    
    # Get best score for each user
    subquery = db.query(
        GameScore.user_id,
        func.max(GameScore.score).label('best_score')
    ).filter(
        GameScore.game_name == game_name
    ).group_by(GameScore.user_id).subquery()
    
    # Get full records for best scores
    top_scores = db.query(GameScore).join(
        subquery,
        (GameScore.user_id == subquery.c.user_id) & 
        (GameScore.score == subquery.c.best_score)
    ).filter(
        GameScore.game_name == game_name
    ).order_by(GameScore.score.desc()).limit(limit).all()
    
    # Format leaderboard
    leaderboard = []
    for idx, score in enumerate(top_scores, 1):
        leaderboard.append({
            "rank": idx,
            "username": score.user.username,
            "score": score.score,
            "time_taken_seconds": score.time_taken_seconds,
            "created_at": score.created_at
        })
    
    return leaderboard

@router.get("/stats")
def get_game_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's gaming statistics"""
    
    from sqlalchemy import func
    
    # Total games played
    total_games = db.query(func.count(GameScore.id)).filter(
        GameScore.user_id == current_user.id
    ).scalar() or 0
    
    # Total XP from games
    total_xp = db.query(func.sum(GameScore.xp_earned)).filter(
        GameScore.user_id == current_user.id
    ).scalar() or 0
    
    # Best score overall
    best_score = db.query(func.max(GameScore.score)).filter(
        GameScore.user_id == current_user.id
    ).scalar() or 0
    
    # Average score
    average_score = db.query(func.avg(GameScore.score)).filter(
        GameScore.user_id == current_user.id
    ).scalar() or 0
    
    return {
        "total_games_played": total_games,
        "total_xp_earned": int(total_xp),
        "best_score": int(best_score),
        "average_score": float(average_score),
        "games_available": len(AVAILABLE_GAMES)
    }