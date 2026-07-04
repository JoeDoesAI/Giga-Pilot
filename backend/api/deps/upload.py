from fastapi import Request

async def get_supabase(request: Request):
    yield request.app.state.supabase