from fastapi import APIRouter

router = APIRouter(prefix="/promote", tags=["Promote"])

@router.get("/")
def get_promotion_list():
    return {
        "status": "success", 
        "data": [
            {"id": 1, "title": "달빛정원 메인 홍보 서버", "category": "FiveM"},
            {"id": 2, "title": "함께 성장하는 개발자 커뮤니티", "category": "Community"}
        ]
    }