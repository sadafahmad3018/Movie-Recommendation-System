from supabase_config import supabase

def add_profile(user):
    try:
        supabase.table("profiles").upsert(
            {
                "id": str(user.id),
                "email": user.email
            },
            on_conflict="id"
        ).execute()

    except Exception:
        pass
def add_favorite(user_id, movie_id, movie_name):
    try:

        existing = (
            supabase.table("favorites")
            .select("id")
            .eq("user_id", user_id)
            .eq("movie_id", movie_id)
            .execute()
        )

        if len(existing.data) > 0:
            return False

        supabase.table("favorites").insert(
            {
                "user_id": user_id,
                "movie_id": movie_id,
                "movie_name": movie_name
            }
        ).execute()

        return True

    except Exception as e:
        print("Favorite Error:", e)
        return False
def get_favorites(user_id):
    try:
        response = (
            supabase.table("favorites")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        return response.data

    except Exception as e:
        print("Get Favorites Error:", e)
        return []
def remove_favorite(favorite_id):
    try:
        supabase.table("favorites")\
            .delete()\
            .eq("id", favorite_id)\
            .execute()

    except Exception as e:
        print("Remove Favorite Error:", e)
def save_history(user_id, movie_id, movie_name):
    try:
        supabase.table("history").insert({
            "user_id": user_id,
            "movie_id": movie_id,
            "movie_name": movie_name
        }).execute()
    except Exception as e:
        print("History Error:", e)

def get_history(user_id):
        print("Logged in user:", user_id)

        response = (
            supabase.table("history")
            .select("*")
            .execute()
        )

        print(response.data)

        return response.data
def remove_favorite_by_movie(user_id, movie_id):
    try:
        (
            supabase.table("favorites")
            .delete()
            .eq("user_id", user_id)
            .eq("movie_id", movie_id)
            .execute()
        )

    except Exception as e:
        print("Remove Favorite Error:", e)

def clear_history(user_id):
    try:
        supabase.table("history") \
            .delete() \
            .eq("user_id", user_id) \
            .execute()
    except Exception as e:
        print("Clear History Error:", e)
def is_favorite(user_id, movie_id):

    response = (
        supabase.table("favorites")
        .select("id")
        .eq("user_id", user_id)
        .eq("movie_id", movie_id)
        .execute()
    )

    return len(response.data) > 0
