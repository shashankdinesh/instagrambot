from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from instaservices import views

app_name = 'instaservices'

urlpatterns = [
    path(
        "getprofile/",
        views.GetProfileAPI.as_view(),
        name="get_profile",
    ),
    path(
        "signin/",
        views.SignInAPI.as_view(),
        name="sign_in",
    ),
    path(
        "follow/",
        views.FollowCandidateAPI.as_view(),
        name="follow",
    ),
    path(
        "unfollow/",
        views.UnFollowSingleUserAPI.as_view(),
        name="unfollow_single_user",
    ),
    path(
        "followfollowersv1/",
        views.FollowUserFollowersAPIv1.as_view(),
        name="targetFollowers",
    ),
    path(
        "unfollowfollowers/",
        views.UnfollowUserFollowersAPI.as_view(),
        name="unfollowfollowers",
    ),

    path(
        "like_posts/",
        views.LikePostsAPI.as_view(),
        name="like_posts_of_hashtag",
    ),

    path(
        "getpost/",
        views.PostScrappingAPI.as_view(),
        name="posts",
    ),

    path(
        "single_post/",
        views.SinglePostAPI.as_view(),
        name="single_post",
    ),

    path('get_login_status', views.LoginStatusAPI.as_view(), name='get_login_status'),
]